import pandas as pd
import re
from file_logging import debug
from numpy import random


class Event:
    """
    This class for add or edit or buy an event by manager or customer with event file
    """

    def __init__(self):
        self.name_of_happen = ''
        self.holding_time = ''
        self.holding_date = ''
        self.event_place = ''
        self.total_capacity = ''
        self.remaining_capacity = ''
        self.ticket_fee = ''
        self.discount_any_id_code = ''
        self.discount_code = False
        self.teacher_student = False

    def add_event(self):
        """
        This method for add an event to event file by manager

        """
        debug("add an event to file.")
        self.name_of_happen = input("Please enter the event:\n")
        self.holding_time = input("Please enter the time such as 21:00:\n")
        while True:
            try:
                self.holding_date = input("Please enter the event(please enter the time such as 2021/11/02):\n")
                pattern = r'(([0-9]{4})-([0-9]{2})-([0-9]{2}))|(([0-9]{4})\/([0-9]{2})\/([0-9]{2}))'
                find_pattern = re.search(pattern, self.holding_date)
                if find_pattern:
                    break
                else:
                    raise ValueError()
            except ValueError:
                print("format date is wrong!please try again")
        self.event_place = input("Please enter the event_place:\n")
        self.total_capacity = input("Please enter the total_capacity:\n")
        self.ticket_fee = input("Please enter the ticket_fee:\n")
        list_number = []
        df = pd.read_csv("event.csv", sep=",")
        last_index = df.index.values[-1]
        random_number = random.randint(10000)
        while True:
            if random_number not in list_number:
                list_number.append(random_number)
                df.loc[last_index + 1, ["name", "place", "time", "date", "total_capacity", "ticket_fee", "id"]] = [
                    self.name_of_happen,
                    self.event_place,
                    self.holding_time,
                    self.holding_date,
                    self.total_capacity,
                    self.ticket_fee,
                    random_number]
                df.to_csv("event.csv", index=False)
                break
            else:
                continue

    @classmethod
    def edit_event(cls):
        """
        This method for edit an event from file by manger.
        """
        number_edit = int(input("Please Enter the ID for edit the event.\n "))
        df = pd.read_csv(
            "event.csv",
            sep=",")
        b = df.loc[
            (df['id'] == number_edit)]
        c = b.index.values
        if len(b) >= 1:
            print(b)
            list_header = ["name", "place", "date", "time", "total_capacity", "ticket_fee"]
            for i in range(len(list_header)):
                edit_value = input(f"Do yo want to change this column ({list_header[i]}) please enter yes or no:")
                if edit_value == "yes":
                    new_value = input(f"Enter the new value of {list_header[i]}:\n")
                    df.loc[c, [list_header[i]]] = [new_value]
                    df.to_csv("event.csv", index=False)
                else:
                    continue

        else:
            print("This ID is wrong")

    @classmethod
    def show_event(cls):
        """
        This method for show an event for manager or customer

        """
        debug("System has a request to show event")
        df = pd.read_csv("event.csv", sep=",")
        print(df)

    @classmethod
    def search_event(cls):
        """
        This method for search in file to find an event or another suggestion for customer
        """
        debug("This method can give  event from user")
        df = pd.read_csv("event.csv", sep=",")
        name_of_happen = input("Please enter the name of your favorite event:\n")
        holding_time = input("Enter the time such as (21:00) you want :\n")
        holding_date = input("Enter the date such as (2021/11/02) you want  :\n")
        event_place = input("Enter the place where you would like to see this event :\n")
        ticket_fee = input("Enter the amount of money you want:\n")
        search_1 = df.loc[
            (df["name"] == name_of_happen) | (df['place'] == event_place) | (df['date'] == holding_date) | (
                    df['time'] == holding_time) | (df['ticket_fee'] == ticket_fee)]

        search_2 = df.loc[
            (df["name"] == name_of_happen) & (df['place'] == event_place) & (df['date'] == holding_date) & (
                    df['time'] == holding_time) & (df['ticket_fee'] == ticket_fee)]
        if len(search_2) >= 1:
            print("your favorite event is exist.")
            print(search_2)
            print("To buy a ticket, you must write the event ID")
        else:
            print("your favorite event is not exist.")
        if len(search_1) >= 1:
            print("we have another suggestion for you\n")
            print(search_1)
            print("To buy a ticket, you must write the event ID")
        else:
            print("Sorry we don't have any suggestion for you")

    def buy_tickets(self):

        """
        This method for buy events by customer
        """
        number_id = int(input("Enter the ID of ticket you want to buy\n"))
        number_of_ticket = int(input("How many tickets you want to buy?\n"))
        df = pd.read_csv("event.csv", sep=",")
        buy_ticket = df.loc[(df["id"] == number_id) & (df["total_capacity"] >= number_of_ticket)]

        if len(buy_ticket) >= 1:
            while True:
                discount_code = input(
                    "DO you have any discount code(enter the number)? "
                    "1_ I have \t\t"
                    "2_ I am student or teachers \t\t "
                    "3_ I have no discount option \t\t"
                    "4_ Pay for the ticket \t\t "
                    "5_ Exit \n")
                if discount_code == "1":
                    if self.teacher_student == False:
                        discount_id = int(input("Enter the discount code:\n"))
                        df = pd.read_csv("discount_code.csv", sep=",")
                        search_discount_code = df.loc[(df["id_discount_cod"] == discount_id)]
                        if len(search_discount_code) >= 1:
                            self.discount_code = True
                    else:
                        print('You can not use two types of discount codes')
                elif discount_code == "2":
                    firstname = input("Enter your first name:\n")
                    lastname = input("Enter your last name:\n")
                    personal_code = int(input("Enter your office code or student code:\n"))
                    df = pd.read_csv("student_file.csv", sep=",")
                    df1 = pd.read_csv("teachers.csv", sep=",")
                    buy_ticket_1 = df.loc[
                        (df["student_code"] == personal_code) & (df["firstname"].str.lower() == firstname.lower()) & (
                                df["lastname"].str.lower() == lastname.lower())]
                    buy_ticket_2 = df1.loc[
                        (df1["office_code"] == personal_code) & (df1["firstname"].str.lower() == firstname.lower()) & (
                                df1["lastname"].str.lower() == lastname.lower())]

                    if len(buy_ticket_1) >= 1 or len(buy_ticket_2) >= 1:
                        if self.discount_code == False:
                            self.teacher_student = True
                        else:
                            print('You can not use types of discount codes')
                elif discount_code == "3":
                    print('Your ticket is free')
                elif discount_code == '4':
                    if self.teacher_student == True or self.discount_code == True:
                        df = pd.read_csv("event.csv", sep=",")
                        a = buy_ticket.index.values
                        b = df.iloc[a]
                        print(b)
                        c = df.loc[a, "ticket_fee"]
                        pay_by_discount = ((c - (c * 10 / 100)) * number_of_ticket)
                        pay_free = (c * number_of_ticket)
                        print(
                            f'You have to pay the amount is {int(pay_free)} but you have discounted '
                            f'code and  by including the code is {int(pay_by_discount)}')
                        buy_ticket_customer_1 = input("Do you want to buy this ticket? yes or no\n")
                        if buy_ticket_customer_1 == "yes":
                            print("Thank you for your purchase")
                            read_shopping = pd.read_csv("Customer_shopping_cart.csv")
                            sum_tickets = read_shopping.loc[read_shopping.index.values[-1], "number_of_tickets"]
                            read_shopping.loc[read_shopping.index.values[-1], "number_of_tickets"] = [
                                sum_tickets + number_of_ticket]
                            read_shopping.to_csv("Customer_shopping_cart.csv")

                            debug(
                                f"a customer buy a ticket This money {int(pay_by_discount)} was credited to your account")
                            df1 = pd.read_csv("discount_code.csv", sep=",")
                            if self.discount_code:
                                df1.at[search_discount_code.index.values, 'id_discount_cod'] = 0
                                df1.to_csv("discount_code.csv", index=False)
                            e = df.loc[a, "total_capacity"]
                            df.loc[a, "total_capacity"] = [e - number_of_ticket]
                            df.to_csv('event.csv', index=False)

                    else:
                        df = pd.read_csv("event.csv", sep=",")
                        a = buy_ticket.index.values
                        b = df.iloc[a]
                        print(b)
                        c = df.loc[a, "ticket_fee"]
                        pay_free_02 = (c * number_of_ticket)
                        print(f'You have to pay the amount  {int(pay_free_02)} ')

                        buy_ticket_customer_2 = input("Do you want to buy this ticket? yes or no\n")
                        if buy_ticket_customer_2 == "yes":
                            print("Thank you for your purchase")
                            read_shopping = pd.read_csv("Customer_shopping_cart.csv")
                            sum_tickets = read_shopping.loc[read_shopping.index.values[-1], "number_of_tickets"]
                            read_shopping.loc[read_shopping.index.values[-1], "number_of_tickets"] = [
                                sum_tickets + number_of_ticket]
                            read_shopping.to_csv("Customer_shopping_cart.csv")

                            debug(
                                f"a customer buy a ticket This money {int(pay_free_02)}  was credited to your account")
                            e = df.loc[a, "total_capacity"]
                            df.loc[a, "total_capacity"] = [e - number_of_ticket]
                            df.to_csv('event.csv', index=False)
                elif discount_code == '5':

                    break
        else:
            print("There is no event of your choice or its capacity is less than the amount of your choice")

    def add_discount_code(self):
        """
        This method for add a new discount code by manger

        """
        debug("a discount id added by manager")
        self.discount_any_id_code = int(input("Enter a discount code:\n"))
        df = pd.read_csv("discount_code.csv")
        add_discount_code = df.loc[(df["id_discount_cod"] == self.discount_any_id_code)]
        if len(add_discount_code) >= 1:
            print("This code is available please try a gain.")
        else:
            c = df.index.values[-1]
            df.loc[c + 1, ['id_discount_cod']] = [self.discount_any_id_code]
            df.to_csv('discount_code.csv', index=False)

    @classmethod
    def sum_buy_tickets(cls):
        """
        to show sum tickets Sold

        """
        read_shopping_file = pd.read_csv("Customer_shopping_cart.csv")
        final = read_shopping_file['number_of_tickets'].sum()
        return f' This amount of {final} tickets is sold out'
