import sqlite3

# importuj wszystkie funkcje z pliku functions
from functions import *

# utworzenie polaczenia
conn = sqlite3.connect('database.db')

choice = '0'
while choice != 'q':
    print("Main Choice: Choose 1 of 5 choices")
    print("Choose 1 for pojazd id")
    print("Choose 2 for something")
    print("Choose 3 for something")
    print("Choose 4 for something")
    print("Choose q to quit")

    choice = input("Please make a choice: ")

    if choice == "1":
        pojazd_id(conn)
    elif choice == "2":
        print("Do Something 2")
    elif choice == "3":
        print("Do Something 3")
    elif choice == "4":
        print("Do Something 4")
    elif choice == "q":
        print("Good bye")
    else:
        print("I don't understand your choice.")


conn.close()


