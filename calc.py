import customtkinter as ctk
import communicator
from functools import partial

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

SYMBOLS = ["1", "2", "3", "+", "4", "5", "6", "-", "7", "8", "9", "*", "^", "0", "=", "/"]

class CalculatorWindow(ctk.CTkFrame):
    def __init__(self, mainwindow, parent):
        super().__init__(parent)
        self.__mw = mainwindow

        self.__calculatorframe = ctk.CTkFrame(master=parent)
        self.__calculatorframe.grid(row=0, column=0)

        self.__equation_label = ctk.CTkLabel(master=self.__calculatorframe, text="")
        self.__equation_label.grid(row=0, column=0, columnspan=4)

        buttoncount = 0

        for x in range(4):
            for y in range(4):
                self.create_symbolbutton(SYMBOLS[buttoncount], x, y)
                buttoncount += 1

        refresh_button = ctk.CTkButton(master=self.__calculatorframe, text="Refresh",
                                        height=60, width=60, command = lambda: self.post("Refresh"))
        refresh_button.grid(row=5, column=0, columnspan=1)

        backspace_button = ctk.CTkButton(master=self.__calculatorframe, text="Erase",
                                        height=60, width=60, command = lambda: self.post("Erase"))
        backspace_button.grid(row=5, column=1, columnspan=1)

        refresh_button = ctk.CTkButton(master=self.__calculatorframe, text="Reset",
                                height=60, width=120, command = lambda: self.post("Reset"))
        refresh_button.grid(row=5, column=2, columnspan=2)

        self.hide()
    
    def create_symbolbutton(self, symbol, x, y):
        symbol_button = ctk.CTkButton(master=self.__calculatorframe, text=symbol,
                                              width=60, height=60, command = lambda: self.post(symbol))
        symbol_button.grid(row=1+x, column=y)

    def hide(self):
        self.__calculatorframe.grid_forget()

    def show(self):
        self.__calculatorframe.grid(row=0, column=0)

    def update_screen(self, response):
        if "error" in response:
            self.__equation_label.configure(text=str(response["error"]))
        else:
            self.__equation_label.configure(text=(str(response["num1"]) + str(response["operator"]) + str(response["num2"])))

    def post(self, code):
        if code == "Erase":
            response = self.__mw.erase()
        elif code == "Reset":
            response = self.__mw.reset()
        elif code == "Refresh":
            response = self.__mw.status()
        elif code == "=":
            response = self.__mw.equals()
        else:
            response = self.__mw.send(code)

        self.update_screen(response)


class LoginWindow(ctk.CTkFrame):
    def __init__(self, mainwindow, parent):
        super().__init__(parent)
        self.__mw = mainwindow
        self.__loginframe = ctk.CTkFrame(master=parent)
        self.__loginframe.grid(row=0, column=0, sticky=ctk.E+ctk.W+ctk.S+ctk.N)
        self.__loginframe.columnconfigure(index=0, minsize=450)

        login_label = ctk.CTkLabel(master=self.__loginframe, text="Login")
        login_label.pack(padx=10, pady=8)

        self.__error_label = ctk.CTkLabel(master=self.__loginframe, text="")
        self.__error_label.pack(padx=0, pady=0)

        self.__username_entry = ctk.CTkEntry(master=self.__loginframe, placeholder_text="Username")
        self.__username_entry.pack(padx=10, pady=8)
        self.__password_entry = ctk.CTkEntry(master=self.__loginframe, placeholder_text="Password", show="*")
        self.__password_entry.pack(padx=10, pady=8)

        credential_button = ctk.CTkButton(master=self.__loginframe, text="Login", command=self.log)
        credential_button.pack(padx=10, pady=8)

        credential_label = ctk.CTkButton(master=self.__loginframe, text="Create an account?", command=self.move_to_reg)
        credential_label.pack(padx=10, pady=8)

    def hide(self):
        self.__loginframe.grid_forget()

    def show(self):
        self.__loginframe.grid(row=0, column=0)
    
    def log(self):
        self.__mw.log([self.__username_entry.get(), self.__password_entry.get()])

    def display_error(self, string):
        self.__error_label.configure(text=string)

    def move_to_reg(self):
        self.__mw.move_to_reg()


class RegistrationWindow(ctk.CTkFrame):
    def __init__(self, mainwindow, parent):
        super().__init__(parent)
        self.__mw = mainwindow
        self.__registrationframe = ctk.CTkFrame(master=parent)
        self.__registrationframe.grid(row=0, column=0)

        register_label = ctk.CTkLabel(master=self.__registrationframe, text="Register")
        register_label.pack(padx=10, pady=8)

        self.__error_label = ctk.CTkLabel(master=self.__registrationframe, text="")
        self.__error_label.pack(padx=0, pady=0)

        self.__username_entry = ctk.CTkEntry(master=self.__registrationframe, placeholder_text="Choose a username")
        self.__username_entry.pack(padx=10, pady=8)
        self.__password_entry = ctk.CTkEntry(master=self.__registrationframe, placeholder_text="Choose a password", show="*")
        self.__password_entry.pack(padx=10, pady=8)

        credential_button = ctk.CTkButton(master=self.__registrationframe, text="Register", command=self.reg)
        credential_button.pack(padx=10, pady=8)

        credential_label = ctk.CTkButton(master=self.__registrationframe, text="Have an account?", command=self.move_to_log)
        credential_label.pack(padx=10, pady=8)

        self.hide()
    
    def hide(self):
        self.__registrationframe.grid_forget()

    def show(self):
        self.__registrationframe.grid(row=0, column=0)

    def reg(self):
        self.__mw.reg([self.__username_entry.get(), self.__password_entry.get()])

    def move_to_log(self):
        self.__mw.move_to_log()


class Calc:
    def __init__(self, cm):
        self.__window = ctk.CTk()
        self.__window.resizable(False,False)
        self.__cm = cm
        self.__token = None

        self.__frames = {"login": LoginWindow(self, self.__window), "registration": RegistrationWindow(self, self.__window), "calculator": CalculatorWindow(self, self.__window)}
        self.__current_frame = self.__frames["login"]

        self.__frames["login"].show()
        self.__window.mainloop()

    def move_to_log(self):
        self.__current_frame.hide()
        self.__frames["login"].show()
        self.__current_frame = self.__frames["login"]

    def move_to_reg(self):
        self.__current_frame.hide()
        self.__frames["registration"].show()
        self.__current_frame = self.__frames["registration"]

    def move_to_calc(self, login_data):
        self.__current_frame.hide()
        self.__frames["calculator"].show()
        self.__current_frame = self.__frames["calculator"]
        self.__current_frame.update_screen(login_data)


    def log(self, credentials):
        print(credentials)
        login_data = cm.on_login(credentials)
        if "error" in login_data:
            self.__current_frame.display_error(login_data["error"])
        else:
            self.__token = login_data["token"]
            self.move_to_calc(login_data)

    def reg(self, credentials):
        if cm.on_register(credentials):
            self.move_to_log()
    
    def send(self, symbol):
        return cm.on_post(symbol, self.__token)

    def status(self):
        return cm.get_status(self.__token)
    
    def equals(self):
        return cm.equals(self.__token)
    
    def reset(self):
        return cm.on_reset(self.__token)
    
    def erase(self):
        return cm.erase(self.__token)

if __name__ == "__main__":
    cm = communicator.Communicator()
    calc = Calc(cm)
