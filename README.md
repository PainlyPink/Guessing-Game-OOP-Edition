

**Guessing Game**
================

**Get Started Quickly**
--------------------

Download the pre-built executable from the `dist` directory and start playing right away!

* [Download Executable (from latest release)](https://github.com/ElektrikFire/Guessing-Game-OOP-Edition/releases/latest/download/Guessing_Game.exe)
A simple number guessing game written in Python using the Blessed library for terminal manipulation.

**Game Overview**
---------------

The game generates a random target number within a defined range, and the player has to guess the number. After each guess, the game provides feedback to help the player narrow down the range.

**Features**
------------

* Randomly generated target number within a defined range
* Feedback after each guess to help the player
* Limited number of guesses (configurable)
* Option to replay the game after winning or losing
* Colorful and interactive terminal interface using Blessed

**Requirements**
---------------

* Python 3.x
* Blessed library (`pip install blessed`)

**Installation**
------------

1. Clone the repository: `git clone https://github.com/ElektrikFire/Guessing-Game-OOP-Edition.git`
2. Install the required library: `pip install blessed`
3. Run the game:
	* `python main.py`
	* Alternatively: `run_python.bat main.py`

**Usage**
-----

1. Run the game by executing `python main.py` in your terminal.
2. Follow the on-screen instructions to play the game.
3. Guess a number within the given range.
4. The game will provide feedback after each guess.
5. Keep guessing until you win or run out of attempts.

**Configuration**
-------------

* The target number range can be configured by modifying the `TARGET_RANGE` variable in `main.py`.
* The maximum number of guesses can be configured by modifying the `MAX_ATTEMPTS` variable in `main.py`.

**License**
-------

This project is licensed under the MIT License. See `LICENSE` for details.

**Contributing**
------------

Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request.

**Acknowledgments**
---------------

* The Blessed library for providing an easy-to-use terminal manipulation API.
* The Python community for providing a vast array of resources and libraries.
