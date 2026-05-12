# This is a calculator based on tkinter and regular python

# Operations included are basic arithmetic operations such as addition, multiplication, subtraction, division
from typing import Any
import tkinter as tk

# Creating root
root = tk.Tk()

# Set root geometry
root.geometry("500x500")

# Set title of our frame
root.title("Calculator")

# Inserting text-field which is a Label
text_field = tk.Label(root, text="0")
text_field.pack()

# Defining four basic functions to perform calculations
def addition(number_1st: float, number_2nd: float) -> float:
    return number_1st + number_2nd


def subtraction(number_1st: float, number_2nd: float) -> float:
    return number_1st - number_2nd


def multiplication(number_1st: float, number_2nd: float) -> float:
    return number_1st * number_2nd


def division(number_1st: float, number_2nd: float) -> float:
    return number_1st / number_2nd

def append_value(value: str):
    previous_text: str = text_field.cget("text")
    new_text = previous_text + value
    text_field.config(text=new_text)


def clear_values() -> None:
    # Clear text field
    text_field.config(text="0")


def number_buttons(root: tk.Tk):
    # Frame for buttons (using grid inside the frame)
    button_frame = tk.Frame(root)
    button_frame.pack()

    buttons = [
        "7",
        "8",
        "9",
        "/",
        "4",
        "5",
        "6",
        "*",
        "1",
        "2",
        "3",
        "-",
        "0",
        ".",
        "=",
        "+",
        "C",
    ]

    row = 0
    col = 0
    numbers = ".0123456789"
    operators = "+-*/"
    for btn_text in buttons:
        if btn_text in numbers:
            button = tk.Button(
                button_frame,
                text=btn_text,
                width=5,
                height=2,
                command=lambda value=btn_text: append_value(value),
            )
        elif btn_text in operators:
            button = tk.Button(
                button_frame,
                text=btn_text,
                width=5,
                height=2,
                command=lambda value=btn_text: handle_operation(value),
            )
        elif btn_text == "=":
            button = tk.Button(
                button_frame,
                text=btn_text,
                width=5,
                height=2,
                command=evaluate,
            )
        else:
            button = tk.Button(
                button_frame,
                text=btn_text,
                width=5,
                height=2,
                command=clear_values,
            )
        button.grid(row=row, column=col, padx=5, pady=5)

        col += 1
        if col > 3:
            col = 0
            row += 1


# Storing values in a list

values: list[str | float] = []


def handle_operation(operation: str):
    previous_value = float(text_field.cget("text"))
    values.append(previous_value)
    values.append(operation)
    clear_values()


def evaluate() -> None:
    new_value = float(text_field.cget("text"))
    values.append(new_value)

    # Gathering values
    operation: str = str(values[1])

    op_function: Any = all_functions.get(operation)
    text_field.config(text=op_function(values[0], values[-1]))

    values.clear()


# Functions
all_functions = {
    "+": addition,
    "-": subtraction,
    "/": division,
    "*": multiplication,
}

# Creating buttons of different numbers
number_buttons(root)

#Binding function
def key_handler(event:tk.Event):
    key = event.char
    if key.isdigit() or key in ".":
        append_value(key)
    elif key in "+-*/":
        handle_operation(key)
    elif key == "\r":  # Enter key
        evaluate()
    elif key.lower() == "c" or key == 'escape':
        clear_values()

root.bind("<Key>", key_handler)
root.bind("<Escape>", lambda event: clear_values())

# Start root
root.mainloop()
