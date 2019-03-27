import chess.pgn
import time
import sys
import math
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD, Adadelta, Adam, RMSprop
from keras.callbacks import ModelCheckpoint, TensorBoard

BOARD_SPACES = 64
ROWS = 8
COLS = 8

letter_lookup = {
    'a':0,
    'b':1,
    'c':2,
    'd':3,
    'e':4,
    'f':5,
    'g':6,
    'h':7
}
piece_lookup = {
    'r':0,
    'n':1,
    'b':2,
    'q':3,
    'k':4,
    'p':5,
    'R':6,
    'N':7,
    'B':8,
    'Q':9,
    'K':10,
    'P':11,
    '.':-1
}

def make_net(inshape, outshape):
    model = Sequential()
    model.add(Conv2D(128, kernel_size=(2, 2), padding='same',
                    input_shape=inshape))
    model.add(Activation('relu'))

    model.add(Conv2D(128, kernel_size=(2, 2), padding='same'))
    model.add(Activation('relu'))

    model.add(Flatten())

    model.add(Dense(1024))
    model.add(Activation('relu'))

    model.add(Dense(1024))
    model.add(Activation('relu'))

    model.add(Dense(outshape, activation='sigmoid'))

    model.compile(loss=keras.losses.mean_squared_error,
                optimizer=Adam(lr=0.001),
                metrics=['mse'])
    return model

def board2array(board, black_or_white):
    strboard = str(board)
    board_data = np.zeros((8, 8, 13))
    idx = 0
    for char in strboard:
        if char in piece_lookup:
            if char != '.':
                piece = np.zeros(13)
                piece[piece_lookup[char]] = 1
                if black_or_white == True:
                    piece[-1] = 1
                board_data[int(idx/COLS)][idx%ROWS] = piece
            idx += 1
    return board_data

def main(num_games=1000):
    dataset_x = []
    dataset_y = []
    posns = []

    pgn = open("data/AllGames.pgn")
    game = chess.pgn.read_game(pgn)
    black_or_white = True
    count = 0
    white_win = None

    while game != None:
        # Get the game board
        board = game.board()

        # Truncate the number of games
        count += 1
        if count >= num_games:
            break

        # Determine the winner of the game
        result = game.headers['Result']
        if result == '1-0':
            white_win = 1
        elif result == '0-1':
            white_win = 0
        else:
            white_win = 0.5
        num_moves = sum(1 for _ in game.mainline_moves())
                
        for i, move in enumerate(game.mainline_moves()):
            # Compute the board state
            state = 0.5*float(i+1)/num_moves
            if black_or_white == False:
                state *= -1
            state += 0.5        
            board.push(move)
                    
            # Turn the board into a vector
            board_data = board2array(board, black_or_white)
                    
            dataset_x.append(board_data)
            dataset_y.append(np.array(state))
            black_or_white = not black_or_white

        game = chess.pgn.read_game(pgn)

    dataset_x = np.stack(dataset_x)
    dataset_y = np.stack(dataset_y)

    inshape = dataset_x[0].shape
    outshape = dataset_y[0].size

    model = make_net(inshape, outshape)

    tensorboard = TensorBoard(log_dir='logs')
    filepath = '/home/mitchellcatoen/weights.{epoch:02d}-{val_loss:.2f}.hdf5'
    checkpoint = ModelCheckpoint(filepath, verbose=1)
    callbacks = [tensorboard, checkpoint]

    model.fit(dataset_x, dataset_y, epochs=200, batch_size=64, callbacks=callbacks, validation_split=0.1)

if __name__ == '__main__':
    num_games = 100
    main(num_games=num_games)