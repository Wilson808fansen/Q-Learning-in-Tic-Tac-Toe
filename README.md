import pygame
import numpy as np
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
LINE_COLOR = (0, 0, 0)
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)
BG_COLOR = (255, 255, 255)

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
        empty_cells = [i for i, val in enumerate(self.board) if val == 0]
        if empty_cells:
            o_action = self.get_best_defensive_move(empty_cells)
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
            return -5, True
        return -0.1, False  # 每次移动的惩罚

    def get_best_defensive_move(self, empty_cells):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 行
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 列
            [0, 4, 8], [2, 4, 6]              # 对角线
        ]
        for condition in win_conditions:
            values = [self.board[i] for i in condition]
            if values.count(-1) == 2 and values.count(0) == 1:  # 玩家即将获胜
                return condition[values.index(0)]
        for condition in win_conditions:
            values = [self.board[i] for i in condition]
            if values.count(1) == 2 and values.count(0) == 1:  # 智能体即将获胜
                return condition[values.index(0)]
        strategic_positions = [4, 0, 2, 6, 8]  # 中心和角落优先
        for pos in strategic_positions:
            if pos in empty_cells:
                return pos
        return random.choice(empty_cells)

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.01):
        self.q_table = {}
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)  # 探索
        q_values = [self.get_q_value(state, a) for a in self.actions]
        max_q = max(q_values)
        best_actions = [a for a, q in zip(self.actions, q_values) if q == max_q]
        return random.choice(best_actions)  # 利用

    def learn(self, state, action, reward, next_state):
        old_q = self.get_q_value(state, action)
        next_max_q = max([self.get_q_value(next_state, a) for a in self.actions])
        new_q = old_q + self.alpha * (reward + self.gamma * next_max_q - old_q)
        self.q_table[(state, action)] = new_q

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

def draw_board(screen, board):
    screen.fill(BG_COLOR)

    pygame.draw.line(screen, LINE_COLOR, (100, 0), (100, 300), 5)
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 300), 5)
    pygame.draw.line(screen, LINE_COLOR, (0, 100), (300, 100), 5)
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (300, 200), 5)

    for i, val in enumerate(board):
        row, col = divmod(i, 3)
        x, y = col * 100 + 50, row * 100 + 50
        if val == 1:  # X
            pygame.draw.line(screen, X_COLOR, (x - 40, y - 40), (x + 40, y + 40), 5)
            pygame.draw.line(screen, X_COLOR, (x - 40, y + 40), (x + 40, y - 40), 5)
        elif val == -1:  # O
            pygame.draw.circle(screen, O_COLOR, (x, y), 40, 5)
    pygame.display.flip()

def train_agent(env, agent, episodes=20000):
    for episode in range(episodes):
        state = env.reset()
        done = False
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state)
            state = next_state
        agent.decay_epsilon()

def main():
    env = TicTacToeEnv()
    agent = QLearningAgent(actions=list(range(9)))

    print("Training the agent...")
    train_agent(env, agent, episodes=20000)
    print("Training complete!")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tic-Tac-Toe with Q-Learning")

    running = True
    state = env.reset()
    draw_board(screen, state)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not env.done:
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
