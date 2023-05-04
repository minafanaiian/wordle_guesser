global freq
# frequancy of letters used in dictionary
freq = 'esiarntolcdugpnkhbyfvwzxqj'

def get_all_5_letter_words():
    words = open("words.txt", "r")
    words = [w.strip() for w in words] # strip the \n from the end of the words
    words = [w.lower() for w in words] # make them all lowercase
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

def optimum_guess(n, words,repetition):

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
            # print(optimum_word,score)
    return optimum_word

def guess(n, words, repetition, included_letters, excluded_letters, letter_location, letter_not_location):
    # search for word that include,exclude
    words = [w for w in words if (include(included_letters,w) and exclude(excluded_letters,w))]
    # if we know a location of a letter, update the letters based on that
    words = [w for w in words if (locate(letter_location,w) and dislocate(letter_not_location,w))]
    optimum_word = optimum_guess(n, words,repetition)
    print(f"Try:  {optimum_word}")
    return optimum_word

def main():
    # innit
    n = 5
    success = False
    repetition = False
    guessed_word = None

    included_letters = []
    excluded_letters = []
    letter_location  = [] #[['e',3],['r',4]]
    letter_not_location = []

    # get the 5 letter words from the dictionary
    words = get_all_5_letter_words()
    
    # initial guess
    guessed_word = optimum_guess(n, words,repetition)
    print(f"Try:  {guessed_word}")
    try:
        success = int(input('Did it work? (1 if yes, 0 if no) '))
    except:
        print("\n   Okay bye! \n")
        exit()
    
    while not success and guessed_word is not None:
        try:
            # let's gather more data about the word:
            included = (input('what letters are included? (- if nothing to add) \n')).split(',')
            for c in included:
                try:
                    included_letters.index(c)
                except ValueError:
                    if c in freq:
                        included_letters.append(c)
            print(f"including: {included_letters}")

            # instead of asking what is excluded, we can figure it out based the suggested word
            excluded = [guessed_word[i] for i in range(5) if (guessed_word[i] not in included) and (guessed_word[i] not in included_letters)]

            for c in excluded:
                try:
                    excluded_letters.index(c)
                except ValueError:
                    if c in freq:
                        excluded_letters.append(c)
            print(f"excluding: {excluded_letters}")

            # get the updated list of letters that their location needs to be updated
            if len(letter_location) == 0:
                letter_location_needs_updating = included_letters
            else:
                letter_location_needs_updating = [c for c in included_letters if c not in letter_location[0][:]]

            # update the location of the letters 
            for c in letter_location_needs_updating:
                print(f"Is the letter -{c}- green?")
                location_is_known = int(input("(1 if yes, 0 if no) "))
                # instead of asking for the current index, we can get that from the guessed word.
                if location_is_known == True:   
                    index = guessed_word.index(c)
                    letter_location.append([c,index])
                else:
                    index_not = guessed_word.index(c)
                    letter_not_location.append([c,index_not])
            
            # do the guessing part
            guessed_word = guess(n,words,repetition,included_letters,excluded_letters,letter_location,letter_not_location)
            if guessed_word == None:
                # try allowing repetition
                repetition = True
                guessed_word = guess(n,words,repetition,included_letters,excluded_letters,letter_location,letter_not_location)
            try:
                success = int(input('Did it work? (1 if yes, 0 if no) '))
            except:
                print("\n   Okay bye! \n")
                break

            if success:
                print(f"Awesome, {guessed_word.upper()} was the wordle word of day!")
                break
            if not success and guessed_word is None:
                print(f"Sorry, coudn't help you find the wordle word of day. :( ")
                break
        
        except Exception as e:
            print(e)
            print("\n   Okay bye! \n")
            exit()
        
  
if __name__ == "__main__":
    main()