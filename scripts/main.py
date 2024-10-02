from secrets import randbelow
from typing import Callable, Optional

from blessed import Terminal

# Initialize Terminal object from blessed for terminal manipulations
_term = Terminal()

# Define the range for the target number
TARGET_RANGE = (1, 9)
MAX_ATTEMPTS: Optional[int] = None  # Allow for None or int
# Define the exit commands
EXIT_COMMANDS = ("exit", "x")
# Define the restart commands
RESTART_COMMANDS = ("re", "r")


# Function to clear the terminal screen
def clear_terminal() -> None:
    """Clear the terminal screen."""
    print(_term.clear, end="")


# Function to check if the guess is a valid number within the target range
def valid_guess(guess: str) -> bool:
    """Check if the guess is a valid number within the target range."""
    try:
        validity = int(guess) in range(TARGET_RANGE[0], TARGET_RANGE[1] + 1)
    except ValueError:
        return False
    else:
        return validity


# Decorator to validate the user's guess
def process_guess(func: Callable[["Game", str], str]) -> Callable[["Game", str], int]:
    """Decorator to validate the user's guess."""

    def wrapper(self: "Game", *args: str, **kwargs: str) -> int:
        """Wrapper function to check if the guess is valid and process it."""
        while True:
            result: str = func(self, *args, **kwargs)
            if valid_guess(result):
                self.guesses += 1
                return int(result)
            if result in EXIT_COMMANDS:
                self.exit()
            if result in RESTART_COMMANDS:
                self.prompt_replay(continue_play=True)
                return 0
            print(_term.red_bold("! Invalid input. Try again!"))

    return wrapper


class Game:
    def __init__(self) -> None:
        """Initialize the game."""
        clear_terminal()
        self.guesses: int = 0
        self.max_attempts: int = self.assign_max_attempts()
        self.target_number: int = self.get_target_number()
        self.main()

    def main(self) -> None:
        """Main game loop."""
        self.greet()
        self.play()

    def play(self) -> None:
        """Play the game."""
        self.user_guess = self.get_user_guess("")
        while not self.correct_guess:
            self.user_guess = self.get_user_guess("")
            self.provide_feedback()

            if self.correct_guess:
                self.declare_victory()
                return
            if self.max_guess_limit:
                self.reached_guess_limit()
                return

    def greet(self) -> None:
        """Display the welcome message and instructions."""
        print(_term.bold_cyan_on_blue("### Welcome To The Guessing Game !! ###"))
        target_range = " and ".join(map(str, TARGET_RANGE))
        print(
            _term.white(
                f"  Guess a number between {target_range} (or enter 'exit' to quit)"
            )
        )

    def assign_max_attempts(self) -> int:
        """Assign the maximum number of guesses based on the target range."""
        if MAX_ATTEMPTS:
            return MAX_ATTEMPTS
        return len(range(*TARGET_RANGE)) + 1

    def get_target_number(self) -> int:
        """Generate a random target number within the defined range."""
        target_number = (
            randbelow(TARGET_RANGE[1] - TARGET_RANGE[0] + 1) + TARGET_RANGE[0]
        )
        print(_term.cyan("Target number generated! Ready your guesses~\n"))
        return target_number

    @process_guess
    def get_user_guess(self, prefix: str = "") -> str:
        """Prompt the user for a guess and return it."""
        guesses = _term.white(str(self.guesses + 1))
        user_guess = input(
            prefix + _term.yellow_bold(f"[{guesses}] Enter your guess: ")
        )
        return user_guess

    @property
    def max_guess_limit(self) -> bool:
        """Check if the user has reached the maximum number of guesses."""
        return self.guesses >= self.max_attempts

    @property
    def correct_guess(self) -> bool:
        """Check if the user's guess is correct."""
        return self.user_guess == self.target_number

    def provide_feedback(self) -> None:
        """Provide feedback to the user based on their guess."""
        condition = (self.user_guess > self.target_number) - (
            self.user_guess < self.target_number
        )
        feedback = {
            1: _term.bright_red("more than"),
            0: _term.bright_green("equal to"),
            -1: _term.bright_red("less than"),
        }[condition]

        formatted_feedback = _term.white(f"Your guess is {feedback} the target!\n")
        print(formatted_feedback)

    def reached_guess_limit(self) -> None:
        """Inform the user that they have reached the maximum number of guesses."""
        print(
            _term.bright_red(
                f"\nYou reached the max guesses limit ({self.max_attempts})!"
            )
        )
        print(_term.bright_red(f"The target number was: {self.target_number}!"))
        self.prompt_replay()

    def declare_victory(self) -> None:
        """Congratulate the user for guessing correctly."""
        print(_term.bold_green("\n VICTORY! You guessed correctly!! "))
        plural = "" if self.guesses == 1 else "es"
        print(_term.green_italic(f"Took {self.guesses} guess{plural}."))
        self.prompt_replay()

    def prompt_replay(self, continue_play: bool = False) -> Optional["Game"]:
        """Ask the user if they want to replay the game."""
        if input(_term.magenta_bold("Replay? (y/n) [y]: ")).lower() in ("y", ""):
            return Game()
        if continue_play:
            self.get_user_guess("\n")
            return None
        self.exit()
        return None

    def exit(self) -> None:
        """Exit the game."""
        print(_term.bright_blue("\n( ﾉ ﾟｰﾟ)ﾉ bye\n"))
        from sys import exit

        exit()


if __name__ == "__main__":
    Game()
