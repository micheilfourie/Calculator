from tkinter import *
from calc_logic import Calculator
from string import digits
import re


class CalculatorUI:

    def __init__(self, textfield1, textfield2):
        self.calculator = Calculator()
        self.textfield1 = textfield1
        self.textfield2 = textfield2
        self.errFlag = False

    # Simplify clear and update event operations >>> Start

    def clear_txt1(self):
        self.textfield1.delete(1.0, END)

    def clear_txt2(self):
        self.textfield2.delete(1.0, END)

    def clear_all(self):
        self.calculator.clear_expression()
        self.clear_txt1()
        self.clear_txt2()

    def clear_update_txt1(self):
        self.clear_txt1()
        expr = self.refactor_expr(self.calculator.get_expression())
        self.textfield1.insert(END, expr)

    def clear_update_txt2(self):
        self.clear_txt2()
        expr = self.refactor_expr(self.calculator.get_expression())
        self.textfield2.insert(END, expr)

    def clear_update_all(self):
        self.clear_update_txt1()
        self.clear_update_txt2()

    # >>> End

    # Refactor expression for proper display in txtfields
    def refactor_expr(self, expr):

        def resub(expr):
            return re.sub(r"(\d)(?=(\d{3})+(?!\d))", r"\1 ", expr)

        def handle_comma(expr):
            lst = []
            if "." in expr:
                lst = expr.split(".")
                expr = resub(lst[0]) + f".{lst[1]}"
            else:
                expr = resub(expr)

            return expr

        def handle_operator(expr):
            lst = []
            operator = ""
            new_lst = []

            for x in expr:
                if x in self.calculator.get_operators():
                    operator = x
                    lst = expr.split(x)

                    for x in range(0, 2):
                        new_lst.append(handle_comma(lst[x]))

            return operator.join(new_lst)

        if not self.check_err():

            if self.calculator.check_expression_for_operator():

                if not expr[0] == "\u002D":
                    expr = handle_operator(expr)
                else:
                    expr = "\u002D" + handle_operator(expr[1:])

            else:
                expr = handle_comma(expr)

            return expr

        else:
            return expr

    # Checks if expression contains an operator
    def check_expression(self):
        if self.calculator.check_expression_for_operator():
            result = self.calculator.evaluate_expression()
            self.calculator.clear_expression()
            self.calculator.update_expression(result)
            self.clear_update_all()

    # Check expression for error
    def check_err(self):
        expr = self.calculator.get_expression()
        err_lst = ["Err", "Can't divide by zero", "Result too large"]
        return True if expr in err_lst else False

    # Replace operator if new operator is entered
    def replace_operator(self, operator):
        self.calculator.replace_operator(operator)

    def expr_and_txt_zero(self):
        self.calculator.set_expression("0")
        self.textfield1.insert(END, "0")
        self.textfield2.insert(END, "0")

    # Keypress event listener
    def key_press(self, event):
        numpad_operators = ("*", "/", "+", "-", ".", ",")
        key = event.char
        if key in digits or key in numpad_operators:
            self.process_event(key)

    # Return (Enter) event listener
    def key_return_press(self, event):
        if event.keysym == "Return":
            self.process_event("=")

    # Backspace event listener
    def backspace_press(self, event):
        if event.keysym == "BackSpace":
            self.process_event("\u232B")

    # Click event listener
    def click(self, event):
        text = event.widget.cget("text")
        self.process_event(text)

    # Process Click, KeyPress, Return and Backspace events
    def process_event(self, text):

        # Temporarily Enable textfields to display text
        self.textfield1.config(state=NORMAL)
        self.textfield2.config(state=NORMAL)

        # Ensure error is displayed first
        if self.errFlag:
            self.clear_all()
            self.errFlag = False

        # Button > Equals
        if text == "=":

            result = ""
            if not "=" in self.textfield1.get(1.0, END) and not self.check_err():
                result = str(self.calculator.evaluate_expression())
                self.textfield1.insert(END, "=")
                self.clear_txt2()
                self.calculator.set_expression(result)
                expr = self.calculator.get_expression()
                expr = self.refactor_expr(expr)
                self.textfield2.insert(END, expr)

            if result == "Err":
                self.errFlag = True

        # Button > Clear All
        elif text == "C" or text == "CE":
            self.clear_all()
            self.expr_and_txt_zero()

        # Button > Backspace
        elif text == "\u232B":
            expr = self.calculator.get_expression()

            if self.check_err():
                self.clear_all()
                self.expr_and_txt_zero()
            else:
                self.calculator.backspace()

            self.clear_update_all()

        # Button > Pow of 2, Sqrt and Reciprocal of 1
        elif text in ["x²", "√x", "1/x"]:
            if not self.check_err():
                result = ""
                self.clear_txt1()
                if text == "x²":
                    result = self.calculator.square()
                    expr = self.refactor_expr(self.calculator.get_expression())
                    self.textfield1.insert(END, f"{expr}²")
                elif text == "√x":
                    result = self.calculator.sqrt()
                    expr = self.refactor_expr(self.calculator.get_expression())
                    self.textfield1.insert(END, f"√{expr}")
                else:
                    result = self.calculator.reciprocal()
                    expr = self.refactor_expr(self.calculator.get_expression())
                    self.textfield1.insert(END, f"1/{expr}")

                self.clear_txt2()
                self.calculator.set_expression(str(result))
                expr = self.refactor_expr(self.calculator.get_expression())
                self.textfield2.insert(END, expr)

        # Button > Toggle pos/neg
        elif text == "±":
            if not self.check_err():
                self.calculator.toggle_negative()
                self.clear_update_all()

        # Button > Decimal
        elif text == "," or text == ".":
            if not self.calculator.check_expr_for_dupe(".") and not self.check_err():
                self.calculator.update_expression(".")
                self.clear_update_all()

        # Buttons > Multiply, Division, Plus, Minus
        elif text in ["x", "*", "÷", "/", "+", "\u002D", "-"]:
            text = text.replace("x", "*").replace("÷", "/").replace("-", "\u002D")

            if not self.calculator.check_expr_for_dupe(text) and not self.check_err():
                self.check_expression()
                self.calculator.update_expression(text)
            else:
                self.replace_operator(text)

            if not self.check_err():
                self.clear_update_all()

        # Button > Zero
        elif text == "0":
            if not self.calculator.check_expr_for_dupe("0"):
                if self.check_err():
                    self.calculator.set_expression(text)
                else:
                    self.calculator.update_expression(text)
                self.clear_update_all()

        # Button > Percentage
        elif text == "%":
            if not self.check_err():
                lst = self.calculator.percentage()
                expr = ""
                if not len(lst) == 1:
                    self.clear_txt1()
                    expr = self.refactor_expr(lst[0])
                    self.textfield1.insert(END, f"{expr}%=")
                    self.clear_txt2()
                    expr = self.refactor_expr(lst[1])
                    self.textfield2.insert(END, str(expr))

        # Other buttons
        else:
            if not self.calculator.check_expr_for_dupe("0") and not self.check_err():
                self.calculator.update_expression(text)
                self.clear_update_all()

            else:
                if self.calculator.get_expression()[0] == "\u002D":
                    self.calculator.set_expression(f"\u002D{text}")
                else:
                    self.calculator.set_expression(text)

                self.clear_update_all()

        # Apply created tag to justify textfields to the right
        self.textfield1.tag_add(RIGHT, "1.0", END)
        self.textfield2.tag_add(RIGHT, "1.0", END)

        # Disables textfields again
        self.textfield1.config(state=DISABLED)
        self.textfield2.config(state=DISABLED)
