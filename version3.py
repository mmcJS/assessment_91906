# imports
# importing secrets is for generating random numbers
import secrets
import string
import tkinter

# installed pyperclip, which was to allow my program access to changing clipboard data
# pyperclip is a module that can be downloaded in this IDE (Pycharm)
# by going from Python Packages -> searching "pyperclip" and installing.
import pyperclip
# tkinter msgboxes and scroll ( used for the Help page )
from tkinter import messagebox, scrolledtext

# imported os so i can create the "logged password" documnts
import os

# all the gui and buttons mostly using tkinter
root = tkinter.Tk()
root.title("Password Generator (version 3)")

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

def log_password(password, name="", description=""):
    with open(log_file_path, "a") as f:
        f.write(f"{name}\t{password}\t{description}\n")

# this function logs the password,
def view_logged_passwords():
    for widget in root.winfo_children():
        widget.grid_forget()

    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as f:
            passwords = f.readlines()

    # changing text to calibri, sized 12, bold
        frame = tkinter.Frame(root)
        # sticky nsew makes the buttons and stuff stretch out with the window being resized
        frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky='nsew')
        # sticky west is to bring the three checkboxes to the left of the screen, for a more compact look
        name_label = tkinter.Label(frame, text="Name", font=('Calibri', 12, 'bold'))
        name_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        password_label = tkinter.Label(frame, text="Password", font=('Calibri', 12, 'bold'))
        password_label.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        description_label = tkinter.Label(frame, text="Description", font=('Calibri', 12, 'bold'))
        description_label.grid(row=0, column=2, padx=10, pady=5, sticky='w')

        for i, line in enumerate(passwords):
            name, password, description = line.strip().split('\t')
            # sticky west is to bring the three checkboxes to the left of the screen, for a more compact look
            name_label = tkinter.Label(frame, text=name, font=('Calibri', 12))
            name_label.grid(row=i+1, column=0, padx=10, pady=5, sticky='w')

            password_label = tkinter.Label(frame, text=password, font=('Calibri', 12))
            password_label.grid(row=i+1, column=1, padx=10, pady=5, sticky='w')

            description_label = tkinter.Label(frame, text=description, font=('Calibri', 12))
            description_label.grid(row=i+1, column=2, padx=10, pady=5, sticky='w')
        # for the logged passwords page, three columns
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

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

# function to show the generate password (home) page
def show_generate_page():
    for widget in root.winfo_children():
        widget.grid_forget()

    tkinter.Label(root, text="Password Length:", font=('Calibri', 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    length_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    tkinter.Checkbutton(root, text="Include Uppercase Letters?", variable=uppercase_var, font=('Calibri', 12)).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='w')
    tkinter.Checkbutton(root, text="Include Numbers?", variable=numbers_var, font=('Calibri', 12)).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='w')
    tkinter.Checkbutton(root, text="Include Special Characters?", variable=special_var, font=('Calibri', 12)).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='w')

    tkinter.Button(root, text="Generate Password", command=generate_and_display_password, font=('Calibri', 12)).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    tkinter.Label(root, text="Generated Password:", font=('Calibri', 12)).grid(row=5, column=0, padx=10, pady=10, sticky='w')
    password_entry.grid(row=5, column=1, padx=10, pady=10, sticky='ew')

    tkinter.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, font=('Calibri', 12)).grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

# function to show the help page when its nav button is clicked
def show_help_page():
    for widget in root.winfo_children():
        widget.grid_forget()

    # doing help text once i complete, so i can add information about everything all at once
    #    help_text = """"

    text_area = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, width=50, height=20, font=('Calibri', 12))
    text_area.grid(column=0, row=0, padx=10, pady=10, columnspan=2, sticky='nsew')
    text_area.config(state=tkinter.DISABLED)

# navigation bar menu at the top
menu = tkinter.Menu(root)
root.config(menu=menu)
menu.add_command(label="Generate", command=show_generate_page)
menu.add_command(label="Logged Passwords", command=view_logged_passwords)
menu.add_command(label="Help!", command=show_help_page)

length_entry = tkinter.Entry(root, font=('Calibri', 12))
uppercase_var = tkinter.BooleanVar()
numbers_var = tkinter.BooleanVar()
special_var = tkinter.BooleanVar()
password_entry = tkinter.Entry(root, width=50, font=('Calibri', 12))

# to initally show the generate home page when the app is opened
show_generate_page()

# logged passwords, borders to make it look more like a spreadsheet.
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=1)
root.rowconfigure(6, weight=1)

root.mainloop()
