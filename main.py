# -*- coding: utf-8 -*-
# ◻︎◯✕

from sys import exit
from time import sleep as sleep
from random import randint as randint

import numpy as np

class Board():

    def __init__(self, row_num: int, col_num: int):
        board = []
        cell_ind = 1
        for row_ind in range(row_num):
            board.append([])
            for col_ind in range(col_num):
                board[row_ind].append(cell_ind)
                cell_ind += 1
        self.row_num = row_num
        self.col_num = col_num
        self.board = np.array(board, dtype=str)

    def show_board(self):
        for row in self.board:
            for cell in row:
                print(cell, ' ', end='')
            print()

    def get_cell_positions(self, player_turn: int) -> np.ndarray:
        cell_positions = []
        cell_ind = 1
        for row_ind in range(len(self.board)):
            cell_positions.append([])
            for col_ind in range(len(self.board[row_ind])):
                cell_positions[row_ind].append((row_ind, col_ind, cell_ind))
                cell_ind += 1
        return np.array(cell_positions, dtype=np.int32)

    def find_cell_by_ind(self, player_turn: int) -> tuple[int]:
        cell_positions = self.get_cell_positions(player_turn)
        for row_ind in range(len(cell_positions)):
            for col_ind in range(len(cell_positions[row_ind])):
                if cell_positions[row_ind, col_ind, -1] == player_turn:
                    return row_ind, col_ind

class Game(Board):
    
    class PlayerWin(Exception):
        pass

    class AIWin(Exception):
        pass

    def __init__(self, row_num: int = 3, col_num: int = 3):
        super().__init__(row_num, col_num)
        print('tic-tac-toe'.upper())

    def ai_take_turn(self):
        print('AI is making a turn...')
        sleep(2)
        ai_turn = randint(1, self.row_num*self.col_num)
        cell_position = self.find_cell_by_ind(ai_turn)
        while (self.board[cell_position] == '◯'
               or self.board[cell_position] == '✕'):
            ai_turn = randint(1, self.row_num*self.col_num)
            cell_position = self.find_cell_by_ind(ai_turn)
        self.board[cell_position] = '✕'

    def take_turn(self):
        player_turn = int(input('Make your step: '))
        cell_position = self.find_cell_by_ind(player_turn)
        while self.board[cell_position] == '✕':
            player_turn = int(input('This cell is take, choose another: '))
            cell_position = self.find_cell_by_ind(player_turn)   
        self.board[cell_position] = '◯'

    def check_bingo(self):
        try:
            for row in self.board:
                if set(row.tolist()) == {'◯'}:
                    raise self.PlayerWin
                elif set(row.tolist()) == {'✕'}:
                    raise self.AIWin
            for col_ind in range(self.col_num):
                if set(self.board[:, col_ind].tolist()) == {'◯'}:
                    raise self.PlayerWin
                elif set(self.board[:, col_ind].tolist()) == {'✕'}:
                    raise self.AIWin
        except self.PlayerWin:
            self.show_board()
            print('You won! Game ended.')
            exit(0)
        except self.AIWin:
            self.show_board()
            print('AI won! Game ended.')
            exit(0)

if __name__ == '__main__':
    row_num = input('Would you set up row number (3)? If no, then just Enter: ')
    col_num = input('Would you set up column number (3)? If no, then just Enter: ')
    
    while True:
        if row_num.isnumeric() and col_num.isnumeric():
            game = Game(int(row_num), int(col_num))
            break
        elif row_num == '' and col_num == '':
            game = Game()
            break
        else:
            print('You entered something wrong, let\'s try again.')
            continue

    while True:
        game.show_board()
        game.take_turn()
        game.check_bingo()
        game.show_board()
        game.ai_take_turn()
        game.check_bingo()
