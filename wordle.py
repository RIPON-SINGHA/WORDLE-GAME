def main():
    secret = "apple"
    attempts = 6

    print(".......WELCOME TO THE WORDLE GAME.......")
    print()
    print("G MEANS EXACT POSITION, Y MENAS EXIST BUT DIFFERENT POSITION AND X MEANS NOT IN THE WORD")
    
    while attempts > 0:
        guess = input("Enter a five letter word: ").lower()

        if len(guess) != 5 or not guess.isalpha():
            print("Enter valid word. only using alphabets of 5 letters.")
            continue
        
        result = evaluate(secret, guess)
        formatted_output = format_output(guess, result)
        print(formatted_output)
        

        if all(letter == "G" for letter in result):
            print("You have guessed the correct word!")
            break

        print(f"{attempts - 1} attempts left")
        
        attempts -= 1

    if attempts == 0:
        print("Attempts over! You lose XD")
        
            


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


main()