# imports
# importing secrets is for generating random numbers
import secrets
import string
import tkinter

# installed pyperclip, which was to allow my program access to changing clipboard data
# papyrclip is a module that can be downloaded in this IDE (Pycharm)
# by going from Python Packages -> searching "pyperclip" and installing.
import pyperclip


# generating password function
def generate_password(length, use_uppercase, use_digits, use_special):
    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

# message boxes
from tkinter import messagebox

# displaying the password function

def generate_and_display_password():
    try:
        length = int(length_entry.get())
        use_uppercase = uppercase_var.get()
        use_digits = numbers_var.get()
        use_special = special_var.get()

        # checks for input of 0
        if length < 1:
            raise ValueError("Character length must be greater than 0, with a recommended length of 6+ for strength.")

        password = generate_password(length, use_uppercase, use_digits, use_special)
        password_entry.delete(0, tkinter.END)
        password_entry.insert(0, password)
    except ValueError:
        # error messagebox
        messagebox.showerror("Invalid Input", "Password length may only be numbers.")


# function that copies the password to clipboard upon press of the "copy the clipboard button" using the
# pyperclip module.
def copy_to_clipboard():
    password = password_entry.get()
    pyperclip.copy(password)
    messagebox.showinfo("Copied!", "Password has been copied to your clipboard!")

# all the gui and buttons mostly using tkinter
root = tkinter.Tk()
root.title("Password Generator (version 1)")

# "password length" text and box
tkinter.Label(root, text="Password Length:").grid(row=0, column=0, padx=10, pady=10)
length_entry = tkinter.Entry(root)
length_entry.grid(row=0, column=1, padx=10, pady=10)

# uppercase letters box + text
uppercase_var = tkinter.BooleanVar()
tkinter.Checkbutton(root, text="Include Uppercase Letters?", variable=uppercase_var).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
# numbers / digits box + text
numbers_var = tkinter.BooleanVar()
tkinter.Checkbutton(root, text="Include Numbers?", variable=numbers_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# special characters box + text
special_var = tkinter.BooleanVar()
tkinter.Checkbutton(root, text="Include Special Characters?", variable=special_var).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

tkinter.Button(root, text="Generate Password", command=generate_and_display_password).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

tkinter.Label(root, text="Generated Password:").grid(row=5, column=0, padx=10, pady=10)
password_entry = tkinter.Entry(root, width=50)
password_entry.grid(row=5, column=1, padx=10, pady=10)

tkinter.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).grid(row=6, column=0, columnspan=2, padx=10, pady=10)


root.mainloop()