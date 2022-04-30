# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import math

import numpy as np  # 提供维度数组与矩阵运算
import copy  # 从copy模块导入深度拷贝方法
from board import Chessboard


# 基于棋盘类，设计搜索策略
class Game:
    def __init__(self, show=True):
        """
        初始化游戏状态.
        """

        self.chessBoard = Chessboard(show)
        self.solves = []
        self.gameInit()

    # 重置游戏
    def gameInit(self, show=True):
        """
        重置棋盘.
        """

        self.Queen_setRow = [-1] * 8
        self.chessBoard.boardInit(False)

    def test(self,x,y,tmp=[]):
        for i,j in enumerate(tmp):
            if math.fabs(i-x) == 0 or math.fabs(j-y) == 0 or math.fabs(i-x) == math.fabs(j - y):
                return False
        return True

    def findSolution(self, row, tmp=[]):
        if np.size(tmp) == 8:
            self.solves.append(np.array(tmp).tolist())
            print(tmp)
        else:
            for i in range(8):
                if self.test(row, i, tmp):
                    tmp.append(i)
                    self.findSolution(row + 1, tmp)
                    tmp.remove(i)

    def run(self, row=0):
        self.findSolution(0,[])

    def showResults(self, result):
        """
        结果展示.
        """

        self.chessBoard.boardInit(False)
        for i, item in enumerate(result):
            if item >= 0:
                self.chessBoard.setQueen(i, item, False)

        self.chessBoard.printChessboard(False)

    def get_results(self):
        """
        输出结果(请勿修改此函数).
        return: 八皇后的序列解的list.
        """

        self.run()
        return self.solves

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    game = Game()
    solutions = game.get_results()
    print('There are {} results.'.format(len(solutions)))
    print(solutions)

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
