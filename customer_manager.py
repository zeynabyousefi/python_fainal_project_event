import pandas as pd
import hashlib
from file_logging import error_logging, warnning_logging, debug
import datetime
import re

"""
This file for person in system(admin or customer) for sing up or log in.
"""


class Customer:
    """
    This class for customer to sing up or log in ,in system
    """

    def __init__(self):
        self.firstname = ''
        self.lastname = ''
        self.password = ''
        self.username = ''
        self.email = ''
        self.login = False

    def get_info_user(self):
        """
        This method for get information about a user to sing up in system.
        """
        self.firstname = input("Enter your firstname:\n")
        self.lastname = input("Enter your lastname:\n")
        self.username = input("Enter your user name:\n")
        while True:
            try:
                self.email = input("Enter your email:\n")
                pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                find_pattern = re.search(pattern, self.email)
                if find_pattern:
                    break
                else:
                    raise ValueError()
            except ValueError:
                print("email is wrong!please try again")
        self.password = input("Enter your password:\n")
        plaintext = self.password.encode()
        d = hashlib.sha256(plaintext)
        hash_code = d.hexdigest()
        df1 = pd.read_csv("user.csv", sep=",")
        b = df1.loc[
            (df1['email'] == self.email)]
        if len(b) >= 1:
            while True:
                print("Your username is available, please try again")

                break
        else:
            print("Sing up successful!")
            debug("a user add in system")
            df2 = pd.read_csv("user.csv", sep=",")
            c = df2.index.values[-1]
            nextTime = datetime.datetime.now() + datetime.timedelta(minutes=3)
            time = nextTime.strftime("%H:%M")
            df2.loc[c + 1, ['password', 'firstname', 'lastname', 'username', 'stat', 'time_log', 'email']] = [hash_code,
                                                                                                              self.firstname,
                                                                                                              self.lastname,
                                                                                                              self.username,
                                                                                                              'unblock',
                                                                                                              time,
                                                                                                              self.email]
            df2.to_csv('user.csv', index=False)

    def search_info_user(self):
        """
       This method for get information about a user to log  in system.
       if user sent wrong password for 3 attempts his account has been
       blocked for 3 min.
       """
        attempts = 3

        df = pd.read_csv("user.csv", sep=",")
        while attempts > 0:
            attempts -= 1
            self.username = input("Enter your username:\n")
            next_time = datetime.datetime.now()
            time_block = next_time.strftime("%H:%M")
            a = df.loc[(df["username"] == self.username.lower())]

            if len(a) >= 1:
                self.password = input("Enter your password:\n").lower()
                hs = hashlib.sha256(self.password.encode('utf-8')).hexdigest()
                find_user_01 = df.loc[
                    (df["password"] == hs) & (df["username"] == self.username.lower()) & (
                                df["time_log"] <= time_block) & (
                            df["stat"] == 'block')]
                find_user_02 = df.loc[
                    (df["password"] == hs) & (df["username"] == self.username.lower()) & (df["stat"] == 'unblock')]
                find_user_03 = df.loc[
                    (df["password"] == hs) & (df["username"] == self.username.lower()) & (
                                df["time_log"] >= time_block) & (
                            df["stat"] == 'block')]
                if len(find_user_03) >= 1:
                    print("your account is unreachable")
                    break
                f = a.index.values

            else:
                print("Invalid Username...")
                print("You have {} attempts left.".format(attempts))
                continue

            if len(find_user_01) >= 1 or len(find_user_02) >= 1:
                print("Login successful!")
                df2 = pd.read_csv("user.csv", sep=",")
                df2.loc[f, ['stat']] = ['unblock']
                df2.to_csv('user.csv', index=False)
                debug("a user log in ")
                self.login = True
                break
            elif attempts == 0:
                next_time = datetime.datetime.now() + datetime.timedelta(minutes=3)
                time_log = next_time.strftime("%H:%M")
                df2 = pd.read_csv("user.csv", sep=",")
                df2.loc[f, ['time_log', 'stat']] = [time_log, 'block']
                df2.to_csv('user.csv', index=False)
                error_logging("Your account has been blocked")
                break


            else:
                print("Invalid Password...")
                print("You have {} attempts left.".format(attempts))

    def edit_user(self):
        """"
        This method for edit a user after log in (without to change email)
        """
        self.firstname = input("Enter your firstname:\n").lower()
        self.lastname = input("Enter your lastname:\n").lower()
        self.username = input("Enter your user name:\n").lower()
        self.password = input("Enter your password:\n").lower()
        self.email = input("Enter the your email:\n")
        plaintext = self.password.encode()
        d = hashlib.sha256(plaintext)
        hash = d.hexdigest()
        df1 = pd.read_csv("user.csv", sep=",")
        v = df1.loc[df1["email"] == self.email]
        b = df1.loc[
            (df1['password'] == hash) & (df1["firstname"] == self.firstname.lower()) & (
                    df1["lastname"] == self.lastname.lower()) & (
                    df1["username"] == self.username.lower())]
        if len(b) >= 1 and len(v) == 1:
            while True:
                print("Your username is available, please try again")

                break
        elif len(v) == 1:
            print("Sing up successful!")
            debug("a user edit profile in system")
            df2 = pd.read_csv("user.csv", sep=",")
            c = v.index.values
            df2.loc[c, ['password', 'firstname', 'lastname', 'username', 'email']] = [hash, self.firstname.lower(),
                                                                                      self.lastname.lower(),
                                                                                      self.username.lower(),
                                                                                      self.email]
            df2.to_csv('user.csv', index=False)
        elif len(v) < 1:
            print('This email is wrong')

    def __len__(self):
        """
        This method for return true or false in menu
        """
        return self.login


class Admin:
    """
        This class for the admin to log in,in system
        """

    def __init__(self):
        self.firstname = ''
        self.lastname = ''
        self.password = ''
        self.username = ''
        self.login = False

    def search_info_admin(self):
        """
        This method for search in manger file to log in admin

        """

        self.firstname = input("Enter your firstname:\n")
        self.lastname = input("Enter your lastname:\n")
        attempts = 3
        df = pd.read_csv("manager.csv", sep=",")
        while attempts > 0:
            attempts -= 1
            self.username = input("Enter your username:\n")
            a = df.loc[(df["username"] == self.username.lower())]
            if len(a) >= 1:
                self.password = input("Enter your password:\n")
                hs = hashlib.sha256(self.password.encode('utf-8')).hexdigest()
                b = df.loc[(df["password"] == hs)]
            else:
                print("Invalid Username...")
                print("You have {} attempts left.".format(attempts))
                continue
            if len(b) >= 1:
                print("Login successful!")
                self.login = True
                break
            elif attempts == 0:
                error_logging("Your account has been blocked")

            else:
                print("Invalid Password...")
                print("You have {} attempts left.".format(attempts))

    @classmethod
    def send_important_message(cls):
        """
        This method for send a message to manager for running out the capacity an event.
        :return:
        """
        df = pd.read_csv("event.csv", sep=",")
        warning_in_event_total_capacity = df.loc[(df["total_capacity"] <= 5)]
        name_event = df.loc[warning_in_event_total_capacity.index.values, "name"]
        if len(warning_in_event_total_capacity) >= 1:
            warnning_logging(f"The capacity of this event {str(name_event)} is running out")

    def __len__(self):
        return self.login
