from game import Game  
from model import AIPlayer

if __name__ == '__main__':

    white_player = AIPlayer("O",1)
    res = 0.0
    res_c = 1

    for i in range(100):
        c = i*1.0/10
        tmp_res = 0.0
        tmp_cnt = 0
        for j in range(100):
            black_player =  AIPlayer("X",c)
            game = Game(black_player, white_player)
            winner, diff = game.run()
            if winner == 0:
                tmp_res += diff
                tmp_cnt += 1
            tmp_res /= tmp_cnt
            if(tmp_res > res):
                res = tmp_res
                res_c = c
    print(c)