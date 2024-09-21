from blessed import Terminal
from random import randint

# Initialize Terminal object from blessed for terminal manipulations
term = Terminal()

# Alias for the built-in input function
readLine = input

# Define the range for the target number
TARGET_RANGE = (1, 9)
MAX_ATTEMPTS = None
# Define the exit commands
EXIT = ("exit", "x")
# Define the restart commands
RESTART = ("re", "r")


# Function to clear the terminal screen
def clearTerminal():
    print(term.clear, end="")


# Custom input function that appends a space to the prompt
def input(prompt: str) -> str:
    return readLine(prompt + " ")


# Decorator to validate the user's guess
def processGuess(func):
    def wrapper(self, *args, **kwargs):
        result: str = func(self, *args, **kwargs)
        # Loop until a valid guess is provided or the user decides to exit/restart
        while not validGuess(result):
            if result in EXIT:
                return self.exit()
            elif result in RESTART:
                return self.PromptReplay(continuePlay=True)
            result = func(self, term.red_bold("! "), *args[1:], **kwargs)
        self.guesses += 1
        return int(result)

    return wrapper


# Function to check if the guess is a valid number within the target range
def validGuess(guess: str) -> bool:
    try:
        validity = int(guess) in range(TARGET_RANGE[0], TARGET_RANGE[1] + 1)
    except ValueError:
        return False
    else:
        return validity


class Game:
    def __init__(self) -> None:
        clearTerminal()
        self.targetNumber: int = None
        self.userGuess: int = None
        self.guesses: int = 0
        self.maxAttempts = self.AssignMaxAttempts()
        self.main()

    def main(self):
        self.greet()
        self.targetNumber = self.GetTargetNumber()
        self.play()

    def play(self):
        while not self.CorrectGuess:
            self.userGuess = self.GetUserGuess()
            self.ProvideFeedback()

            if self.CorrectGuess:
                self.DeclareVictory()
                return
            elif self.MaxGuessLimit:
                self.ReachedGuessLimit()
                return

    def greet(self):
        # Display the welcome message and instructions
        print(term.bold_cyan_on_blue("### Welcome To The Guessing Game !! ###"))
        targetRange = " and ".join(map(str, TARGET_RANGE))
        print(
            term.white(
                f"↳ Guess a number between {targetRange} (or enter 'exit' to quit)"
            )
        )

    def AssignMaxAttempts(self) -> int:
        # Assign the maximum number of guesses based on the target range
        if MAX_ATTEMPTS:
            return MAX_ATTEMPTS
        return len(range(*TARGET_RANGE)) + 1

    def GetTargetNumber(self) -> int:
        # Generate a random target number within the defined range
        targetNumber = randint(*TARGET_RANGE)
        print(term.cyan("Target number generated! Ready your guesses~\n"))
        return targetNumber

    @processGuess
    def GetUserGuess(self, prefix: str = "") -> int | str:
        # Prompt the user for a guess and return it
        guesses = term.white(str(self.guesses + 1)) + term.yellow("")
        userGuess = (
            input(prefix + term.yellow_bold(f"[{guesses}] Enter your guess:"))
            .strip()
            .lower()
        )
        return userGuess

    @property
    def MaxGuessLimit(self):
        # Check if the user has reached the maximum number of guesses
        return self.guesses == self.maxAttempts

    @property
    def CorrectGuess(self):
        # Check if the user's guess is correct
        return self.userGuess == self.targetNumber

    def ProvideFeedback(self):
        # Provide feedback to the user based on their guess
        condition = (self.userGuess > self.targetNumber) - (
            self.userGuess < self.targetNumber
        )
        feedback = {
            1: term.bright_red("more than"),
            0: term.bright_green("equal to"),
            -1: term.bright_red("less than"),
        }[condition]

        formatted_feedback = term.white(f"Your guess is {feedback} the target!\n")
        print(formatted_feedback)

    def ReachedGuessLimit(self):
        # Inform the user that they have reached the maximum number of guesses
        print(
            term.bright_red(
                f"\nYou reached the max guesses limit {{{self.maxAttempts}}}! Better luck next time!!"
            )
        )
        print(term.bright_red(f"The target number was: {self.targetNumber}!"))
        self.PromptReplay()

    def DeclareVictory(self):
        # Congratulate the user for guessing correctly
        print(term.bold_green("\n🎉 VICTORY! You guessed correctly!! 🎉"))
        plural = "" if self.guesses == 1 else "es"
        print(term.green_italic(f"Took {self.guesses} guess{plural}."))
        self.PromptReplay()

    def PromptReplay(self, continuePlay=False):
        # Ask the user if they want to replay the game
        if input(term.magenta_bold("Replay? (y/n) [y]:")).lower() in ("y", ""):
            return Game()
        if continuePlay:
            return self.GetUserGuess("\n")
        self.exit()

    def exit(self):
        print(term.bright_blue("\n( ﾉ ﾟｰﾟ)ﾉ bye\n"))
        from sys import exit

        exit()


if __name__ == "__main__":
    Game()
