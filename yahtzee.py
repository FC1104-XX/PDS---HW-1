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
    print(f"Dice roll: {dice_roll}")
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
    for digit in range(1, len(dice)):
        if digit in dice_roll_frequency:
            score_dictionary[str(digit)] = dice_roll_frequency[digit] * digit
        else:
            score_dictionary[str(digit)] = 0

    #three of a kind, four of a kind 
    #ACHO QUE ISTO TÁ MAL
    for digit in dice_roll_frequency:
        if dice_roll_frequency[digit] >= 3:
            score_dictionary["three_of_a_kind"] = sum(dice)
        else:
            score_dictionary["three_of_a_kind"] = 0

        if dice_roll_frequency[digit] >= 4:
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





if __name__ == "__main__":
    print(roll_dice.__doc__)
    print(roll_dice(5))
    print(create_empty_scorecard.__doc__)
    print(create_empty_scorecard())
    print(helper_freq_dict_for_list.__doc__)
    print(helper_freq_dict_for_list([5, 5, 5, 2, 1, 2, 9, 8, 1, 1, 0, 6, 9]))
    print(select_keep.__doc__)
    x=roll_dice(5)
    selected = select_keep(x)
    print(selected)
    print(reroll.__doc__)
    y=reroll(x, selected)
    print(y)
    print(has_straight.__doc__)
    print(has_straight([1,2,3,4],4))
    x=[2, 3, 3, 5, 6]
    print(x)
    print(evaluate(x))
    x=[1, 1, 1, 1, 1]
    print(x)
    print(evaluate(x))
    x=[2, 3, 3, 5, 6]
    print(x)
    print(evaluate(x))
    x=[2, 2, 2, 2, 5]
    print(x)
    print(evaluate(x))