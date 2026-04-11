import random

def main():
    attempts = 6

    words = load_wordlist()
    secret = random.choice(words) 
    used_letters = {}
    guessed_words = set()

    print(".......WELCOME TO THE WORDLE GAME.......")
    print()
    print("G MEANS EXACT POSITION, Y MENAS EXIST BUT DIFFERENT POSITION AND X MEANS NOT IN THE WORD")
    print("You have 6 atttemps.")
    
    while attempts > 0:
        guess = input("Enter a five letter word: ").lower()

        if len(guess) != 5 or not guess.isalpha():
            print("Enter valid word. only using alphabets of 5 letters.")
            continue
        if guess not in words:
            print("Word not in the word list.")
            continue
        
        if guess in guessed_words:
            print("You already guessed this word.")
            continue
            
        guessed_words.add(guess)

        result = evaluate(secret, guess)
        update_used_letters(used_letters, guess, result)
        formatted_output = format_output(guess, result)
        print(formatted_output)
        print_used_letters(used_letters)
        print(f"guessed_words: {", ".join(sorted(guessed_words))}")

        if all(letter == "G" for letter in result):
            print("You have guessed the correct word!")
            break

        attempts -= 1
        print(f"{attempts} attempts left") if attempts > 0 else None
        
        

    if attempts == 0:
        print("Attempts over! You lose XD")
        print(f"the word was '{secret}'")
        
            


def evaluate(secret, guess):
    result = [None] * len(secret)
    Freq_pool = {}
    for char in secret:
        if char not in Freq_pool:
            Freq_pool[char] = 1
        else:
            Freq_pool[char] += 1

    for i in range(len(secret)):
        if guess[i] == secret[i]:
            result[i] = "G"
            Freq_pool[guess[i]] -= 1

    for i in range(len(secret)):
        if result[i] is None:
            char = guess[i]
            if char in Freq_pool and Freq_pool[char] > 0:
                result[i] = "Y"
                Freq_pool[char] -= 1
            else:
                result[i] = "X"

    return result

def format_output( guess, result):
    res = []
    for i in range(len(result)):
        if result[i] == "G":
            res.append(f"[{guess[i]}]")
        elif result[i] == "Y":
            res.append(f"({guess[i]})")
        else:
            res.append(guess[i])
    return " ".join(res)


def load_wordlist():
    with open("words.txt", "r") as words:
        word_list = []
        for word in words:
            word_list.append(word.strip().lower())
        
        return word_list
    

def update_used_letters(used_letters, guess, result):
    priority = {
        'G' : 3,
        'Y' : 2,
        'X' : 1
    }
    for i in range(len(guess)):
        letter = guess[i]
        status = result[i]

        if letter not in used_letters:
            used_letters[letter] = status
        else:
            old_status = used_letters[letter]

            if priority[status] > priority[old_status]:
                used_letters[letter] = status

def print_used_letters(used_letters):
    output = []

    for letter in sorted(used_letters.keys()):
        output.append(f"{letter}({used_letters[letter]})")

    print(f"Used letters: {" ".join(output)}")

if __name__ == "__main__":
    main()