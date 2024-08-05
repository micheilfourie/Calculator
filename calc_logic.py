import math


class Calculator:

    def __init__(self):
        self.expression = ""
        self.operators = ("*", "/", "+", "\u002D")

    def get_expression(self):
        return self.expression

    def get_expr_last(self):
        return self.expression[-1]

    def get_operators(self):
        return self.operators

    def set_expression(self, expr):
        self.expression = expr

    # Concatinate Expression
    def update_expression(self, text):
        self.expression += text

    # Clear Expression
    def clear_expression(self):
        self.expression = ""

    # Replace operator if new operator is entered
    def replace_operator(self, operator):
        last_char = self.get_expr_last()
        if self.check_expression_for_operator() and last_char in self.operators:
            if self.expression[0] == "\u002D":
                self.expression = self.expression[1:].replace(last_char, operator)
            else:
                self.expression = self.expression.replace(last_char, operator)

    # Check if expression contains an operator
    def check_expression_for_operator(self):
        expr = self.expression
        for x in self.operators:
            if x in expr:
                return False if list(expr).index(x) == 0 and x == "\u002D" else True
        return False

    # Check for duplicate operators or zeros
    def check_expr_for_dupe(self, val):
        expr = self.expression
        if val == "0" and "." not in expr and val in expr:
            if val == expr[0] or expr[0] == "\u002D" and val == expr[1]:
                return True
        elif val in self.operators and self.get_expr_last() in self.operators:
            return True
        elif val == "." and "." in expr:
            lst = []
            if self.check_expression_for_operator():
                for x in self.operators:
                    if x in expr:
                        lst = expr.split(x)
                        if not "." in lst[1]:
                            return False
            else:
                return True
        else:
            return False

    # removes operator at the end of expression or calculate the expression to avoid error
    def process_expr(self):
        if self.get_expr_last() in self.operators:
            self.expression = self.expression[:-1]
        elif self.check_expression_for_operator():
            self.expression = str(self.evaluate(self.expression))

    # Parse expression to string and calls evaluate()
    def evaluate_expression(self):
        try:
            return str(self.evaluate(self.expression))
        except Exception as e:
            print(f"Error in evaluate_expression(): {e}")
            return "Err"

    # Handles pow of 2 operation
    def square(self):
        try:
            self.process_expr()
            expr = float(self.expression)
            return int(expr**2) if expr.is_integer() else expr ** 2
        except OverflowError:
            return "Result too large"
        except Exception as e:
            if "e" in self.expression:
                return "Result too large"
            else:
                print(f"Error in square(): {e}")
                return "Err"

    # Handles sqrt operation
    def sqrt(self):
        try:
            self.process_expr()
            expr = math.sqrt(float(self.expression))
            return int(expr) if expr.is_integer() else expr

        except Exception as e:
            print(f"Error in sqrt(): {e}")
            return "Err"

    # Handles reciprocal of 1 operation
    def reciprocal(self):
        try:
            self.process_expr()
            expr = 1 / float(self.expression)
            return int(expr) if expr.is_integer() else expr

        except ZeroDivisionError:
            return "Can't divide by zero"

        except Exception as e:
            print(f"Error in reciprocal(): {e}")
            return "Err"

    # Removes last char of expression (Backspace)
    def backspace(self):
        if len(self.expression) > 1:
            self.expression = self.expression[:-1]
        elif len(self.expression) == 1 and not self.expression[0] == "0":
            self.expression = "0"

    # Make expression negative or positive respectively
    def toggle_negative(self):
        try:
            if self.expression[0] == "\u002D":
                self.expression = self.expression[1:]
            else:
                self.expression = "\u002D" + self.expression
        except Exception as e:
            print(f"Error in toggle_negative(): {e}")
            return "Err"

    def percentage(self):

        def calc_percentage(num1, num2, operator):
            num1 = float(num1)
            num2 = float(num2)
            calc = num1 * num2 / 100

            if operator == "+":
                return num1 + calc

            elif operator == "\u002D":

                return num1 - calc

            elif operator == "*":
                return num1 * calc

            elif operator == "/":
                return num1 / calc

        return_list = [self.expression]

        try:
            if not "\u002D" == self.expression[0]:

                newList = []
                total = 0.0

                if "+" in self.expression:
                    newList = self.expression.split("+")
                    total = calc_percentage(newList[0], newList[1], "+")

                elif "\u002D" in self.expression:
                    newList = self.expression.split("\u002D")
                    total = calc_percentage(newList[0], newList[1], "\u002D")

                elif "*" in self.expression:
                    newList = self.expression.split("*")
                    total = calc_percentage(newList[0], newList[1], "*")

                elif "/" in self.expression:
                    newList = self.expression.split("/")
                    total = calc_percentage(newList[0], newList[1], "/")

                else:
                    return return_list

                if total.is_integer():
                    self.expression = str(int(total))
                else:
                    self.expression = str(total)

                return_list.append(self.expression)
                return return_list

        except Exception as e:
            print(f"Error in percentage(): {e}")
            return ["Err"]

    # Handles +, -, *, and / operations
    def evaluate(self, expr):

        def calc_expr(expr):
            try:
                operator_flag = False
                operation = ""
                total = ""
                num2 = ""
                temp = ""

                if expr == "" or expr == "0":
                    return "0"

                expr = list(expr)

                if expr[0] == "\u002D":
                    temp = expr.pop(0)

                for x in expr:
                    for y in self.operators:
                        if x == y:
                            if expr.index(x) == 0 and not x == "\u002D":
                                return "".join(expr)
                            else:
                                if temp == "":
                                    operation = y
                                    total = "".join(expr[: expr.index(x)])
                                    num2 = "".join(expr[expr.index(x) + 1 :])
                                    operator_flag = True
                                else:
                                    operation = y
                                    total = temp + "".join(expr[: expr.index(x)])
                                    num2 = "".join(expr[expr.index(x) + 1 :])
                                    operator_flag = True

                if not operator_flag:
                    return "".join(expr)

                num2 = float(num2)
                total = float(total)

                if operation == "+":
                    total += num2
                elif operation == "\u002D":
                    total -= num2
                elif operation == "*":
                    total *= num2
                elif operation == "/":
                    if not num2 == 0.0:
                        total /= num2
                    else:
                        return "Can't divide by zero"
                else:
                    return total

                if total.is_integer():

                    return int(total)

                else:
                    return total

            except ValueError:
                return total
            except Exception as e:
                print(f"Error in calc_expr(): {e}")
                return "Err"

        return calc_expr(expr)
