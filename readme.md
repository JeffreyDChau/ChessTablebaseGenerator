# Chess Tablebase Generator

The Chess Tablebase Generator purpose is to generate a tablebase and store it onto DynamoDB.

## Description

Given an starting FEN(A string to represent the chessboard) table on DynamoDB should return A Win/Draw/Loss ex:"White win" and a ending fen. Each of these values are partitioned by the starting fen. 

## Getting Started
Clone the repo into your project folder.

This project require python in order to generate the tablebase. It will also require the use of DynamoDB in order to store the large amounts of data.

Download link for Python:https://www.python.org/downloads/

Create an keys.py file in root of project to contain AWS credentials
```bash
ACCESS_KEY = # AWS access key
SECRET_KEY = # AWS secret key
REGION = # AWS region
```

## File Stucture
* _pycache_ - Containes imports for keys.
    * keys.cpython-310.pyc - key
* stockfish_15.1 - Stockfish engine, used for calculating best move
* gitignore - a ignore file to hide access and secret keys 
* generator.py - genereates and stores tablebase into dynamodb
* readme - information about the project
* keys.py - contains AWS DynamoDB credentials used to store into database hidden in gitignore file

### Dependencies

Install the following dependences:

Python chess
```bash
pip install chess
```

Stockfish engine
```bash
pip install stockfish
```

Boto3 SDK for AWS
```bash
pip install boto3
```

### Generator.py



```
code blocks for commands
```pip install chess
## Authors

Contributors names and contact info

Contributer: Jeffrey Chau 
Email:jeffrey.chau@seattlecolleges.edu