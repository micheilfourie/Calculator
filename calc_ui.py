from tkinter import *
from calc_event_handler import CalculatorUI


def main():

    root = Tk()
    root.title("Micheil's Calculator")

    textfield1 = Text(
        root,
        width=34,
        height=1,
        font=("Helvetica", 12),
        bd=0,
        bg="#161c20",
        fg="#F5F5F5",
    )
    textfield1.grid(row=0, column=0, columnspan=4, padx=3, pady=3)

    textfield2 = Text(
        root,
        width=21,
        height=1,
        font=("Helvetica", 20, "bold"),
        bd=0,
        bg="#161c20",
        fg="#F5F5F5",
    )
    textfield2.grid(row=1, column=0, columnspan=4, padx=3, pady=3)

    calculator_ui = CalculatorUI(textfield1, textfield2)

    # Add tag "right" to justify text
    textfield1.tag_configure("right", justify=RIGHT)
    textfield2.tag_configure("right", justify=RIGHT)

    # Tuple containing (Button text, Row position and Column Position)
    buttons = (
        ("1", 6, 0),
        ("2", 6, 1),
        ("3", 6, 2),
        ("+", 6, 3),
        ("4", 5, 0),
        ("5", 5, 1),
        ("6", 5, 2),
        ("\u002D", 5, 3),  # minus symbol
        ("7", 4, 0),
        ("8", 4, 1),
        ("9", 4, 2),
        ("x", 4, 3),
        ("C", 2, 2),
        ("\u232B", 2, 3),  # backspace symbol
        ("0", 7, 1),
        ("=", 7, 3),
        ("%", 2, 0),
        ("x²", 3, 1),
        ("÷", 3, 3),
        ("±", 7, 0),
        (",", 7, 2),
        ("√x", 3, 2),
        ("CE", 2, 1),
        ("1/x", 3, 0),
    )

    # Create Buttons using the buttons tuple
    for text, row, col in buttons:
        btn = Button(
            root,
            text=text,
            width=6,
            height=1,
            font=("Helvetica", 15, "bold"),
            bg="#2b373f",
            fg="#F5F5F5",
            bd=0,
        )
        btn.grid(row=row, column=col, padx=3, pady=3)
        btn.bind("<Button-1>", calculator_ui.click)

    # Starts window with 0 displayed in txtfields
    def display():
        textfield1.insert(END, "0")
        textfield2.insert(END, "0")
        textfield1.tag_add(RIGHT, "1.0", END)
        textfield2.tag_add(RIGHT, "1.0", END)
        calculator_ui.calculator.set_expression("0")
        textfield1.config(state=DISABLED)
        textfield2.config(state=DISABLED)

    # Create Keypress Events
    root.bind("<KeyPress>", calculator_ui.key_press)
    root.bind("<Return>", calculator_ui.key_return_press)
    root.bind("<BackSpace>", calculator_ui.backspace_press)

    root.attributes("-alpha", 0.98)
    root["bg"] = "#161c20"
    root.resizable(False, False)
    root.after_idle(display)
    root.mainloop()


if __name__ == "__main__":
    main()
