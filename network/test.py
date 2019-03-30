import core
import chess
import sys

if __name__ == '__main__':
    num_games = 100
    model = core.Model()
    bw = True
    board = chess.Board()

    while not board.is_checkmate():
        print(board)
        legal_moves = board.generate_legal_moves()
        while(True):
            try:
                m = input('Move: ')
                m = chess.Move.from_uci(m)
                if m in legal_moves:
                    board.push(m)
                else:
                    continue
                break
            except Exception as E:
                print(E)
                continue

        bw = not bw


        valid_moves = board.generate_legal_moves()
        if bw:
            best_score = 0
        else:
            best_score = 1
        best_move = None

        bw = not bw
        for move in valid_moves:
            board.push(move)
            next_moves = board.generate_legal_moves()

            score = model.inference(board, bw)
            # print(score, move)
            if bw and score < best_score:
                best_score = score
                best_move = move
            elif not bw and score > best_score:
                best_score = score
                best_move = move
    
            board.pop()

        board.push(best_move)
        print(board, best_score)

        
        

