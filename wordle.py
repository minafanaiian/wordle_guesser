def get_all_n_letter_words(n):
    # get dictionary
    with open("/usr/share/dict/words") as f:
        words = f.readlines()
    words = [w.strip() for w in words] # strip the \n from the end of the words
    words = [w.lower() for w in words] # make them all lowercase
    # wordle uses 5 letter words only
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
    freq = 'esiarntolcdugpnkhbyfvwzxqj'
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

def main():
    # innit
    included_letters = []
    excluded_letters = []
    letter_location  = []
    letter_not_location = []
    repetition = False # by default, change if there is a repetition
    
    # user inputs
    n = 5
    included_letters = ['i', 't', 'o']
    excluded_letters = ['a', 'r', 's', 'e', 'n', 'c', 'p', 'l']
    letter_location  = [['i',1]]#,['l',5],['i',6],['n',7]]
    letter_not_location = [['t',0],['t',4],['o',1],['o',3]]
    repetition = True 
    
    # start program 
    # get the n letter words from the dictionßary
    words = get_all_n_letter_words(n)
    # search for word that include,exclude
    words = [w for w in words if (include(included_letters,w) and exclude(excluded_letters,w))]
    # if we know a location of a letter, update the letters based on that
    words = [w for w in words if locate(letter_location,w) and dislocate(letter_not_location,w)]
    if len(words) < 100:
        print(f"all possible words:{words}")
    # find the optimum next guess
    optimum_next_word = optimum_guess(words,repetition,n)
    print(optimum_next_word)
  
if __name__ == "__main__":
    main()