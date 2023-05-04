global freq
freq = 'esiarntolcdugpnkhbyfvwzxqj'

def get_all_n_letter_words(n):
    # get dictionary
    with open("/usr/share/dict/words") as f:
        words = f.readlines()
    words = [w.strip() for w in words] # strip the \n from the end of the words
    words = [w.lower() for w in words] # make them all lowercase
    # wordle uses n letter words only
    words = [w for w in words if len(w)==n]
    return words

def include(included_letters,word):
    for letter in included_letters:
        if word.find(letter) == -1:
            return False
        else:
            continue
    return True

def exclude(excluded_letters,word):
    for letter in excluded_letters:
        if word.find(letter) != -1:
            return False 
        else:
            continue
    return True

def locate(letter_location,word):
    for letter,index in letter_location:
        if word[index] != letter:
            return False 
        else: 
            continue
    return True

def dislocate(letter_not_location,word):
    for letter,index in letter_not_location:
        if word[index] == letter:
            return False 
        else: 
            continue
    return True

def optimum_guess(words,repetition,n):
    # frequancy of letters used in dictionary

    high_score = 1000000000
    optimum_word = None
    for w in words:
        score = 0
        if not repetition:
            if len(set(list(w)))!=n:
                continue
        for c in w:
            if c in freq:
                score += freq.index(c)
            else:
                score += 100
        if score < high_score:
            high_score = score
            optimum_word = w
            print(optimum_word,score)
    return optimum_word

def guess(n, repetition, words, included_letters, excluded_letters, letter_location, letter_not_location):
    # search for word that include,exclude
    words = [w for w in words if (include(included_letters,w) and exclude(excluded_letters,w))]
    # if we know a location of a letter, update the letters based on that
    words = [w for w in words if (locate(letter_location,w) and dislocate(letter_not_location,w))]
    if len(words) < 200:
        print(f"all possible words:{words}")
    optimum_next_word = optimum_guess(words,repetition,n)
    print(optimum_next_word)
    return optimum_next_word

def main():
    # innit
    n = 0
    success = False
    repetition = False
    guessed_word = None

    included_letters = []
    excluded_letters = []
    letter_location  = [] #[['e',3],['r',4]]
    letter_not_location = []

    # user inputs: define the word length
    while (n > 24 or n < 2):
        try: 
            n = int(input('Number of letters (between 2 and 24): \n'))
            # check if n makes sense:
            if (n > 24 or n < 2) :
                print(f"{n} is not between 2 and 24. Please try again. ")
                n = int(input('Number of letters: '))
        except ValueError or KeyboardInterrupt:
            n = 0
            print("Input numbers only! Let's try again.")

    # get the n letter words from the dictionary
    words = get_all_n_letter_words(n)
    
    # initial guess
    guessed_word = guess(n,repetition,words,[],[],[],[])
    try:
        success = int(input('Did it work? (1 if yes, 0 if no) '))
    except:
        print("okay bye!")
        exit()
    
    while not success and guessed_word is not None:
        # get gather more data about the word:
        included = (input('what letters are included? (- if nothing to add) \n')).split(',')
        for c in included:
            try:
                included_letters.index(c)
            except ValueError:
                if c in freq:
                    included_letters.append(c)
        print(f"including: {included_letters}")
        
        excluded = (input('what letters are excluded? (- if nothing to add) \n')).split(',')
        for c in excluded:
            try:
                excluded_letters.index(c)
                # continue
            except ValueError:
                if c in freq:
                    excluded_letters.append(c)
                # continue 
        print(f"excluding: {excluded_letters}")

        # get the updated list of letters that their location needs to be updated
        if len(letter_location) == 0:
            letter_location_needs_updating = included_letters
        else:
            letter_location_needs_updating = [c for c in included_letters if c not in letter_location[0][:]]

        # update the location of the letters 
        for c in letter_location_needs_updating:
            print(f"Do you know the location of the letter {c}?")
            location_is_known = int(input("(1 if yes, 0 if no) "))
            if location_is_known == True:
                index = int(input("What is the index? (count from 1) \n"))
                letter_location.append([c,index-1])
            else:
                print(f"Where is the index of {c} currently? (count from 1)")
                index_not = int(input(""))
                letter_not_location.append([c,index_not-1])
        
        # do the guessing part
        guessed_word = guess(n,repetition,words,included_letters,excluded_letters,letter_location,letter_not_location)
        if guessed_word == None:
            # try allowing repetition
            repetition = True
            guessed_word = guess(n,repetition,words,included_letters,excluded_letters,letter_location,letter_not_location)
        try:
            success = int(input('Did it work? (1 if yes, 0 if no) '))
        except:
            print("okay bye!")
            break

        if success:
            print(f"Awesome, {guessed_word.upper()} was the wordle word of day")
            break
        if not success and guessed_word is None:
            print(f"Sorry, coudn't help you find the wordle word of day")
            break
        
  
if __name__ == "__main__":
    main()