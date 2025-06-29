import tkinter as tk
from tkinter import messagebox
from user_manager import UserManager


class RegisterWindow(tk.Toplevel):
    def __init__(self, parent, manager):
        super().__init__(parent) #Before customizing your own window by calling tk.Toplevel, it loads its standard features.

        self.manager = manager
        self.title("Register")
        self.geometry("300x220")
        self.configure(bg="#323232")
        self.transient(parent) #It stays connected to the main window. If the main window shrinks, it also shrinks.
        self.grab_set() #1.As long as this window is open, the user cannot interact with any other window.
        self.entries = {} #dictionary
        fields = ["Name", "Surname", "Email", "Password", "Age"]

        for i, field in enumerate(fields): #You start a loop for each element.
            tk.Label(self, text=field + ":",bg="#323232",fg="orange",font="bold").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(self,bg="#626262",fg="orange",font="bold", show="*" if field == "Password" else None)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry

        register_button = tk.Button(self, text="Register", command=self._attempt_register, bg="#626262",fg="orange",font="bold")
        register_button.grid(row=len(fields), columnspan=2, pady=10,padx= 10,sticky="ew") #grid = It divides the screen
        # into rows and columns like a table, making it easy to place products on the screen.
    def _attempt_register(self):
        fname = self.entries["Name"].get()
        lname = self.entries["Surname"].get()
        email = self.entries["Email"].get()
        password = self.entries["Password"].get()
        age_str = self.entries["Age"].get()

        if not all([fname, lname, email, password, age_str]):
            messagebox.showwarning("Warning", "All fields must be filled.", parent=self)
            return

        if self.manager.check_email_exists(email):
            messagebox.showerror("Error", "Email already exists.", parent=self)#It makes the incoming error
                                                                                            # message open on top of it.
            return

        #age messagebox
        try:
            age = int(age_str)
            if age < 18:
                messagebox.showerror("Error", "You must be at least 18 years old.", parent=self)
                return
            if age > 100:
                messagebox.showerror("Error", "Please enter a valid age.", parent=self)
                return
        except ValueError:
            messagebox.showerror("Error", "Age must be a number.", parent=self)
            return


        if self.manager.register_user(fname, lname, email, password, age):
            messagebox.showinfo("Success", "Account created successfully!", parent=self)
            self.destroy() #When you press the "Done" button on the success page, it also causes the register page to close.
        else:
            messagebox.showerror("Error", "Could not create account.", parent=self)

class LoginWindow(tk.Toplevel):
    def __init__(self, parent, manager):
        super().__init__(parent) #Before customizing your own window by calling
                                # tk.Toplevel, it loads its standard features.
        self.manager = manager
        self.title("Log In")
        self.geometry("300x140")
        self.configure(bg="#323232")
        self.transient(parent)   #It stays connected to the main window. If the main window shrinks, it also shrinks.
        self.grab_set()     #bu pencere açıkken başka pencere ile etkileşim olmaz

        tk.Label(self, text="Email:",bg="#323232",fg="orange",font="bold").grid(row=0, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self,bg="#323232",fg="orange",font="bold")
        self.email_entry.grid(row=0, column=1)

        tk.Label(self, text="Password:",bg="#323232",fg="orange",font="bold").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self, show="*",bg="#323232",fg="orange",font="bold")
        self.password_entry.grid(row=1, column=1)

        login_button = tk.Button(self, text="Log In", command=self._attempt_login, bg="#626262",fg="orange",font="bold")
        login_button.grid(row=2, column=0,columnspan=3,pady=10,padx= 10,sticky="ew") #To stick and align to an edge, sticky() is used.

    def _attempt_login(self):
        #.get() allows retrieving the data entered by the user.
        email = self.email_entry.get()
        password = self.password_entry.get()

        if self.manager.login(email, password):
            messagebox.showinfo("Welcome", "Login successful!", parent=self)
            self.destroy()
        else:
            messagebox.showerror("Error", "Email or password is incorrect.", parent=self)

class App:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.root.title("User Login System")
        self.root.geometry("250x200")
        self.root.configure(bg="#323232")
        tk.Label(self.root, text="Welcome!", font=("Arial", 20),fg="orange", bg="#323232").pack(pady=20)
        #`.pack()` places the text inside the window and makes it visible.
        tk.Button(self.root, text="Register!", command=self._open_register_window, width=20, bg="#626262", fg="orange",font="bold").pack(pady=10)
        tk.Button(self.root, text="Log In!", command=self._open_login_window, width=20, bg="#626262", fg="orange",font="bold").pack(pady=10)

    def _open_register_window(self):
        RegisterWindow(self.root, self.manager)

    def _open_login_window(self):
        LoginWindow(self.root, self.manager)

if __name__ == "__main__":
    root = tk.Tk()
    user_manager_instance = UserManager("users.xlsx")
    app = App(root, user_manager_instance)
    root.mainloop()
#This runs the application and keeps it on the screen.