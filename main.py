from yahtzee import *
import random, time

class GameState:
    """Class for the game with the main game loop function, we can set random seeding"""
    def __init__(self, seed=None):
        #so we can set seeds for testing, its a public attribute so we can print it out easily in the main function
        #if we decide to keep different dice or score a different inbetween tests with the same seed, the numbers will be off
        #the seed only determines were we start in a sequence of determined random numbers, by calling different random methods
        #inbetween tests we are moving forward or backwards differently in that sequence
        if seed is None:
            self.seed = int(time.time())
        else:
            self.seed = seed
        random.seed(self.seed)

        #private attributes, only need to be accessed by the class itself
        self._card = create_empty_scorecard() #creating the scorecard
        self._used = [] #initalizing the used scoring options as a list

    def loop(self):
        for i in range(13):
            print(f"Round {i+1}")
            dice = play_round(self._card)
            print(f"Dice: {dice}")
            scores = evaluate(dice)

            option, score = choose(scores, self._used)
            self._card[option] = score
            display_scorecard(self._card)
            print("\n--------------------------\n")

        print("\n--------------------------")
        print("\n--------------------------")
        print("\nFinal Score:\n")
        display_scorecard(self._card)


if __name__ == "__main__":
    game = GameState()
    print(f"\n   Random Seed for current game: {game.seed}\n")
    game.loop()