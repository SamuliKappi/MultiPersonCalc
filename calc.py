import customtkinter as ctk
import communicator

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

        self.__username_entry = ctk.CTkEntry(master=self.__loginframe, placeholder_text="Username")
        self.__username_entry.pack(padx=10, pady=8)
        self.__password_entry = ctk.CTkEntry(master=self.__loginframe, placeholder_text="Password", show="*")
        self.__password_entry.pack(padx=10, pady=8)

        self.hide()

    def hide(self):
        self.__loginframe.grid_forget()

    def show(self):
        self.__loginframe.grid(row=0, column=0)

    def return_credentials(self):
        return [self.__username_entry.get(), self.__password_entry.get()]


class RegistrationWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.__registrationframe = ctk.CTkFrame(master=parent)
        self.__registrationframe.grid(row=0, column=0)

        login_label = ctk.CTkLabel(master=self.__registrationframe, text="Register")
        login_label.pack(padx=10, pady=8)

        self.__username_entry = ctk.CTkEntry(master=self.__registrationframe, placeholder_text="Choose a username")
        self.__username_entry.pack(padx=10, pady=8)
        self.__password_entry = ctk.CTkEntry(master=self.__registrationframe, placeholder_text="Choose a password", show="*")
        self.__password_entry.pack(padx=10, pady=8)

        self.hide()
    
    def hide(self):
        self.__registrationframe.grid_forget()

    def show(self):
        self.__registrationframe.grid(row=0, column=0)

    def return_credentials(self):
        return [self.__username_entry.get(), self.__password_entry.get()]


class Calc:
    def __init__(self, communicator):
        self.__window = ctk.CTk()
        self.__window.resizable(width=0,height=0)
        self.__cm = communicator

        self.__frames = {"login": LoginWindow(self.__window), "registration": RegistrationWindow(self.__window), "calculator": RegistrationWindow(self.__window)}
        self.__current_frame = self.__frames["login"]

        credential_button = ctk.CTkButton(master=self.__window, text="Login", command=self.log_or_reg)
        credential_button.grid(row=1, column=0, pady=5)

        credential_label = ctk.CTkLabel(master=self.__window, text="Create an account?", cursor="hand2")
        credential_label.bind("<Button-1>", lambda e: self.move_to_log_or_reg())
        credential_label.grid(row=4, column=0, pady=5)

        self.__frames["login"].show()
        self.__window.mainloop()

    def move_to_log_or_reg(self):
        if isinstance(self.__current_frame, LoginWindow):
            self.__current_frame.hide()
            self.__frames["registration"].show()
            self.__current_frame = self.__frames["registration"]
        else:
            self.__current_frame.hide()
            self.__frames["login"].show()
            self.__current_frame = self.__frames["login"]

    def log_or_reg(self):
        credentials = self.__current_frame.return_credentials()

        if isinstance(self.__current_frame, LoginWindow):
            if cm.on_login(credentials):
                self.__current_frame.hide()
                self.__frames["calculator"].show()
                self.__current_frame = self.__frames["calculator"]
        else:
            if cm.on_register(credentials):
                self.__current_frame.hide()
                self.__frames["login"].show()
                self.__current_frame = self.__frames["login"]


if __name__ == "__main__":
    cm = communicator.Communicator()
    calc = Calc(cm)
