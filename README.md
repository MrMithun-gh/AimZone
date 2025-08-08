Aim Trainer
A fast-paced reflex and accuracy training game built with Pygame. Test your clicking speed and precision as targets appear and shrink, all while trying to beat your personal best score.

Features
Dynamic Targets: Targets appear at random locations and grow, then shrink. Click them before they disappear to score points.

Game State Management: The game includes a dedicated start screen and a comprehensive end screen.

High Score Tracking: Your personal best score is saved to a local highscore.txt file, allowing you to compete against your own records across multiple sessions.

Interactive UI: Modern and minimalist design with responsive buttons for "Start Game," "Play Again," and "Exit."

In-Game Statistics: Track your progress in real-time with an overlay displaying your time, hits, and current lives.

How to Play
The objective is simple: click on the targets as quickly as possible. You have 3 lives. A target is missed if it disappears before you can click it. The game ends when you lose all your lives.

How to Run
This game requires Python and the Pygame library.

Install Pygame: If you don't already have it, install Pygame using pip:

pip install pygame

Run the Game: Save the Python code as a file (e.g., main.py) and run it from your terminal:

python main.py

High Score: The game will automatically create a file named highscore.txt in the same directory to save your personal best.

Code Structure
The main script handles all game logic, including the different game states (START_SCREEN, GAME_LOOP, END_SCREEN), button interactions, and the core game mechanics. The highscore.txt file is used to persist data between sessions.
