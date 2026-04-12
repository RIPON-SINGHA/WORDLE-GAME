import tkinter as tk
from wordle import evaluate, update_used_letters, load_wordlist
import random

words = load_wordlist()
secret = random.choice(words)
guessed_word = set()
current_row = 0
used_letters = {}
print(secret)

def submit_guess():
    global current_row

    if current_row >= 6:
        return
    
    guess = entry.get().lower()

    if len(guess) != 5 or not guess.isalpha():
        label1.config(text= "Please enter valid words")
        return
    
    entry.delete(0, tk.END)

    if guess not in words:
        label1.config(text = "Not in the wordlist")
        return

    if guess in guessed_word:
        label1.config(text="You already guessed this word!")
        return
    
    guessed_word.add(guess)

    

    result = evaluate(secret, guess)
    update_used_letters(used_letters, guess, result)

    display = []
    for letter in sorted(used_letters):
        status = used_letters[letter]
        display.append(f"{letter.upper()}({status})")

    label2.config(text = ", ".join(display))

    for i in range(5):
        if result[i]== "G":
            color = "green"
        elif result[i] == "Y":
            color = "yellow"
        else:
            color="gray"
        
        grid_label[current_row][i].config(text=guess[i].upper(), bg = color)

    if secret == guess:
        label1.config(text="YOU WON, You guessed the secret word!")
        entry.config(state="disabled")
        btn.config(state="disabled")
        return
    
    current_row += 1

    if current_row == 6:
        label1.config(text=f"Game over! The word was {secret.upper()}")
        entry.config(state="disabled")
        btn.config(state="disabled")


def restart_game():
    global current_row, used_letters, secret, guessed_word
    import random

    current_row = 0
    used_letters = {}
    guessed_word.clear()

    secret = random.choice(words)

    for row in range(6):
        for col in range(5):
            grid_label[row][col].config(text="", bg = default_bg)
    
    btn.config(state = "normal")
    entry.config(state="normal")
    label1.config(text = "Welcome to WORDLE GAME")
    label2.config(text = "")


root = tk.Tk()
grid_frame = tk.Frame(root)
grid_frame.pack(pady=30)

control_frame = tk.Frame(root)
control_frame.pack(pady=20)

root.title("WORDLE GAME")
root.geometry("700x700")

grid_label = []

for row in range(6):
    grid_box = []
    for col in range(5):
        label = tk.Label(grid_frame, fg="black", width=4, height=2, borderwidth=1, relief="solid", font=("Arial", 20, "bold"), anchor="center")
        label.grid(row = row, column= col, padx= 5, pady= 5)
        grid_box.append(label)
    grid_label.append(grid_box)

default_bg = grid_label[0][0].cget("bg")

entry = tk.Entry(control_frame)
entry.pack(pady=10)

btn = tk.Button(control_frame, text="Submit", command=submit_guess)
btn.pack(pady=10)

label1 = tk.Label(control_frame, text="Welcome to WORDLE GAME", justify="left", anchor = "w")
label1.pack(pady=20)

label2 = tk.Label(control_frame, text = "")
label2.pack(pady=20)

restart_btn = tk.Button(control_frame, text = "Restart", command=restart_game)
restart_btn.pack(pady=20)

root.mainloop() 
 