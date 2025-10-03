from yahtzee import *

def main():
    card = create_empty_scorecard() #creating the scorecard
    used = [] #initalizing the used scoring options as a list

    for i in range(13):
        dice = play_round(card)

        scores = evaluate(dice)

        option, score = choose(scores, used)
        card[option] = score
        display_scorecard(card)

    print("\nFinal Score: ")
    display_scorecard(card)

if __name__ == "__main__":
    main()