from wordledict import get_lists
import random 
# Load possible list of words
winning_words, viables = get_lists()
#winning_words = winning_words + viables

#######################################################################
################ SET THE CURRENT STATE OF THE BOARD HERE ##############
#######################################################################

# List of green letters. Zero based position.
# Replace each asterisk with a known green letter. 
green_letters = ['*', '*', '*', '*', '*'] 

# List of all yellow letters and where they have been seen. 
# Zero based position.
yellow_letters = [set([]), # For example set(['a', 'c']) means a and c have been seen as yelow in the first letter.
                  set([]), # Yellows seen in the second letter...
                  set([]),
                  set([]),
                  set([])]

# Set of black letters.
black_letters = set("")     # All letters that have been played but aren't in the final solution. 
                            # e.g. "abc" means A, B and C have been played and isn't yellow or green.

#######################################################################
#######################################################################

# Wordle will mark a black letter if it appears yellow or green elsewhere so just in case. 
black_letters = black_letters.difference(set().union(*yellow_letters))
black_letters = black_letters.difference(set(green_letters))


def is_viable(candidate, 
                green_letters,
                yellow_letters,
                black_letters):
    """
    Takes a state of the world and a word and makes sure that the word is viable given all the info so far. 
    """
    assert len(candidate) == len(green_letters), "Candidate word and green letter list must be of the same length"
    assert len(candidate) == len(yellow_letters), "Candidate word and yellow letter list must be of the same length"
    
    
    # If it has any black letters, it's not viable.
    if len(set(candidate).intersection(black_letters)) != 0:
        return False
    
    
    # If it has something other than the right letter in a known green, it's not viable.
    for i in range(0, len(candidate)):
        if green_letters[i] == '*': 
            continue
        if green_letters[i] != candidate[i]:
            return False
     
    # If it has a yellow in a place where its been seen as yellow, it's not viable. 
    for i in range(0, len(candidate)):
        if candidate[i] in yellow_letters[i]:
            return False
    
    # If it doesn't have all the yellows, it's not viable.
    all_yellows = set().union(*yellow_letters)
    if len(all_yellows) > len(all_yellows.intersection(set(candidate))):
        return False
    
    return True


def get_viable_candidates(winning_words, 
                            green_letters,
                            yellow_letters,
                            black_letters):
    """
    Get the list of candidates that are viable for a given state of the board.
    """
    return [w for w in winning_words if is_viable(w, green_letters, yellow_letters, black_letters)]

def score_candidate(winning_words, 
                    green_letters,
                    yellow_letters,
                    black_letters,
                    candidate):
    """
    Takes the state of the board and a candidate word and runs a 
    heuristic to give it a score.
    """    
    # If it's not viable it gets a score of -1. 
    if not is_viable(candidate, green_letters, yellow_letters, black_letters):
        return -1
    
    num_viable_before = len(get_viable_candidates(winning_words, 
                                                    green_letters,
                                                    yellow_letters,
                                                    black_letters))
    
    letter_level_score = [0] * len(candidate)
    # Let's go letter by letter.
    for i in range(0, len(candidate)):
        # If I play this letter what's the remaining set of candidates if this letter is green?
        new_green = green_letters.copy()
        new_green[i] = candidate[i]
        num_viable_g = len(get_viable_candidates(winning_words, 
                                                 new_green,
                                                 yellow_letters,
                                                 black_letters))
                                                 
        # If I play this letter what's the remaining set of candidates if this letter is yellow?
        new_yellows = [s.copy() for s in yellow_letters]
        new_yellows[i] = new_yellows[i].union([candidate[i]])
        num_viable_y = len(get_viable_candidates(winning_words, 
                                                    green_letters,
                                                    new_yellows,
                                                    black_letters))
                                                    
                                                                                                  
        # If I play this letter what's the remaining set of candidates if this letter is black?
        new_blacks = black_letters.union([candidate[i]])
        num_viable_b = len(get_viable_candidates(winning_words, 
                            green_letters,
                            yellow_letters,
                            new_blacks))


        eliminated_g = num_viable_before - num_viable_g
        eliminated_y = num_viable_before - num_viable_y
        eliminated_b = num_viable_before - num_viable_b
        
        weight_g = 1 # These weights are a bit random...
        weight_y = 10
        weight_b = 20

        letter_level_score[i] = weight_g*eliminated_b + \
                                weight_y*eliminated_y + \
                                weight_g*eliminated_g
    
    # Reward those with more unique words.     
    return sum(letter_level_score)*len(set(candidate))

viables = get_viable_candidates(winning_words, 
                            green_letters,
                            yellow_letters,
                            black_letters)

print("Scoring " + str(len(viables)) + " words.")

candidates = []
c = 0
for candidate in viables:
    score = score_candidate(winning_words, 
                            green_letters, 
                            yellow_letters, 
                            black_letters,
                            candidate)
    c = c + 1
    if c % 100 == 0:
        print("Scored " + str(c) + " candidates so far.")
    candidates.append((candidate, score))

candidates.sort(key = lambda x:x[1])

for c in candidates:
    print(c[0] + " - "  + str(c[1]))
    
    
# Of the top candidates, pick one at random to play.
top_score = max(candidates, key = lambda x:x[1])[1]
rc = random.sample([c for c in candidates if c[1] == top_score], 1)

print("\n Suggested word to play: " + str(rc))