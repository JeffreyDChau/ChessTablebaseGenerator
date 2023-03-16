import chess
from stockfish import Stockfish
import boto3
from botocore.config import Config
import keys

config = Config(
    retries=dict(
        max_attempts=20
    )
)
## Setup Boto3 to connect to AWS
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=keys.ACCESS_KEY,
    aws_secret_access_key=keys.SECRET_KEY,
    region_name=keys.REGION,
    config=config
)
##Label Dynamodb Table
table = dynamodb.Table('Two_piece_tablebase')
table2 = dynamodb.Table('Three_piece_tablebase')

#Import stockfish engine to generate solutions
stockfish = Stockfish(path="stockfish_15.1/stockfish-windows-2022-x86-64-avx2.exe")

#Check if current boardstate is checkmate. Return true or false
def isCheckmate(board):
    if board.is_checkmate():
        return True
    else:
        return False

##Takes chess piece type and position and evaluates best move based on current boardstate
def bestMove(board, move_count):
    stockfish.set_fen_position(board.fen())
    best_move = chess.Move.from_uci(stockfish.get_best_move())

    print("The piece moved:" + str(best_move))
    board.push(best_move)
    move_count = move_count + 1
    print("move: " + str(move_count) +"\n" + str(board))

    threePieceGen(board, move_count)

#Generates all possible positions for the king and stores tablebase which should always be a draw
def twoPieceGen(board):
    board.clear_board()
    board.set_piece_at(chess.A1, chess.Piece(chess.KING, chess.WHITE))
    board.set_piece_at(chess.H8, chess.Piece(chess.KING, chess.BLACK))

    for king1_square in chess.SQUARES:
        for king2_square in chess.SQUARES:
            if king1_square == king2_square:
                continue
            board.set_piece_at(king1_square, chess.Piece(chess.KING, chess.WHITE))
            board.set_piece_at(king2_square, chess.Piece(chess.KING, chess.BLACK))
            item = {
                'starting_fen': board.fen(),
                'result': 'Draw',
                'ending_fen': board.fen()
            }
            table.put_item(Item=item)
            board.remove_piece_at(king1_square)
            board.remove_piece_at(king2_square)

# Generates an item that stores beginning boardstate, Win/Draw/Loss and ending boardstate.
# If boardstate is not an ideal endgamestate, will run best move to change gamestate
def threePieceGen(board, move_count):
    if len(board.piece_map()) ==2:
            item = {
                'starting_fen': board.fen(),
                'result': 'Draw',
                'ending_fen': board.fen()
            }
            table2.put_item(Item=item)
    elif isCheckmate(board):
        results = board.result()
        winner =""
        print(board.fen())
        if results == "1-0":
            print("White wins!" + " in " + str(move_count) + "moves")
            winner="White win"
            
        elif results == "0-1":
            print("Black wins!" + " in " + str(move_count) + "moves")
            winner="Black win"
        print("Endgame board state:\n" + str(board))
        print("Storing: \n" + "Starting fen: " + str(starting_fen) + "\nw/d/l: "+ winner + "\nEnding fen: " + str(board.fen()))
        item = {
                'starting_fen': board.fen(),
                'result': winner,
                'ending_fen': board.fen()
            }
        table2.put_item(Item=item)
    elif board.can_claim_threefold_repetition():
        print("Repeated move move 3 times. Therefore draw")
        print("Storing: \n" + "Starting fen: " + str(starting_fen) + "\nw/d/l: "+ "Draw" + "\nEnding fen: " + str(board.fen()))
        item = {
                'starting_fen': board.fen(),
                'result': 'Draw',
                'ending_fen': board.fen()
            }
        table2.put_item(Item=item)
    elif board.is_fifty_moves():
        print("No change in board state in 50 turns. Therefore draw")
        print("Storing: \n" + "Starting fen: " + str(starting_fen) + "\nw/d/l: "+ "Draw" + "\nEnding fen: " + str(board.fen()))
        item = {
                'starting_fen': board.fen(),
                'result': 'Draw',
                'ending_fen': board.fen()
            }
        table2.put_item(Item=item)
    else:
        bestMove(board, move_count)

## --------------------------------------Start READING HERE -----------------------------------------
#Diffrent board states to test. Use to test if solver is working and to start the generator
#KRvK
board = chess.Board("5k2/8/8/4R1K1/8/8/8/8 w - - 0 1")

#KPvK
#board = chess.Board("8/8/P1K3k1/8/8/8/8/8 w - - 0 1")

#KQvK
#board = chess.Board("8/2Q5/6k1/8/3K4/8/8/8 w - - 0 1")

#KvK
#board = chess.Board("4k3/8/8/4K3/8/8/8/8 b - - 0 1")
#KBvK
#board = chess.Board("8/5k2/8/2B1K3/8/8/8/8 w - - 0 1")

#KNvK
#board = chess.Board("8/2n2k2/8/4K3/8/8/8/8 b - - 0 1")

#Draw situations
#Board will have a situation over 50 turns
#board = chess.Board("4k3/8/8/4P3/8/4K3/8/8 b - - 0 1")

##Print boardstate given
print("Total number of pieces on the board:", len(board.piece_map()))
print("Starting board: \n" + str(board))
starting_fen = board.fen()

#Checks if boardstate has only two pieces. If so, generate an 2 piece tablebase
if len(board.piece_map()) ==2:
   twoPieceGen(board)
   

#Checks if boardstate has only three pieces. If so, check conditions if there is a automatic draw. Generates a three piece tablebase if conditions are correct
if len(board.piece_map()) ==3:
    fenBoard = str(board.fen())
    print(fenBoard)
    if fenBoard.count("b") > 1 or fenBoard.count("B") >= 1 :
        print("Bishop and king cannot checkmate. Therefore draw")
        print("Storing: \n" + "Starting fen: " + str(starting_fen) + "\nw/d/l: "+ "Draw" + "\nEnding fen: " + str(board.fen()))
    elif fenBoard.__contains__('n') or fenBoard.__contains__('N'):
        print("Knight and king cannot checkmate. Therefore draw")
        print("Storing: \n" + "Starting fen: " + str(starting_fen) + "\nw/d/l: "+ "Draw" + "\nEnding fen: " + str(board.fen()))
    else:
        threePieceGen(board, 0)
    