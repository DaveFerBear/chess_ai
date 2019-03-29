import core
import chess

if __name__ == '__main__':
    num_games = 100
    model = core.Model()
    bw = True
    board = chess.Board()
    print(board)

    while not board.is_checkmate():
        valid_moves = board.generate_legal_moves()
        if bw:
            best_score = 0
        else:
            best_score = 1
        best_move = None

        for move in valid_moves:
            board.push(move)
            next_moves = board.generate_legal_moves()

            score = model.inference(board, bw)
            # print(score, move)
            if bw and score > best_score:
                best_score = score
                best_move = move
            elif not bw and score < best_score:
                best_score = score
                best_move = move
    
            board.pop()
        
        bw = not bw
        board.push(best_move)
        print(board, best_score)
        print(best_move)
        input(' ')
        # break
