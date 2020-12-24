# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string
from copy import deepcopy

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

word: string
n: int >= 0
returns: int >= 0
"""
    words_lst = list(word.lower())
    first_component = sum(list(map(lambda x: SCRABBLE_LETTER_VALUES[x], words_lst)))
    second_component = max(1, 7 * len(words_lst) - 3 * (n - len(words_lst)))
    return first_component * second_component

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    print("Current hand: ", end="")
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')
    print()

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    hand_copy = hand.copy()
    for letter in word:
        try:
            hand_copy[letter.lower()] -= 1
            if hand_copy[letter.lower()] == 0:
                del hand_copy[letter.lower()]
        except:
            pass

    return hand_copy

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    test = True
    word1 = word.lower()
    checked_letters = []
    hand_letters = [letter for letter in hand.keys()]

    if "*" in word1:
        position = []
        for letter in range(len(word1)):
            if word1[letter] == "*":
                position.append(letter)
        if len(position) >= 2:
            test = False
        else:
            pos = position[0]
            test = False
            for var_vow in VOWELS:
                word2 = word1[:pos] + var_vow + word1[pos + 1:]
                hand1 = deepcopy(hand)
                hand1[var_vow] = hand1.get(var_vow, 0) + 1
                if is_valid_word(word2, hand1, word_list):
                    return True

    if word1 not in word_list:
        test = False

    if test:
        for letter_in_word in word1:
            if letter_in_word not in checked_letters:
                if letter_in_word in hand_letters:
                    counter = 0
                    for letter in word1:
                        if letter == letter_in_word:
                            counter += 1
                    if hand[letter_in_word] - counter < 0:
                        test = False
                    checked_letters.append(letter_in_word)
                else:
                    test = False
            if not test:
                break
    return test

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    return sum(hand.values())
    
    pass  # TO DO... Remove this line when you implement this function

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    
        # Display the hand
        
        # Ask user for input
        
        # If the input is two exclamation points:
        
            # End the game (break out of the loop)

            
        # Otherwise (the input is not two exclamation points):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            # update the user's hand by removing the letters of their inputted word
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function

    total_score = 0
    while True:
        print("\nCurrent hand: ", end="")
        display_hand(hand)
        word = input("Enter word, or “!!” to indicate that you are finished:  ")

        if word == "!!":
            break
        elif is_valid_word(word, hand, word_list):
            score_on_this_step = get_word_score(word, calculate_handlen(hand))
            total_score += score_on_this_step
            print("\"{0}\" earned {1} points. Total: {2} points".format(word, score_on_this_step, total_score))
            hand = update_hand(hand, word)
        else:
            hand = update_hand(hand, word)
            print("\nThis is not a valid word. Please choose another word.")

        if hand == {}:
            print("\nRan out of letters. Total score: {0} points \n----------------------------".format(total_score))
            break
    return total_score

#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    new_letter = letter
    while new_letter in [letters for letters in hand.keys()]:
        new_letter = random.choice(VOWELS + CONSONANTS)
    hand[new_letter] = hand[letter]
    del hand[letter]
    return hand







def ask_for_num_of_hands():
    """Ask player for number of hands player want to play
    Returns:
        integer: number of hands
    """
    try:
        # Ask player for number
        num = int(input("Enter total number of hands: "))
        if num < 1:
            raise ValueError
        # If it`s positive integer - return it
        return num
    except ValueError:
        # If it`s not positive integer - don`t return it
        print("Incorrect input. Please, enter positive integer")
        # And ask again
        return ask_for_num_of_hands()

def ask_substitution_letter():
    """Ask player if substitution of letter if wanted, and asks letter if so.
    Returns:
        tuple: First position boolean - True if substitution is wanted
    """
    # Asks if substitution is wanted
    inp = input("Would you like to substitute a letter? ")
    # If isn`t wanted return False
    if inp.lower() == 'no':
        return (False, None)
    # If is wanted: asks for letter
    elif inp.lower() == "yes":
        inp_letter = input("Which letter would you like to replace: ")
        return (True, inp_letter)
    # If input is not correct - ask again
    else:
        print("Incorrect input. Please, enter 'yes' or 'no'.")
        return ask_substitution_letter()

def regame(hand_score, is_regame_availible, hand, word_list):
    """Makes regame if is_regame_availivle is true
    Args:
        hand_score (int): previous hand score
        is_regame_availible (bool): if regame is availible
        hand (dict): current hand
        word_list (list): list of correct words
    Returns:
        tuple: first: integer -greater of two scores - hand_score, of hand_score of new game
               second: boolean - new value of is_regame_availible
    """
    # If regame is not availible - just return previous game score
    if not is_regame_availible:
        return (hand_score, False)
    # Asking player
    inp = input("Would you like to replay the hand? ")
    # If player want to regame
    if inp.lower() == "yes":
        # Play new game with previous hand
        new_score = play_hand(hand, word_list)
        # Return max of both scores
        return (max(new_score, hand_score), False)
    # If player doesn`t want to regame
    elif inp.lower() == "no":
        return (hand_score, is_regame_availible)
    # If input is incorrect - try again
    else:
        print("Incorrect input. Please, enter 'yes' or 'no'.")
        return regame(hand_score, is_regame_availible, hand, word_list)









    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    num_of_hands = ask_for_num_of_hands()
    # Initiating total score
    total_score = 0
    counter = 0
    # Initiating availible try to regame
    is_regame_availible = True
    while counter < num_of_hands:
        # Dealing new hand
        hand = deal_hand(HAND_SIZE)
        # Display current hand
        display_hand(hand)
        # Asking if substitution is needed, if True - replase letter
        tuple_substitution = ask_substitution_letter()
        if tuple_substitution[0]:
            hand = substitute_hand(hand, tuple_substitution[1])
        print()
        # Play hand
        hand_score = play_hand(hand, word_list)
        # Asking for regame
        hand_score, is_regame_availible = regame(hand_score, is_regame_availible, hand, word_list)
        # Adding hand score to total
        total_score += hand_score
        counter += 1
    # Print total score
    print(f"Total score over all hands: {total_score}")




if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
