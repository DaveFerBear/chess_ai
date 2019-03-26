import pickle

class PST:
    def randomize_pst(pst, randomness):
        new_pst = {}
        for piece,table in pst.items():
            new_pst[piece] = []
            for square in range(len(table)):
                new_pst[piece].append(table[square] + round(triangular(-1*randomness,randomness,0)))
            new_pst[piece] = tuple(new_pst[piece])
        return new_pst

    def randomize_piece(piece, randomness):
        new_piece = {}
        for letter,value in piece.items():
            new_piece[letter] = value + round(triangular(-1*randomness,randomness,0))
        return new_piece

    def generate_pst_padded(pst, piece):
        new_pst = {}
        for k,table in pst.items():
            padrow = lambda row: (0,) + tuple(x+piece[k] for x in row) + (0,)
            new_pst[k] = sum((padrow(table[i*8:i*8+8]) for i in range(8)), ())
            new_pst[k] = (0,)*20 + new_pst[k] + (0,)*20
        return new_pst
        

    def save_data(pst, piece, prefix):
        f = open('Genetic/Store/' + prefix + '_pst.pckl', 'wb')
        pickle.dump(pst, f)
        f.close()
        f = open('Genetic/Store/' + prefix + '_piece.pckl', 'wb')
        pickle.dump(piece, f)
        f.close()

    def load_data(prefix):
        f = open('Genetic/Store/' + prefix + '_pst.pckl', 'rb')
        pst = pickle.load(f)
        f.close()
        f = open('Genetic/Store/' + prefix + '_piece.pckl', 'rb')
        piece = pickle.load(f)
        f.close()
        return pst, piece

def main():
    pass

if __name__ == '__main__':
    main()