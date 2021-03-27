[![Python package](https://github.com/unitrium/02180-Introduction-to-AI-SP21-BOARD-GAME-ASSIGNMENT/actions/workflows/python-test.yml/badge.svg)](https://github.com/unitrium/02180-Introduction-to-AI-SP21-BOARD-GAME-ASSIGNMENT/actions/workflows/python-test.yml)
# 02180 - Introduction to AI - SP21 - BOARD GAME ASSIGNMENT

Assignement for the course 02180 Introduction to AI.   

The goal of this assignment is to implement an AI which play a board game.  

This code is for the game called __Taiji__.

## Requirements

python 3.8

## How to play

In order to play this game, you have to run 
```python
python3 main.py
```

Then you have to choose if you want to play with an AI (YES/NO) and which color you want (WHITE/BLACK). 

In our implementation, X represents the white color and O represents the black one.  

When it's your turn you have to indicate where you want to play by giving the x and y coordinates of the white part of the piece and the direction d of where will put the black part.  

## How to win

At the end of the game -when there is no more adjacent free squares on the board- the code will compute the score of each players by computing the 3 biggest groups of each player color. The one with the highest score win the game.
