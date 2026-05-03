import tkinter as tk
from wordle import evaluate, update_used_letters, load_wordlist
import random

words = load_wordlist()

class wordleGame:
    def __init__(self):
        
        self.secret = random.choice(words)
        self.guessed_word = set()
        self.current_row = 0
        self.used_letters = {}


    def submit_guess(self):
        if self.current_row >= 6:
            return
        
        guess = self.entry.get().lower()

        if len(guess) != 5 or not guess.isalpha():
            self.label1.config(text= "Please enter valid words")
            return
        
        self.entry.delete(0, tk.END)

        if guess not in words:
            self.label1.config(text = "Not in the wordlist")
            return

        if guess in self.guessed_word:
            self.label1.config(text="You already guessed this word!")
            return
        
        self.guessed_word.add(guess)

        

        result = evaluate(self.secret, guess)
        update_used_letters(self.used_letters, guess, result)
        self.keycolor_update()
        display = []
        for letter in sorted(self.used_letters):
            status = self.used_letters[letter]
            display.append(f"{letter.upper()}({status})")

        self.label2.config(text = ", ".join(display))

        for i in range(5):
            if result[i]== "G":
                color = "green"
            elif result[i] == "Y":
                color = "yellow"
            else:
                color="gray"
            
            self.grid_label[current_row][i].config(text=guess[i].upper(), bg = color)
            
        if self.secret == guess:
            self.label1.config(text="YOU WON, You guessed the secret word!")
            self.entry.config(state="disabled")
            self.btn.config(state="disabled")
            for keys in self.keyboard_buttons:
                self.keyboard_buttons[keys].config(state="disabled")

            return
        
        current_row += 1

        if current_row == 6:
            self.label1.config(text=f"Game over! The word was {self.secret.upper()}")
            self.entry.config(state="disabled")
            self.btn.config(state="disabled")
            
            for keys in self.keyboard_buttons:
                self.keyboard_buttons[keys].config(state="disabled")


game = wordleGame()
print(game.secret)





