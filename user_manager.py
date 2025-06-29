import pandas as pd
import os #It offers functions that allow you to create, delete files, and perform path operations.
import hashlib
from user import User

class UserManager:

    _COLUMNS = ['first_name', 'last_name', 'email', 'password', 'age']

    def __init__(self, file_name="users.xlsx"):
        self.file_name = file_name
        self.users = self._load_users()

    @staticmethod
    def _hash_password(password):#if here self or cls we can’t use @staticmethod
        """Hashes the given password with SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()
    #encode text convert the computer language
    #hashlib.256 Encrypts using hashlib.256 algorithm
    #.hexdiges() so that it can be read by people

    def _load_users(self):
        if not os.path.exists(self.file_name):#Checks if the specified file exists
            try:#When the program runs, it checks the Excel file, if not, it recreates it.
                df = pd.DataFrame(columns=self._COLUMNS)
                df.to_excel(self.file_name, index=False)
                return []
            except IOError:
                return []
        try:
            df = pd.read_excel(self.file_name)
            #Check columns for accuracy
            if not all(col in df.columns for col in self._COLUMNS):
                # Return empty list if columns are missing or incorrect
                return []
            return [
                User(row['first_name'], row['last_name'], row['email'], row['password'], row['age'])
                for _, row in df.iterrows()
            ]
        except Exception:
            return []

    def _save_users(self):
        try:
            user_data = [vars(u) for u in self.users]#{'first_name': 'Ali', 'last_name': 'Veli', 'email': 'a@b.com'}
            df = pd.DataFrame(user_data, columns=self._COLUMNS)#columns=self._COLUMNS statement ensures that the columns are in a certain order
            df.to_excel(self.file_name, index=False)
        except IOError:
            pass

    def check_email_exists(self, email):
        return any(user.email == email for user in self.users)

    def register_user(self, first_name, last_name, email, password, age):
        """
            Registers a new user.
        Returns "True" if successful, "False" if the email already exists.
        """
        if self.check_email_exists(email):
            return False  # unsuccsessful: E-posta available

        hashed_password = self._hash_password(password)
        new_user = User(first_name, last_name, email, hashed_password, age)
        self.users.append(new_user) #used to add a new element to the end of the list
        self._save_users()
        return True  # success

    def login(self, email, password):

        hashed_password = self._hash_password(password)
        for user in self.users:
            if user.email == email and user.password == hashed_password:
                return True  # success entry
        return False  # unsuccsessful entry