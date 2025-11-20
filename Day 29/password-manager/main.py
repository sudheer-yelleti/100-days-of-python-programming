from tkinter import *
from tkinter import messagebox

from password_generator import PasswordGenerator


class PasswordSave:
    def __init__(self):
        self.window = Tk()
        self.window.title("Password Manager")
        self.window.config(padx=50, pady=50)

        # Canvas and logo
        canvas = Canvas(width=200, height=200)
        logo_img = PhotoImage(file="logo.png")
        canvas.create_image(100, 100, image=logo_img)
        canvas.grid(row=0, column=1)

        # Labels
        Label(text="Website").grid(row=1, column=0)
        Label(text="Email/Username").grid(row=2, column=0)
        Label(text="Password").grid(row=3, column=0)

        # Entries
        self.website_entry = Entry(width=35)
        self.website_entry.grid(row=1, column=1, columnspan=2)
        self.website_entry.focus()

        self.email_entry = Entry(width=35)
        self.email_entry.grid(row=2, column=1, columnspan=2)
        self.email_entry.insert(0, "sudheer.167@gmail.com")

        self.password_entry = Entry(width=17)
        self.password_entry.grid(row=3, column=1)

        # Buttons
        generate_password_button = Button(text="Generate Password", command=self.generate_password)
        generate_password_button.grid(row=3, column=2)

        add_password_button = Button(text="Add Password", width=36, command=self.save)
        add_password_button.grid(row=4, column=1, columnspan=2)

        self.window.mainloop()

    def generate_password(self):
        generator = PasswordGenerator()
        password = generator.generate_password()
        self.password_entry.delete(0, END)
        self.password_entry.insert(0, password)

    def save(self):
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if len(website) == 0 or len(password) == 0:
            messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
            return

        is_ok = messagebox.askokcancel(
            title=website,
            message=f"These are the details entered:\nEmail: {email}\nPassword: {password}\nClick OK to save."
        )

        if is_ok:
            with open("data.txt", "a") as data_file:
                data_file.write(f"{website} | {email} | {password}\n")

            self.website_entry.delete(0, END)
            self.password_entry.delete(0, END)
            messagebox.showinfo(title="Success", message="Your password has been saved!")


if __name__ == "__main__":
    PasswordSave()
