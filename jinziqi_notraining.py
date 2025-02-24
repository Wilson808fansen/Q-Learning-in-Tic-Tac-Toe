import pygame
import numpy as np
import random

# 初始化 Pygame
pygame.init()

# 定义屏幕大小和颜色
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
LINE_COLOR = (0, 0, 0)
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)
BG_COLOR = (255, 255, 255)

# 定义井字棋环境
class TicTacToeEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [0] * 9  # 0: empty, 1: X (agent), -1: O (environment)
        self.done = False
        return tuple(self.board)

    def step(self, action):
        if self.board[action] != 0 or self.done:
            return tuple(self.board), -10, True  # 非法动作或游戏已结束
        self.board[action] = 1  # 智能体放置 X
        reward, done = self.check_winner()
        if done:
            return tuple(self.board), reward, done
        # 环境随机放置 O
        empty_cells = [i for i, val in enumerate(self.board) if val == 0]
        o_action = random.choice(empty_cells)
        self.board[o_action] = -1
        reward, done = self.check_winner()
        return tuple(self.board), reward, done

    def check_winner(self):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 行
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 列
            [0, 4, 8], [2, 4, 6]              # 对角线
        ]
        for condition in win_conditions:
            values = [self.board[i] for i in condition]
            if values.count(1) == 3:  # 智能体获胜
                return 10, True
            elif values.count(-1) == 3:  # 玩家获胜
                return -10, True
        if 0 not in self.board:  # 平局
            return 0, True
        return -0.1, False  # 每次移动的惩罚

# 绘制井字棋棋盘
def draw_board(screen, board):
    screen.fill(BG_COLOR)
    # 绘制网格线
    pygame.draw.line(screen, LINE_COLOR, (100, 0), (100, 300), 5)
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 300), 5)
    pygame.draw.line(screen, LINE_COLOR, (0, 100), (300, 100), 5)
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (300, 200), 5)
    # 绘制棋子
    for i, val in enumerate(board):
        row, col = divmod(i, 3)
        x, y = col * 100 + 50, row * 100 + 50
        if val == 1:  # X
            pygame.draw.line(screen, X_COLOR, (x - 40, y - 40), (x + 40, y + 40), 5)
            pygame.draw.line(screen, X_COLOR, (x - 40, y + 40), (x + 40, y - 40), 5)
        elif val == -1:  # O
            pygame.draw.circle(screen, O_COLOR, (x, y), 40, 5)
    pygame.display.flip()

# 主函数
def main():
    # 初始化环境
    env = TicTacToeEnv()

    # 初始化 Pygame 窗口
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tic-Tac-Toe (Untrained Agent)")

    # 游戏主循环
    running = True
    state = env.reset()
    draw_board(screen, state)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not env.done:
                # 获取玩家点击的位置
                x, y = event.pos
                col, row = x // 100, y // 100
                action = row * 3 + col
                # 执行动作
                if state[action] == 0:  # 只有空格才能下棋
                    state, reward, done = env.step(action)
                    draw_board(screen, state)
                    if done:
                        if reward == 10:
                            print("You win!")
                        elif reward == -10:
                            print("You lose!")
                        else:
                            print("It's a draw!")
                        state = env.reset()
                        draw_board(screen, state)
    pygame.quit()

if __name__ == "__main__":
    main()