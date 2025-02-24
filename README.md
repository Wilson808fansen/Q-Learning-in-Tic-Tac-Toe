Introduction
Reinforcement Learning (RL) is a machine learning approach whose goal is to train an agent to perform a specific task by interacting with an environment. The core idea of Reinforcement Learning is to allow the agent to learn how to take action to maximise cumulative reward through trial and error. We are using this technique for human-computer interaction in Tic-Tac-Toe. The goal is to enable the agent to fully understand the rules of chess, apply them, and become a Tic-Tac-Toe master!
This statement outlines the iterative development process, evaluates the agent's performance, and discusses the results.

Problem Statement
Tic-Tac-Toe is a classic two-player game played on a 3x3 grid. The objective is to align three of your symbols (X or O) in a row, column, or diagonal while preventing your opponent from doing the same. While simple for humans to master, teaching an agent to play optimally requires careful design of the environment, reward function, and learning algorithm.

Our challenge was to:
1.Design a Tic-Tac-Toe environment that supports both human and AI players.
2.Implement a Q-Learning algorithm to regulate incentives and train intelligences to play chess in an optimal way.
3.Visualize the game using Pygame to allow human interaction with the trained agent rather than in a terminal window.
4.Evaluate the agent's performance before and after training.
