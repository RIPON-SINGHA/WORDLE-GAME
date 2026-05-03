import tkinter as tk
from tkinter import messagebox
from wordle import evaluate, update_used_letters, load_wordlist
import random

words = load_wordlist()

class wordleGame:
    def __init__(self):
        self.root = tk.Tk()

        self.secret = random.choice(words)
        self.guessed_word = set()
        self.current_row = 0
        self.used_letters = {}

        self.setup_ui()

        self.keyboard_ui()
        
        self.bind_events()

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

        for i in range(5):
            if result[i]== "G":
                color = "green"
            elif result[i] == "Y":
                color = "yellow"
            else:
                color="gray"
            
            self.grid_label[self.current_row][i].config(text=guess[i].upper(), bg = color)
            
        if self.secret == guess:
            self.show_popup("YOU WON, You guessed the secret word \n Want to play again?")
            self.label1.config(text="YOU WON, You guessed the secret word!")
            self.entry.config(state="disabled")
            self.btn.config(state="disabled")
            for keys in self.keyboard_buttons:
                self.keyboard_buttons[keys].config(state="disabled")

            return
        
        self.current_row += 1

        if self.current_row == 6:
            self.show_popup(f"Game over! The word was {self.secret.upper()} \n Want to play again?")
            self.label1.config(text=f"Game over! The word was {self.secret.upper()}")
            self.entry.config(state="disabled")
            self.btn.config(state="disabled")
            
            for keys in self.keyboard_buttons:
                self.keyboard_buttons[keys].config(state="disabled")



    def handle_input(self, letter):
        word = self.entry.get()
        if len(word) < 5:
            self.entry.insert(tk.END, letter)

    
    def input_handler(self, event):
        if event.keysym == "BackSpace":
            self.handle_backspace()
        elif event.keysym == "Return":
            self.handle_enter()
        elif event.char.isalpha() and len(event.char) == 1:
            self.handle_input(event.char.upper())

        return "break"
    
    def handle_backspace(self, event = None):
        currTxt = self.entry.get() #5
        if len(currTxt) > 0:
            self.entry.delete(len(currTxt) - 1, tk.END)
        return "break"

    def handle_enter(self, event = None):
        self.submit_guess()
        return "break"

    def ui_key_press(self, btn):
        if btn == "BACK":
            self.handle_backspace()
        elif btn == "ENTER":
            self.handle_enter()
        else:
            self.handle_input(btn)


    def keycolor_update(self):
        for letter, color in self.used_letters.items():
            key = letter.upper()

            if key in self.keyboard_buttons:
                btn = self.keyboard_buttons[key]

                if color == "G":
                    btn.config(bg="green")
                elif color == "Y":
                    if btn.cget("bg") != "green":
                        btn.config(bg="yellow", fg="black")
                else:
                    if btn.cget("bg") not in ["green", "yellow"]:
                        btn.config(bg="gray", fg="white")

    def restart_game(self):
        self.current_row = 0
        self.used_letters = {}
        self.guessed_word.clear()

        self.secret = random.choice(words)

        for row in range(6):
            for col in range(5):
                self.grid_label[row][col].config(text="", bg = self.default_bg)
        
        for keys in self.keyboard_buttons:
            self.keyboard_buttons[keys].config(bg="white", fg="black", state = "normal")
        
        self.btn.config(state = "normal")
        self.entry.delete(0, tk.END)
        self.entry.config(state="normal")
        self.label1.config(text = "Welcome to WORDLE GAME")
        self.label2.config(text = "")


    def setup_ui(self):
        self.root.title("WORDLE GAME")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        self.root.bind("<Key>", self.input_handler)

        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=30)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=20)

        self.grid_label = []

        for row in range(6):
            grid_box = []
            for col in range(5):
                label = tk.Label(self.grid_frame, fg="black", width=4, height=2, borderwidth=1, relief="solid", font=("Arial", 20, "bold"), anchor="center")
                label.grid(row = row, column= col, padx= 5, pady= 5)
                grid_box.append(label)

            self.grid_label.append(grid_box)

        self.default_bg = self.grid_label[0][0].cget("bg")

        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=10)
        self.entry.bind("<Key>", self.input_handler)

        self.btn = tk.Button(self.root, text="SUBMIT", command=self.submit_guess)
        self.btn.pack(pady=10)

        self.label1 = tk.Label(self.root, text="Welcome to the WORDLE GAME", justify="left", anchor="w", font=("Arial", 15, "bold"))
        self.label1.pack(pady=20)

        self.label2 = tk.Label(self.root, text="")
        self.label2.pack(pady=20)

        self.restartBtn = tk.Button(self.root, text="Restart", command= self.restart_game)
        self.restartBtn.pack(pady=20)


    def keyboard_ui(self):
        self.keyboard_frame = tk.Frame(self.root)
        self.keyboard_frame.pack(pady=20)

        self.keyboard_layout = [
            ["Q","W","E","R","T","Y","U","I","O","P"],
            ["A","S","D","F","G","H","J","K","L"],
            ["ENTER","Z","X","C","V","B","N","M","BACK"]
        ]


        self.keyboard_buttons = {}
        keyboard = []
        base_offset = 3

        max_cols = 10 
        for i in range(3):
            key_row = []
            row_len = len(self.keyboard_layout[i])
            start_col = (max_cols - row_len) // 2 + base_offset

            for j in range(row_len):
                letter = self.keyboard_layout[i][j]

                display_text = "←" if letter == "BACK" else ("ENT" if letter == "ENTER" else letter)
                width = 6 if letter in ["ENTER", "BACK"] else 3

                key = tk.Button(
                    self.keyboard_frame,
                    text=display_text,
                    width=width,
                    height=1,
                    font=("Arial", 10, "bold"),
                    command=lambda l=letter: self.ui_key_press(l)
                )

                key.grid(row=i, column=start_col + j, padx=1 if i == 0 else 2, pady=2)

                key_row.append(key)
                self.keyboard_buttons[letter] = key

            keyboard.append(key_row)
    
    def bind_events(self):
        self.root.bind("<Key>", self.input_handler)
        self.entry.bind("<Key>", self.input_handler)

    def restart_from_popup(self, popup):
        popup.destroy()
        self.restart_game()

    def show_popup(self, msg):
        popup = tk.Toplevel(self.root)
        popup.title("Result")
        popup.geometry("700x200")
        popup.transient(self.root)
        popup.grab_set()

        popup.update_idletasks()

        popup_width = 700
        popup_height = 200

        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        x = root_x + (root_width // 2) - (popup_width // 2)
        y = root_y + (root_height // 2) - (popup_height // 2)

        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        label = tk.Label(popup, text=msg, font=("Arial", 20, "bold"))
        label.pack(expand=True)

        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=10)

        yes_btn = tk.Button(btn_frame, text="Yes", command=lambda: self.restart_from_popup(popup))
        yes_btn.pack(side="left", padx=10)

        no_btn = tk.Button(btn_frame, text="No", command=self.root.quit)
        no_btn.pack(side="right", padx=10)



game = wordleGame()
print(game.secret)
game.root.mainloop()





