import tkinter as tk
from wordle import evaluate, format_output

secret = "apple"
guessed_word = []
current_row = 0

def submit_guess():
    global current_row
    guess = entry.get().lower()
     
    if len(guess) != 5 or not guess.isalpha():
        label.config(text= "Please enter valid words")
        return
    
    result = evaluate(secret, guess)
    # formatted_output = format_output(guess, result)

    if current_row >= 6:
        return 
    for i in range(5):
        grid_label[current_row][i].config(text=guess[i].upper())
    current_row += 1

    # guessed_word.append(formatted_output)
    # all_guesses = "\n".join(guessed_word)
    # label.config(text=all_guesses)

    entry.delete(0, tk.END)

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
        label = tk.Label(grid_frame, fg="gray", width=4, height=2, borderwidth=1, relief="solid", font=("Arial", 20, "bold"), anchor="center")
        label.grid(row = row, column= col, padx= 5, pady= 5)
        grid_box.append(label)
    grid_label.append(grid_box)

entry = tk.Entry(control_frame)
entry.pack(pady=10)

btn = tk.Button(control_frame, text="Submit", command=submit_guess)
btn.pack(pady=10)

label = tk.Label(control_frame, text="Welcome to WORDLE GAME", justify="left", anchor = "w")
label.pack(pady=20)

root.mainloop()
