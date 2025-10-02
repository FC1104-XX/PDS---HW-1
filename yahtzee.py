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
    for char in user_input:
        if int(char) not in dice_roll: #input be composed strictly of digits that exist in the dice roll
            print("Invalid input: digits only and no spaces")
            return select_keep(dice_roll)
    user_input = [int(char) for char in user_input]

    dice_roll_frequency = helper_freq_dict_for_list(dice_roll) #using helper function to turn dice roll list into a frequency table
    user_input_frequency = helper_freq_dict_for_list(user_input) #*** 
    
    for digit, frequency in user_input_frequency.items():
        if frequency > dice_roll_frequency[digit]:
            print("Invalid input: select a valid choice")
            return select_keep(dice_roll)
    return user_input  
    
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
