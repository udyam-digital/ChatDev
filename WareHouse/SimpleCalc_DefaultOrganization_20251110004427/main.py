'''
This file contains the CalculatorApp class which implements a simple GUI calculator
that can perform addition, subtraction, multiplication, and division of two numbers.
'''
import tkinter as tk
from tkinter import messagebox
class CalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Simple Calculator")
        # Create input fields
        self.first_number = tk.Entry(master)
        self.first_number.grid(row=0, column=1)
        self.second_number = tk.Entry(master)
        self.second_number.grid(row=1, column=1)
        # Create labels
        tk.Label(master, text="First Number").grid(row=0, column=0)
        tk.Label(master, text="Second Number").grid(row=1, column=0)
        # Create buttons
        tk.Button(master, text="Add", command=self.add).grid(row=2, column=0)
        tk.Button(master, text="Subtract", command=self.subtract).grid(row=2, column=1)
        tk.Button(master, text="Multiply", command=self.multiply).grid(row=3, column=0)
        tk.Button(master, text="Divide", command=self.divide).grid(row=3, column=1)
        tk.Button(master, text="Clear", command=self.clear).grid(row=4, column=0, columnspan=2)
        # Result label
        self.result_label = tk.Label(master, text="Result: ")
        self.result_label.grid(row=5, column=0, columnspan=2)
    def add(self):
        result = self.get_numbers()
        if result is not None:
            self.result_label.config(text=f"Result: {result[0] + result[1]}")
    def subtract(self):
        result = self.get_numbers()
        if result is not None:
            self.result_label.config(text=f"Result: {result[0] - result[1]}")
    def multiply(self):
        result = self.get_numbers()
        if result is not None:
            self.result_label.config(text=f"Result: {result[0] * result[1]}")
    def divide(self):
        result = self.get_numbers()
        if result is not None:
            if result[1] == 0:
                messagebox.showerror("Error", "Cannot divide by zero")
            else:
                self.result_label.config(text=f"Result: {result[0] / result[1]}")
    def clear(self):
        self.first_number.delete(0, tk.END)
        self.second_number.delete(0, tk.END)
        self.result_label.config(text="Result: ")
    def get_numbers(self):
        try:
            first = float(self.first_number.get())
            second = float(self.second_number.get())
            return first, second
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers")
            return None
def main():
    root = tk.Tk()
    calculator = CalculatorApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()