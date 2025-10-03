import random

roll_dice = lambda dice_amount: [random.randint(1,6) for i in range(dice_amount)]
roll_dice.__doc__ = "Rolls x amount of dice"

def create_empty_scorecard():
    """Returns empty yahtzee scoreboard"""
    keys = ["1", "2", "3", "4", "5", "6", "three_of_a_kind",
            "four_of_a_kind", "full_house", "four_straight",
            "five_straight", "yahtzee", "chance"]
    return {val : None for val in keys} #all key values are initialized as None before the game has started 

def helper_freq_dict_for_list(dice_roll):
    """Helper function to turn dice roll (list) into a dictionary with the frequencies of each roll"""
    list_frequency = {}
    for element in dice_roll:
        if element in list_frequency:
            list_frequency[element] += 1
        else:
            list_frequency[element] = 1
    return list_frequency

def select_keep(dice_roll):
    """Returns the dice that will NOT be re-rolled according to the request of the user"""
    user_input = input("Select which dice you would like to keep(ex: 332, 641, [no spaces]): ")

    if user_input == "": #if the user wants to reroll all the dice
        return []
    
    if not (user_input.isdigit() and all(int(char) in dice_roll for char in user_input)): #input must be composed strictly of digits and those digits must exist in the dice roll
        print("Invalid input: digits only and no spaces, and said digits must exist in the dice roll")
        return select_keep(dice_roll)
        
    user_input = [int(char) for char in user_input]

    dice_roll_frequency = helper_freq_dict_for_list(dice_roll) #using helper function to turn dice roll list into a frequency table
    user_input_frequency = helper_freq_dict_for_list(user_input) #*** 
        
    for digit, frequency in user_input_frequency.items(): #if the frequency of the user input for a given number (1-6) is higher than the frequency of the dice roll it's an invalid input
        if frequency > dice_roll_frequency[digit]:
            print("Invalid input: select a valid choice")
            return select_keep(dice_roll)   
    return user_input  

reroll = lambda dice, kept: roll_dice(len(dice) - len(kept)) + kept
reroll.__doc__ = """Rerolls the dice that were not kept and returns the new dice roll(rerolled + kept)"""

def has_straight(dice, length):
    """Checks if there is a straight of k length in a given dice roll"""
    ordered_dice = sorted(set(dice)) #we convert dice to a set and then an ordered list because 1) it is an ordered data structure, easier to find a sequence 2) duplicates are of no importance in straights
    
    if len(dice)<length: #straights of k=length can only exist if the amount of non duplicate numbers is >= k
        return False
    
    longest_seq=1

    for i in range(1, len(ordered_dice)):
        if ordered_dice[i] == ordered_dice[i-1] + 1:
            longest_seq += 1
            if longest_seq == length:
                return True
        else:
            longest_seq = 1
    return False

def evaluate(dice):
    """Calculate all possible scores given a dice roll"""

    score_dictionary = {} #where all possible scores are appended
    dice_roll_frequency = helper_freq_dict_for_list(dice) #frequency of all digits in the dice roll

    #sum all the digits individually in the dice_roll
    for digit in range(1, 7):
        if digit in dice_roll_frequency:
            score_dictionary[str(digit)] = dice_roll_frequency[digit] * digit
        else:
            score_dictionary[str(digit)] = 0

    #three of a kind, four of a kind 
    if any(freq >= 3 for freq in dice_roll_frequency.values()):
        score_dictionary["three_of_a_kind"] = sum(dice)
    else:
        score_dictionary["three_of_a_kind"] = 0

    if any(freq >= 4 for freq in dice_roll_frequency.values()):
        score_dictionary["four_of_a_kind"] = sum(dice)
    else:
        score_dictionary["four_of_a_kind"] = 0

    #full house
    if len(dice_roll_frequency.keys()) == 2 and sorted(dice_roll_frequency.values()) == [2, 3]: #if we sort them we dont have to iterate over them 2 times 
        score_dictionary["full_house"] = 25
    else:
        score_dictionary["full_house"] = 0
    
    #four_straight, five_straight
    if has_straight(dice, 5):
        score_dictionary["four_straight"] = 30
        score_dictionary["five_straight"] = 40
    else:
        score_dictionary["five_straight"] = 0
        if has_straight(dice, 4):
            score_dictionary["four_straight"] = 30
        else:
            score_dictionary["four_straight"] = 0
    
    #yahtzee
    if len(dice_roll_frequency.keys()) == 1:
        score_dictionary["yahtzee"] = 50
    else:
        score_dictionary["yahtzee"] = 0
    
    #chance
    score_dictionary["chance"] = sum(dice)

    return score_dictionary

def choose(scores, used):
    """Filters all possible scoring options by comparing the score possibilities of the round that have not been used previously and returns the chose option and respective score"""

    non_null_scores = {option: score for option, score in scores.items() if score != 0} #filter out all scoring options which equal zero
    valid_options = {option: score for option, score in non_null_scores.items() if option not in used} #filter out all previously used scoring options

    #Extra logic for if there are no scoring options left, must pick one and fill it with a 0
    if not valid_options:
        print(f"\nNo valid scoring options. Pick one to 0 out:")
        valid_options = {option: 0 for option, score in scores.items() if option not in used}
    else:
        print("\nAll Scoring options:")

    #in order to make the process easier through indexing we convert the dictionary of valid options into a typecasted list of items
    valid_options_indexed = list(valid_options.items())
    
    for i, option_score in enumerate(valid_options_indexed):
        print(f"{i+1})  [{option_score[0]}: {option_score[1]} points]\n")

    user_input = input("Type in your scoring option NUMBER(ex. 2, 3, 7): ")
    if not user_input.isdigit():
        print("Enter a VALID scoring option.")
        return choose(scores, used)
    
    if int(user_input) not in range(1, len(valid_options_indexed)+1):
        print("Enter a VALID scoring option.")
        return choose(scores, used)

    option, score = valid_options_indexed[int(user_input)-1]
    used.append(option)

    return option, score 

def display_scorecard(card):
    """Prints out the scoreboard"""
    print("\n")
    print("Scorecard :")
    print("--------------------------\n")

    for option, score in card.items():
        print(f"{option}: {score} points")
    

    #upper score
    upper_options = [str(i) for i in range(1,7)]
    upper_sum = sum(card[option] for option in upper_options if card[option] is not None)
    print(f"\nUpper Section Total: {upper_sum} points")

    #bonus
    bonus = 0
    if upper_sum >= 63:
        bonus = 35
    print(f"\nBonus: {bonus} points")

    #total score
    total_score = sum(score for score in card.values() if score is not None) + bonus
    print(f"\nTotal Score: {total_score}  points")  

def play_round(card):
    """Play a round of yahtzee with the previously defined functions"""
    print("\nRound Start!\n")

    dice = roll_dice(5) #Up to 3 dice throws
    for i in range(2): 
        print(f"\nDice: {dice}")
        kept = select_keep(dice)
        dice = reroll(dice, kept)

    return dice

