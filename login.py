# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image

from config import THEME_IMAGE
from home_page import HomeWin
from user_manager import UserManager


def Registration():
    """Init registe and login GUI
    """

    root = Tk()
    width = 900
    height = 400
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    geometry = '%dx%d+%d+%d' % (width,
                                height,
                                (screenwidth - width) / 2,
                                (screenheight - height) / 2)
    root.geometry(geometry)
    # root.geometry('900x400')
    root.title("Anisa - Registration And Sign In")
    root.config(bg='#FFEBCE')
    root.resizable(width=False, height=False)

    user_manager = UserManager()

    def on_enter(event):
        """Envent to control enter password is show *

        :param event: event object
        :return: None
        """
        if c_password_entry.get() == "Only enter if you are signing up!":
            c_password_entry.delete(0, END)
            c_password_entry.config(show="*", fg='black')

    def PWCheck():
        """Checkt user input password is right

        :return: if input is right then return True, or is False
        """
        errors = []

        if password_entry.get() != c_password_entry.get():
            errors.append("Passwords don't match!")

        if len(password_entry.get()) < 8:
            errors.append("Password length must be at least 8 characters!")

        if not any(char.isdigit() for char in password_entry.get()):
            errors.append(
                "Your password must contain at least one numerical alphabet!")

        if not any(char.isalpha() for char in password_entry.get()):
            errors.append(
                "Your password must contain at least one English alphabet!")

        if errors:
            messagebox.showinfo("Error", "\n".join(errors))
            return False

        return True

    def Register():
        """User Register

        :return: None
        """
        if email_cbox.get() == "":
            messagebox.showinfo("Register", "Please input Email!")
        else:
            try:
                if PWCheck():
                    user_manager.register(
                        email_cbox.get(), password_entry.get())
                    messagebox.showinfo("Register", "Register successful!")

            except Exception as e:
                messagebox.showinfo("Register", e)

    def Login():
        """User login

        :return:
        """
        email_get = email_cbox.get()
        password_get = password_entry.get()

        try:
            user = user_manager.login(email_get, password_get)
            messagebox.showinfo("Login", "Login successful!")

            # rember
            if is_chk_remember_passwd.get():
                user_manager.add_user_remember(email_get, password_get)
            else:
                user_manager.delete_user_remember(email_get)
            # toggle_home()
            root.destroy()
            win = HomeWin(user)
            win.mainloop()

        except Exception as e:
            messagebox.showinfo("Login", e)

    def show_password():
        """Show really password instead of *

        :return:
        """
        if password_entry.cget('show') == '':
            password_entry.config(show='*')
            c_password_entry.config(show='*')
        else:
            password_entry.config(show='')
            c_password_entry.config(show='')

    # center frame
    center_frame = Frame(root)
    center_frame.config(pady=60, bg='#000000')
    center_frame.pack(anchor='center', expand=True)

    # Logo Image Resize
    InLogoImage = Image.open(THEME_IMAGE)
    resized_logo = InLogoImage.resize((359, 150), Image.LANCZOS)
    logo_image = ImageTk.PhotoImage(resized_logo)

    # Logo Image Frame
    logo_frame = Frame(center_frame)
    logo_frame.config(bg='#000000')
    logo_frame.grid(row=0, column=0, sticky="NSEW")

    # Print Logo image
    logo_label = Label(logo_frame, image=logo_image, bg='#000000')
    logo_label.grid(row=0, column=0)

    # Register frame
    register_frame = Frame(center_frame)
    register_frame.config(bg='#000000')
    register_frame.grid(row=0, column=1, sticky="NSEW")

    # Button frame
    button_frame = Frame(center_frame)
    button_frame.config(bg='#000000')
    button_frame.grid(row=1, column=1, sticky="NSEW")

    sep_line = Label(
        register_frame,
        text="--------------------------------------------------------------------------------------------",
        bg='#000000',
        fg='white')
    sep_line.grid(row=0, column=0, columnspan=3, sticky='ew')

    sep_line_2 = Label(
        register_frame,
        text="--------------------------------------------------------------------------------------------",
        bg='#000000',
        fg='white')
    sep_line_2.grid(row=4, column=0, columnspan=3, sticky='ew')

    # username label and text entry box
    email_label = Label(register_frame, text="Email", bg='#000000', fg='white')
    email_label.grid(row=1, column=0, pady=5, sticky='w')
    email = StringVar()

    email_cbox = ttk.Combobox(register_frame, width=28)
    email_cbox.grid(row=1, column=1, pady=5, padx=5)

    user_remember = user_manager.get_user_remember()

    email_cbox['value'] = tuple(user_remember.keys())

    def func(event):
        """Select remember password and auto input

        :param event:
        :return:
        """
        password.set(user_remember[email_cbox.get()])
        chk_remember_passwd.select()

    email_cbox.bind("<<ComboboxSelected>>", func)

    # password label and password entry box
    password_label = Label(
        register_frame,
        text="Password",
        bg='#000000',
        fg='white')
    password_label.grid(row=2, column=0, pady=5, sticky='w')
    password = StringVar()
    password_entry = Entry(
        register_frame,
        textvariable=password,
        show='*',
        width=30)
    password_entry.grid(row=2, column=1, pady=5, padx=5)

    # Confirm Password label and entry box
    c_password_label = Label(
        register_frame,
        text="Confirm Password",
        bg='#000000',
        fg='white')
    c_password_label.grid(row=3, column=0, pady=5, sticky='w')
    c_password = StringVar()
    c_password_entry = Entry(
        register_frame,
        textvariable=c_password,
        show='',
        width=30)
    c_password_entry.config(fg='grey')
    c_password_entry.insert(0, "Only enter if you are signing up!")
    c_password_entry.bind('<FocusIn>', on_enter)
    c_password_entry.grid(row=3, column=1, pady=5, padx=5)

    # Show Password button
    show_password_button = Button(
        button_frame,
        text="Show Password",
        width=19,
        command=show_password)
    show_password_button.grid(row=5, column=2, pady=10, padx=5, sticky='e')

    # Register button
    btn_register = Button(
        button_frame,
        text="Register",
        width=19,
        command=Register)
    btn_register.grid(row=5, column=0, pady=10, padx=5, sticky='e')

    # Login button
    btn_login = Button(button_frame, text="Login", width=19, command=Login)
    btn_login.grid(row=5, column=1, pady=10, padx=5, sticky='e')

    # add check box
    is_chk_remember_passwd = IntVar()
    chk_remember_passwd = Checkbutton(
        button_frame,
        text="Remember Password",
        variable=is_chk_remember_passwd,
        onvalue=1,
        offvalue=0)
    chk_remember_passwd.grid(row=6, column=0, pady=10, padx=0, sticky='w')

    # Close the window
    def on_closing():
        """When Form will closing, this can promot user quite info.

        :return:
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    def toggle_home():
        """Destroy this form then to add nex form

        :return:
        """
        root.destroy()

    root.mainloop()


# Entry Point
if __name__ == '__main__':
    Registration()