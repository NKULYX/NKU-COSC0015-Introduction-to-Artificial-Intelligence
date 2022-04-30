import copy
import datetime
import random
import cmath

class Node:
    def __init__(self, chess, parent):
        self.chess = chess
        self.times = 0
        self.score = 0
        self.parent = parent
        self.next_nodes = []
        self.un_visited_nodes = []

    def UCB1(self, c = 1):
        if(self.times==0 or self.parent.times==0):
            return 0
        return self.score/self.times + c*(cmath.sqrt(2*cmath.log(self.parent.times)/self.times).real)
        
    
class AIPlayer:
    """
    AI 玩家
    """

    def __init__(self, color, c):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """

        self.color = color
        self.root = Node((-1, -1), None)    #根节点棋子位置
        self.cur_color = color              #记录在选择过程所用颜色
        self.simColor = ""                  #标记在模拟过程所用颜色
        self.c = c

    
    def changeColor(self, myColor):
        if(myColor=="O"):
            return "X"
        else:
            return "O"

    def game_over(self, board):
        b_list = list(board.get_legal_actions('X'))
        w_list = list(board.get_legal_actions('O'))
        is_over = len(b_list) == 0 and len(w_list) == 0 
        return is_over
    
    def SelectPolicy(self, board):
        curNode = self.root
        while(True):
            # 如果游戏结束了，则直接返回当前这个节点
            if(self.game_over(board)):
                return curNode
            # 如果还有未扩展过的节点
            if(len(curNode.un_visited_nodes)>0):
                # 随机扩展一个节点
                action = curNode.un_visited_nodes.pop(random.randint(0, len(curNode.un_visited_nodes)-1))
                curNode.next_nodes.append(Node(action, curNode))
                # 下棋并更新棋盘信息
                board._move(action, self.cur_color)
                self.cur_color = self.changeColor(self.cur_color)
                # 获取新扩展节点的后继节点，并加入到未扩展的列表中
                curNode.next_nodes[-1].un_visited_nodes = list(board.get_legal_actions(self.cur_color))
                # 返回拓展节点准备进行模拟
                return curNode.next_nodes[-1]
            # 如果所有的节点都扩展过了，则根据UCB1选择节点
            else:
                temp = None
                score = -1e9
                for node in curNode.next_nodes:
                    curScore = node.UCB1(self.c)
                    if(curScore>score):
                        score = curScore
                        temp = node
                # 如果没有选择出来的节点则跳步
                if(temp==None):
                    # 无棋可走，添加一个占位节点
                    curNode.next_nodes.append(Node((-1, -1), curNode))
                    temp = curNode.next_nodes[0]
                    # 更换颜色继续搜索节点
                    curNode.next_nodes[0].un_visited_nodes = list(board.get_legal_actions(self.changeColor(self.cur_color)))
                # 如果选择的不是一个占位节点，则说明有棋可下
                elif(temp.chess != (-1, -1)):
                    board._move(temp.chess, self.cur_color)
                #至此，已经向下找到最优路径temp并完成落子
                self.cur_color = self.changeColor(self.cur_color)#反色
                curNode = temp
    
    def SimulatePolicy(self, board):
        # 当游戏还未结束的时候，模拟玩家的下棋
        while(not self.game_over(board)):
            action_list = list(board.get_legal_actions(self.simColor))
            # 如果有棋可下，则下棋
            if(len(action_list)!=0):
                action = random.choice(action_list)
                board._move(action, self.simColor)
            # 无论是否有棋可下都需要反转颜色
            self.simColor = self.changeColor(self.simColor)
        # 获取获胜方和获胜子数
        winner,win_score = board.get_winner()
        if(winner==0):
            return "X",win_score
        elif(winner==1):
            return "O",win_score
        else:
            return "-",win_score

    def BackPropagate(self, node, winner, win_score):
        if(node == None):#递归终点
            return
        if(self.cur_color==winner):
            node.score -= win_score
        elif(self.changeColor(self.cur_color)==winner):
            node.score += win_score
        node.times+=1
        self.cur_color = self.changeColor(self.cur_color)
        self.BackPropagate(node.parent, winner, win_score)

    def UCTSearch(self, board):
        startTime = datetime.datetime.now()
        self.root = Node((-1, -1), None)
        self.root.un_visited_nodes = list(board.get_legal_actions(self.color))#初始化可能状态
        while((datetime.datetime.now() - startTime).seconds < 50):
            newBoard = copy.deepcopy(board)
            self.cur_color = copy.deepcopy(self.color)
            startNode = self.SelectPolicy(newBoard)
            self.simColor = copy.deepcopy(self.cur_color)
            winner,win_score = self.SimulatePolicy(newBoard)
            self.BackPropagate(startNode, winner, win_score)
            # 判断是否有多次重复访问的点
            flag = False
            for node in self.root.next_nodes:
                if node.times > 1000:
                    flag = True
                    break
            if flag:
                break
        temp = None
        score = -1e9
        for node in self.root.next_nodes:
            curScore = node.UCB1(self.c)
            if(curScore>score):
                score = curScore
                temp = node
        if(node==None):
            pass
        return temp.chess

    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        # print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))

        # -----------------请实现你的算法代码--------------------------------------
        action = self.UCTSearch(board)
        # ------------------------------------------------------------------------

        return action