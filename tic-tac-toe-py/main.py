# -*- coding: utf-8 -*-

from os import system as sys
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
        self.board = board

    def show_board(self):
        for row in self.board:
            for cell in row:
                print(cell, ' ', end='')
            print()

    def get_cell_positions(self, player_turn: int) -> list:
        cell_positions = []
        cell_ind = 1
        for row_ind in range(len(self.board)):
            cell_positions.append([])
            for col_ind in range(len(self.board[row_ind])):
                cell_positions[row_ind].append((row_ind, col_ind, cell_ind))
                cell_ind += 1
        return cell_positions

    def find_cell_by_ind(self, player_turn: int) -> tuple:
        cell_positions = self.get_cell_positions(player_turn)
        for row_ind in range(len(cell_positions)):
            for col_ind in range(len(cell_positions[row_ind])):
                if cell_positions[row_ind][col_ind][-1] == player_turn:
                    return row_ind, col_ind

class Game(Board):
    
    class PlayerWin(Exception):
        pass

    class AIWin(Exception):
        pass

    class Draw(Exception):
        pass

    def __init__(self, row_num: int = 3, col_num: int = 3):
        super().__init__(row_num, col_num)
        print('\ntic-tac-toe'.upper())

    def ai_take_turn(self):
        print('AI is making a turn...')
        sleep(2)
        ai_turn = randint(1, self.row_num*self.col_num)
        cell_position = self.find_cell_by_ind(ai_turn)
        while (self.board[cell_position[0]][cell_position[1]] == '◯'
               or self.board[cell_position[0]][cell_position[1]] == '✕'):
            ai_turn = randint(1, self.row_num*self.col_num)
            cell_position = self.find_cell_by_ind(ai_turn)
        self.board[cell_position[0]][cell_position[1]] = '✕'

    def take_turn(self):
        while True:
            try:
                player_turn = int(input('Make your step: '))
                cell_position = self.find_cell_by_ind(player_turn)
                break
            except ValueError:
                print('You entered something wrong. Let\'s again.')
                continue

        while self.board[cell_position[0]][cell_position[1]] == '✕':
            try:
                player_turn = int(
                                  input('This cell is taken, choose another: '))
                cell_position = self.find_cell_by_ind(player_turn)
            except ValueError:
                print('You entered something wrong. Let\'s again.')
                continue
        self.board[cell_position[0]][cell_position[1]] = '◯'

    def check_board(self):
        try:
            for row in self.board:
                if set(row) == {'◯'}:
                    raise self.PlayerWin
                elif set(row) == {'✕'}:
                    raise self.AIWin

            for col_ind in range(self.col_num):
                if set(np.array(self.board)[:, col_ind].tolist()) == {'◯'}:
                    raise self.PlayerWin
                elif set(np.array(self.board)[:, col_ind].tolist()) == {'✕'}:
                    raise self.AIWin
            
            filled_row_num = 0
            for row in self.board:
                if set(row) == {'◯', '✕'} :
                        filled_row_num += 1
                        if filled_row_num == self.row_num:
                            raise self.Draw
        except self.PlayerWin:
            sys('clear')
            self.show_board()
            print('You won! Game ended.')
            is_restart = input('Would you restart? Yes or no: ').lower()
            sys('clear')
            if is_restart == 'yes':
                restart()
            else:
                exit(0)
        except self.AIWin:
            sys('clear')
            self.show_board()
            print('AI won! Game ended.')
            is_restart = input('Would you restart? Yes or no: ').lower()
            sys('clear')
            if is_restart == 'yes':
                restart()
            else:
                exit(0)
            exit(0)
        except self.Draw:
            sys('clear')
            self.show_board()
            print('Draw! Game ended.')
            is_restart = input('Would you restart? Yes or no: ').lower()
            sys('clear')
            if is_restart == 'yes':
                restart()
            else:
                exit(0)
            exit(0)

def setup():
    while True:
        row_num = input('Would you set up row number (3)? If no, then just Enter: ')
        col_num = input('Would you set up column number (3)? If no, then just Enter: ')

        if row_num.isnumeric() and col_num.isnumeric():
            game = Game(int(row_num), int(col_num))
            break
        elif row_num == '' and col_num == '':
            game = Game()
            break
        else:
            print('You entered something wrong, let\'s try again.')
            continue
    return game

def run(game: Game):
    while True:
        game.show_board()
        game.take_turn()
        game.check_board()
        sys('clear')
        game.show_board()
        game.ai_take_turn()
        game.check_board()
        sys('clear')

def restart():
    game = setup()
    run(game)

if __name__ == '__main__':
    game = setup() 
    run(game)
