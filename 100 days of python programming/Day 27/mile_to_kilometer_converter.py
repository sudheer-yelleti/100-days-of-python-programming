from tkinter import *

window = Tk()
window.title("Mile to Kilometer Converter")
window.config(padx=20, pady=20)


def convert():
    miles = float(miles_input.get())
    kilometers = miles * 1.60934
    kilometers_output.config(text=f"{kilometers:.2f}")


miles_input = Entry(width=5)
miles_input.grid(row=0, column=1)

miles_label = Label(text="Miles")
miles_label.grid(row=0, column=2)

is_equal_label = Label(text="is equal to")
is_equal_label.grid(row=1, column=0)

kilometers_output = Label(text="0")
kilometers_output.grid(row=1, column=1)

kilometers_label = Label(text="Kilometers")
kilometers_label.grid(row=1, column=2)

calc_button = Button(text="Calculate", command=convert)
calc_button.grid(row=2, column=1)

window.mainloop()
