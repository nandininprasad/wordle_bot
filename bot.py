# Create wordle bot
# May 13, 2024

file = open("words.txt", "r")
orig_word_list = []

for line in file:
    #line = line.lower()
    orig_word_list.append(line.strip().lower())

#print(word_list)

#Goal
# 1. Want to solve wordle in fewest number of steps
# 2. Want to get maximum info from each guess -- 
# ie decent distrib of vowels/consonants, 
# what new letters do u get after avoiding previous/double letters 

# enoguh intformation u go for guess

#Strategies:
# 1. letter frequency in total word list
# 2. letter frequency in each position in each word in total list
# 3. Sepearate list for words with the same letter twice?
# 4. relative frequency of words (from google)
# 5. use bigrams? (ch, st, etc.,)

# If a letter is confirmed to not be in the guess, delete words from the 
# word list

# If letter is confirmed - correct spot or wrong spot, then include from
# list that contains double letters 

#TOUPLE IS INMUTABLE

# list - can contain different data types including lists
# array - contains objects of only same data type
# time complexity -- IMPORTANT. Big O means worst case entry

# a1 a2 a3 a4 a5 

def calc_let_freq_tot():
    let_freq = {} #dictionary

    #set each letter freq to 0
    # letters = ['a','b','c','d','e','f','g','h','i','']
    # for letter in letters:
    #     letter_frequency[letter] = 0 

    for word in orig_word_list:
        for letter in word:
            # if letter not in letter_frequency:
            #     letter_frequency[letter] = 1
            # else:
            #     letter_frequency[letter] += 1
            let_freq[letter] = let_freq.get(letter,0) + 1

    return let_freq

#lambda function --> 
# Find which letters have the most frequency in the word list
let_freq = calc_let_freq_tot() #dictionary
sort_let_freq = sorted(let_freq.items(), key=lambda x:x[1], reverse=True)
# print(sort_let_freq[0:7])

def calc_let_pos_freq():
    let_pos_freq = {}

    for word in orig_word_list:
        #unpacking touple that enumerate is giving. enumerate is retuning a touple. 
        # i, letter is unpacking the touple
        for i,letter in enumerate(word): # (o,'n'), (1,'a') # touple
            # x=(1,2) touple. unpzcking x,y = (1,2) --> x=1, y=2
            position = let_pos_freq.get(letter, [0]*5)  
            # set to [0,0,0,0,0] first time you encounter a new letter
            position[i] += 1
            let_pos_freq[letter] = position
    return let_pos_freq

let_pos_freq = calc_let_pos_freq()
sort_let_pos_freq = sorted(let_pos_freq.items(), key=lambda t:sum(t[1]), reverse=True)
# print(sort_let_pos_freq)

# print(sort_let_freq[:5])
# print(sort_let_pos_freq[:4])

def get_freq_score(word_list):
    freq_score = {}

    for word in word_list:
        word_score = 0
        for i, letter in enumerate(word):
            # letter_score = let_pos_freq[letter] #list .. #letter-> string key, has list values
            # letter_pos_score = letter_score[i] #int
            # letter_pos_score = let_pos_freq[letter][i] #combining above two lines
            word_score += let_pos_freq[letter][i] # which is letter_pos_score
        freq_score[word] = word_score
   
    return freq_score

#dictionary word(str):freq_score(int)

# most frequent word in whole word list (sample space)
# OR
# most frequent word in reduced word list (conditional)

def rank_words(word_list):
    updated_freq_score = get_freq_score(word_list)
    #covert dictionary to list of (key, value) pairs
    ranked_word_list = [] # alternativeyl, ranked_list = frequency_score.items().sort(key reverse)
    ranked_word_list = sorted(updated_freq_score.items(), key=lambda x:x[1], reverse=True)
    
    return ranked_word_list


#score double-letters in same word negatively

def trim_list(correct_placed, wrong_placed_letters, wrong_letters, word_list):

    # correct placed
    for i, letter in correct_placed:
        word_list = [word for word in word_list if word[i] == letter]

    # wrong placed
    for i, letter in wrong_placed_letters:
        word_list = [word for word in word_list if  letter in word and word[i] != letter]

    # wrong letters
    for i, letter in wrong_letters:
        word_list = [word for word in word_list if letter not in word]

    return word_list

def check_word(guess, target):

    correct_placed = []
    wrong_placed_letters = []

    for i in range(len(target)):
        if guess[i] == target[i]:
            correct_placed.append((i, guess[i]))
        elif guess[i] in target:
            wrong_placed_letters.append((i, guess[i]))

    wrong_letters = [(i, guess[i]) for i in range(len(target)) if (i, guess[i]) not in correct_placed and (i, guess[i]) not in wrong_placed_letters]

    return correct_placed, wrong_placed_letters, wrong_letters

def get_word_placements_from_user(guess):
    correct_placed = []
    wrong_placed_letters = []
    wrong_letters = []

    for i, letter in enumerate(guess):
        print(f"Letter {i+1}/{len(guess)}: {letter}")
        print("1) Correct placement")
        print("2) Wrong placement")
        print("3) Wrong letter")
        print("4) Skip")
        print("5) Exit")

        choice = input(">")
        if choice == "1":
            correct_placed.append((i, letter))
        elif choice == "2":
            wrong_placed_letters.append((i, letter))
        elif choice == "3":
            wrong_letters.append((i, letter))
        elif choice == "4":
            continue
        elif choice == "5":
            exit(0)
        else:
            print("Invalid choice. Try again")
            i -= 1

    return correct_placed, wrong_placed_letters, wrong_letters

def human_game( rank_words):
    
    solved = False
    words = orig_word_list.copy()
    num_tries = 6
    while num_tries > 0 and not solved:

        print("Number of tries left: ", num_tries)
        # Guess a word
        # ranked_list, prob_list = rank_words(words)
        ranked_list = rank_words(words)


        print("Suggestions: ")
        for i in range(0, min(5, len(ranked_list))):
            print(f"{i+1}) {ranked_list[i]}")


        TakeInput = True

        while TakeInput:
            try:
                print("Enter a word >", end="")
                guess = input().strip().lower()
                
                
                if guess not in words:
                    raise ValueError("Word not in dictionary")
                
                TakeInput = False

            except EOFError:
                exit(0)



        else:
            correct_placed, wrong_placed_letters, wrong_letters = get_word_placements_from_user(guess)
            if len(correct_placed) == 5:
                solved = True
            print("--> ", end="")
            for i, letter in enumerate(guess):
                if (i, letter) in correct_placed:
                    print(f"[{letter}]", end="")
                elif (i, letter) in wrong_placed_letters:
                    print(f"({letter})", end="")
                else:
                    print(letter, end="")

            print(f"\n {len(correct_placed)} correct placed, {len(wrong_placed_letters)} wrong placed")
            
            old_len = len(words)
            words = trim_list(correct_placed, wrong_placed_letters, wrong_letters, words)
            
            print(len(words) - old_len, f" words removed from list, {len(words)} words left")


        num_tries -= 1

    if not solved:
        
        return -1


### Get user input
human_game(rank_words=rank_words)