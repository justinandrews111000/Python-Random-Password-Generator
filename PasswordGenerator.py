import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime

letters = [
    'a', 'b', 'c', 'd',
    'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l',
    'm', 'n', 'o', 'p',
    'q', 'r', 's', 't',
    'u', 'v', 'w', 'x',
    'y', 'z',
    'A', 'B', 'C', 'D',
    'E', 'F', 'G', 'H',
    'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P',
    'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X',
    'Y', 'Z'
]

symbols = ["!", "@", "$", "#", "%", "^", "&", "*",
           "-", "_", "+", "=", "{", "}", "[", "]",
           "\\", "|", ":", ";", "\"", "'"]


user_rand = 3.97

root = tk.Tk()
root.title('Password Generator')
root.geometry('500x200')
root.resizable(False, False)

widget_state = tk.StringVar()
widget_state.set('disabled')


def gen_random_num():
    rand_hash = hash(str(random.randint(0, 1000)))
    if rand_hash < 0:
        rand_hash *= -1
    return rand_hash


frame = ttk.Frame(root)

rand_frame = tk.Toplevel(frame)
rand_frame.title('Random Number Seed Generater')
rand_frame.geometry('400x400')
rand_frame.withdraw()

password = []
password_letters = []
index_list = []
display_text = tk.StringVar()
letter_bool = tk.BooleanVar()
symbol_bool = tk.BooleanVar()
pass_length = tk.IntVar()


def generate_pass():
    password = []
    password_letters = []
    hash_val = str(gen_random_num())
    hash_arr = []
    for i in hash_val:
        hash_arr.append(i)
    if len(hash_arr) > pass_length.get():
        while len(hash_arr) > pass_length.get():
            hash_arr.pop(-1)
    if len(hash_arr) < pass_length.get():
        hash_val = str(gen_random_num())
        for i in hash_val:
            if len(hash_arr) < pass_length.get():
                hash_arr.append(i)
    for i in hash_arr:
        temp_pass = int(i) * user_rand % 10
        password.append(int(temp_pass))
    if letter_bool.get():
        password_letters = add_letters(password)
        display_text.set(password_letters)
    if symbol_bool.get():
        password_symbols = add_symbols(password)
        display_text.set(password_symbols)
    else:
        display_text.set(password)


def add_letters(password):
    symbol_and_char_spread = random.randint(int(len(password) / 4),
                                            int(len(password) / 2))
    i = 0
    index_template = []
    while i != len(password):
        index_template.append(i)
        i += 1
    i = 0
    while i != symbol_and_char_spread:
        index = random.randint(0, (len(index_template) - 1))
        index_list.append(index_template[index])
        index_template.pop(index)
        i += 1
    for i in range(symbol_and_char_spread):
        rand_letter_index = random.randint(0, len(letters) - 1)
        password[index_list[i]] = letters[rand_letter_index]
    index_list.clear()
    return password


def add_symbols(password):
    symbol_and_char_spread = random.randint(int(len(password) / 4),
                                            int(len(password) / 2))
    i = 0
    index_template = []
    while i != len(password):
        index_template.append(i)
        i += 1
    i = 0
    while i != symbol_and_char_spread:
        index = random.randint(0, (len(index_template) - 1))
        index_list.append(index_template[index])
        index_template.pop(index)
        i += 1
    for i in range(symbol_and_char_spread):
        rand_symbol_index = random.randint(0, len(symbols) - 1)
        password[index_list[i]] = symbols[rand_symbol_index]
    index_list.clear()
    return password


def set_window_state():
    rand_frame.state(newstate='normal')
    rand_frame.grab_set()
    rand_frame.focus()


not_rand_label_text = tk.StringVar()
not_rand_label_text.set("You must generate a random seed using the button at the top of the window.")

not_rand_label = tk.Label(frame, textvariable=not_rand_label_text)

rand_button = tk.Button(frame, text="Generate Seed")
rand_button.configure(command=set_window_state)

slider_label = tk.Label(frame, text="Password Size:")

