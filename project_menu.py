from event_project import *
from customer_manager import Customer, Admin

"""
This code for buy an event by a customer a
and this file just for call(make an object) and use method or class fro another file
i use pandas to check or edit in csv file

"""
while True:
    person = input("who are you?pleas choose a choice:\t\t 1_manager \t\t 2_user \t\t 3_Exit\n")
    if person == "1":
        admin_obj = Admin()
        admin_obj.search_info_admin()
        if bool(admin_obj):
            Admin.send_important_message()
            print()
            while True:
                admin_menu = input(
                    "You can choose one of the options:"
                    "\t\t 1_Add event"
                    "\t\t 2_Edit event"
                    "\t\t 3_see all event"
                    "\t\t 4_Add discount code"
                    "\t\t 5_see all ticket Sold"
                    "\t\t 6_Exit\n")
                if admin_menu == '1':
                    event_obj = Event()
                    print(event_obj.add_event())
                elif admin_menu == '2':
                    event_obj = Event()
                    print(event_obj.edit_event())
                elif admin_menu == '3':
                    event_obj = Event()
                    print(event_obj.show_event())
                elif admin_menu == '4':
                    event_obj = Event()
                    event_obj.add_discount_code()
                elif admin_menu == "5":
                    print(Event.sum_buy_tickets())
                elif admin_menu == '6':
                    break

    elif person == "2":
        while True:
            person_user = input("Create an account if you do not have one:\t\t 1_Sing up \t\t 2_Log in \t\t 3_Exit\n")
            if person_user == "1":
                user_obj = Customer()
                user_obj.get_info_user()
            elif person_user == "2":
                user_obj = Customer()
                user_obj.search_info_user()
                if bool(user_obj):
                    while True:
                        edit_user_n = input(
                            "You can edit your account if you one:"
                            "\t\t 1_Edit_profile "
                            "\t\t 2_See all event "
                            "\t\t 3_Search a ticket "
                            "\t\t 4_Bought a ticket "
                            "\t\t 5_Exit\n ")
                        if edit_user_n == "1":
                            user_obj = Customer()
                            user_obj.edit_user()
                        elif edit_user_n == "2":
                            Event().show_event()
                        elif edit_user_n == "3":
                            Event().search_event()
                        elif edit_user_n == "4":
                            user_obj = Event()
                            user_obj.buy_tickets()
                        elif edit_user_n == "5":
                            break
            elif person_user == "3":
                break
    elif person == "3":
        break
