import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class CalculatorWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.__registrationframe = ctk.CTkFrame(master=parent)
        self.__registrationframe.grid(row=0, column=0)

        username_entry = ctk.CTkEntry(master=self.__registrationframe, placeholder_text="Wow")
        username_entry.pack(padx=10, pady=8)
        password_entry = ctk.CTkEntry(master=self.__registrationframe, placeholder_text="Wow", show="*")
        password_entry.pack(padx=10, pady=8)

        self.hide()
    
    def hide(self):
        self.__registrationframe.grid_forget()

    def show(self):
        self.__registrationframe.grid(row=0, column=0)

class LoginWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.__loginframe = ctk.CTkFrame(master=parent)
        self.__loginframe.grid(row=0, column=0, sticky=ctk.E+ctk.W+ctk.S+ctk.N)

        login_label = ctk.CTkLabel(master=self.__loginframe, text="Login")
        login_label.pack(padx=10, pady=8)

        username_entry = ctk.CTkEntry(master=self.__loginframe, placeholder_text="Username")
        username_entry.pack(padx=10, pady=8)
        password_entry = ctk.CTkEntry(master=self.__loginframe, placeholder_text="Password", show="*")
        password_entry.pack(padx=10, pady=8)

        self.hide()

    def hide(self):
        self.__loginframe.grid_forget()

    def show(self):
        self.__loginframe.grid(row=0, column=0)


class RegistrationWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.__registrationframe = ctk.CTkFrame(master=parent)
        self.__registrationframe.grid(row=0, column=0)

        login_label = ctk.CTkLabel(master=self.__registrationframe, text="Register")
        login_label.pack(padx=10, pady=8)

        username_entry = ctk.CTkEntry(master=self.__registrationframe, placeholder_text="Wow")
        username_entry.pack(padx=10, pady=8)
        password_entry = ctk.CTkEntry(master=self.__registrationframe, placeholder_text="Wow", show="*")
        password_entry.pack(padx=10, pady=8)

        self.hide()
    
    def hide(self):
        self.__registrationframe.grid_forget()

    def show(self):
        self.__registrationframe.grid(row=0, column=0)


class View:
    def __init__(self):
        self.__window = ctk.CTk()
        self.__window.resizable(width=0,height=0)
        self.__window.columnconfigure(0, minsize=225)

        self.__frames = {"login": LoginWindow(self.__window), "registration": RegistrationWindow(self.__window), "test": RegistrationWindow(self.__window)}
        self.__current_frame = self.__frames["login"]

        login_button = ctk.CTkButton(master=self.__window, text="Login", command=self.login)
        login_button.grid(row=1, column=0, pady=5)

        calc_button = ctk.CTkButton(master=self.__window, text="calc", command=self.calculator)
        calc_button.grid(row=2, column=0, pady=5)

        reg_button = ctk.CTkButton(master=self.__window, text="reg", command=self.registration)
        reg_button.grid(row=3, column=0, pady=5)

        reg_label = ctk.CTkLabel(master=self.__window, text="Create an account?", cursor="hand2")
        reg_label.bind("<Button-1>", lambda e: self.registration if isinstance(LoginWindow, self.__current_frame) else self.login)
        reg_label.grid(row=4, column=0, pady=5)

        self.__frames["login"].show()

        self.__window.mainloop()

    def calculator(self):
        self.__current_frame.hide()
        self.__frames["calculator"].show()
        self.__current_frame = self.__frames["calculator"]

    def login(self):
        self.__current_frame.hide()
        self.__frames["login"].show()
        self.__current_frame = self.__frames["login"]

    def registration(self):
        self.__current_frame.hide()
        self.__frames["registration"].show()
        self.__current_frame = self.__frames["registration"]

window = View()
