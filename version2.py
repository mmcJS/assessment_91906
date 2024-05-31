# imports
# importing secrets is for generating random numbers
import secrets
import string
import tkinter

# installed pyperclip, which was to allow my program access to changing clipboard data
# pyperclip is a module that can be downloaded in this IDE (Pycharm)
# by going from Python Packages -> searching "pyperclip" and installing.
import pyperclip

from tkinter import messagebox, scrolledtext

# import os
import os

# all the gui and buttons mostly using tkinter
root = tkinter.Tk()
root.title("Password Generator (version 2)")

# places the password_log.txt in the same directory as the python file for easy access
current_directory = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_directory, "password_log.txt")

# directory check for debugging purposes
print(f"{log_file_path}")

# generating password function

def generate_password(length, use_uppercase, use_numbers, use_special):
    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    password = ''.join(secrets.choice(characters) for _ in range(length))
    log_password(password)
    return password

# this function logs the password,
def log_password(password):
    with open(log_file_path, "a") as f:
        f.write(password + "\n")

# this function views logged passwords
def view_logged_passwords():
    for widget in root.winfo_children():
        widget.grid_forget()

    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as f:
            passwords = f.read()

        text_area = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, width=50, height=20)
        text_area.grid(column=0, row=0, padx=10, pady=10, columnspan=2)
        text_area.insert(tkinter.END, passwords)
        text_area.config(state=tkinter.DISABLED)



# displaying the password function
def generate_and_display_password():
    try:
        length = int(length_entry.get())
        use_uppercase = uppercase_var.get()
        use_numbers = numbers_var.get()
        use_special = special_var.get()

        # checks for input of 0
        if length < 1:
            raise ValueError("Character length must be greater than 0, with a recommended length of 6+ for strength.")

        password = generate_password(length, use_uppercase, use_numbers, use_special)
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

# function to show the generate password page
def show_generate_page():
    for widget in root.winfo_children():
        widget.grid_forget()

    tkinter.Label(root, text="Password Length:").grid(row=0, column=0, padx=10, pady=10)
    length_entry.grid(row=0, column=1, padx=10, pady=10)

    tkinter.Checkbutton(root, text="Include Uppercase Letters?", variable=uppercase_var).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    tkinter.Checkbutton(root, text="Include Numbers?", variable=numbers_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    tkinter.Checkbutton(root, text="Include Special Characters?", variable=special_var).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    tkinter.Button(root, text="Generate Password", command=generate_and_display_password).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    tkinter.Label(root, text="Generated Password:").grid(row=5, column=0, padx=10, pady=10)
    password_entry.grid(row=5, column=1, padx=10, pady=10)

    tkinter.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# function to show the help page when its nav button is clicked
def show_help_page():
    for widget in root.winfo_children():
        widget.grid_forget()



# doing help text once i complete, so i can add information about everything all at once
#    help_text = "

    text_area = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, width=50, height=20)
    text_area.grid(column=0, row=0, padx=10, pady=10, columnspan=2)
    text_area.config(state=tkinter.DISABLED)

# navigation bar menu
menu = tkinter.Menu(root)
root.config(menu=menu)
menu.add_command(label="Generate", command=show_generate_page)
menu.add_command(label="Logged Passwords", command=view_logged_passwords)
menu.add_command(label="Help!", command=show_help_page)

#

length_entry = tkinter.Entry(root)
uppercase_var = tkinter.BooleanVar()
numbers_var = tkinter.BooleanVar()
special_var = tkinter.BooleanVar()
password_entry = tkinter.Entry(root, width=50)


# Initially show the generate password page
show_generate_page()

root.mainloop()