pass_length_slider = tk.Scale(frame, from_=12, to=32,
                              orient='horizontal', variable=pass_length, state=widget_state.get())

letters_check = tk.Checkbutton(frame, text="Include letters",
                               variable=letter_bool,
                               onvalue=True, offvalue=False, state=widget_state.get())

symbols_check = tk.Checkbutton(frame, text="Include Symbols",
                               variable=symbol_bool,
                               onvalue=True, offvalue=False, state=widget_state.get())

generate_pass_button = ttk.Button(
    frame, text='Generate Password', state=widget_state.get())
generate_pass_button.configure(command=generate_pass)

display_pass = ttk.Entry(frame, textvariable=display_text,
                         state='readonly', width=60, justify='center')


not_rand_label.grid(column=0, row=0, sticky="E")
rand_button.grid(column=0, row=1, stick='W')
slider_label.grid(column=0, row=2, sticky='W')
pass_length_slider.grid(column=0, row=3, sticky='W')
letters_check.grid(column=0, row=4, sticky='w')
symbols_check.grid(column=0, row=5, sticky='w')
generate_pass_button.grid(column=0, row=6, sticky='w')
display_pass.grid(column=0, row=7, columnspan=4, sticky='s')

frame.grid(padx=10, pady=10)

rand_button_disabled_list = []
rand_button_times = []


def rand_button_click(button):

    button.config(state='disabled')
    rand_button_disabled_list.append(button)

    current_time = datetime.now()
    current_microsec = current_time.microsecond
    rand_button_times.append(current_microsec // 11000)
    print(rand_button_times)
    if len(rand_button_disabled_list) == 9:
        rand_frame.withdraw()
        frame.grab_set()
        frame.focus()
        average_time = sum(rand_button_times) / len(rand_button_times)

        
        # fix this shit
        global user_rand
        user_rand = average_time
        widget_state.set('active')
        not_rand_label_text.set('')
        for i in rand_button_disabled_list:
            i.config(state='active')


rand_label = tk.Label(rand_frame,
                      text="Click all of the buttons to create a random seed.")
b1 = tk.Button(rand_frame, text="Button1",
               command=lambda: rand_button_click(b1))
b2 = tk.Button(rand_frame, text="Button2",
               command=lambda: rand_button_click(b2))
b3 = tk.Button(rand_frame, text="Button3",
               command=lambda: rand_button_click(b3))
b4 = tk.Button(rand_frame, text="Button4",
               command=lambda: rand_button_click(b4))
b5 = tk.Button(rand_frame, text="Button5",
               command=lambda: rand_button_click(b5))
b6 = tk.Button(rand_frame, text="Button6",
               command=lambda: rand_button_click(b6))
b7 = tk.Button(rand_frame, text="Button7",
               command=lambda: rand_button_click(b7))
b8 = tk.Button(rand_frame, text="Button8",
               command=lambda: rand_button_click(b8))
b9 = tk.Button(rand_frame, text="Button9",
               command=lambda: rand_button_click(b9))

rand_label.grid(column=0, row=0, columnspan=3, sticky="nsew")
b1.grid(column=0, row=1, sticky="nsew", padx=5, pady=5)
b2.grid(column=1, row=1, sticky="nsew", padx=5, pady=5)
b3.grid(column=2, row=1, sticky="nsew", padx=5, pady=5)
b4.grid(column=0, row=2, sticky="nsew", padx=5, pady=5)
b5.grid(column=1, row=2, sticky="nsew", padx=5, pady=5)
b6.grid(column=2, row=2, sticky="nsew", padx=5, pady=5)
b7.grid(column=0, row=3, sticky="nsew", padx=5, pady=5)
b8.grid(column=1, row=3, sticky="nsew", padx=5, pady=5)
b9.grid(column=2, row=3, sticky="nsew", padx=5, pady=5)

rand_frame.rowconfigure((0, 1, 2, 3), weight=1)
rand_frame.columnconfigure((0, 1, 2), weight=1)


root.mainloop()
