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

class Model:
    def __init__(self, path='models/weights.44-0.10.hdf5'):
        self.model = make_net((8, 8, 13), 1)
        self.model.load_weights(path)
    
    def inference(self, board, black_or_white):
        board_data = board2array(board, black_or_white)
        output = self.model.predict(np.reshape(board_data, (1, 8, 8, 13)))
        return output

def make_net(inshape, outshape):
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(2, 2), padding='same', activation='relu', input_shape=inshape))
    model.add(Conv2D(32, kernel_size=(2, 2), padding='same', activation='relu'))

    model.add(Conv2D(64, kernel_size=(2, 2), padding='same', activation='relu'))
    model.add(Conv2D(64, kernel_size=(2, 2), padding='same', activation='relu'))

    model.add(Flatten())

    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(512))
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

def inference(board, black_or_white):
    board_data = board2array(board, black_or_white)
    print(board_data)
    model = make_net((8, 8, 13), 1)
    model.load_weights('models/weights.40-0.00.hdf5')
    output = model.predict(np.reshape(board_data, (1, 8, 8, 13)))
    print(output)

def train(num_games=1000):
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

def print_bw_and_board(black_or_white, board):
    print(board)
    if black_or_white:
        print("White plays")
        return
    print("Black plays")

if __name__ == '__main__':
    num_games = 100
    pgn = open("data/fisc.pgn")
    game = chess.pgn.read_game(pgn) 
    model = Model()
    board = game.board()
    bw = True

    for move in game.mainline_moves():
        print_bw_and_board(bw, board)
        print(model.inference(board, bw))
        bw = not bw
        board.push(move)

    