[![Python package](https://github.com/unitrium/02180-Introduction-to-AI-SP21-BOARD-GAME-ASSIGNMENT/actions/workflows/python-test.yml/badge.svg)](https://github.com/unitrium/02180-Introduction-to-AI-SP21-BOARD-GAME-ASSIGNMENT/actions/workflows/python-test.yml)
# 02180 - Introduction to AI - SP21 - BOARD GAME ASSIGNMENT

Assignement for the course 02180 Introduction to AI.   

The goal of this assignment is to implement an AI which play a board game.  

This code is for the game called __Taiji__.

## Description

__Taiji__ is a two-player game whose goal is to have the 3 biggest groups of one's color by placing black and white tiles in a 11x11 board.
A group is composed by all the squares connected to each other horizontally or vertically (not diagonally).
The game ends when there are no more empty space of size 2. The player with the highest score wins the game.

## Requirements

python 3.8

## Run the code

In order to play this game, you have to run 
```python
python3 main.py
```

Then you have to choose if you want to play with an AI (YES/NO) and which color you want (WHITE/BLACK). The white player starts the game.

In our implementation, X represents the white color and O represents the black one.  

When it's your turn you have to indicate where you want to play by giving the x and y coordinates of the white part of the piece and the direction d of where will put the black part.
