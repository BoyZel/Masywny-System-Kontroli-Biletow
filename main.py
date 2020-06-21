import sqlite3

# importuj wszystkie funkcje z pliku functions
from functions import *

# utworzenie polaczenia
conn = sqlite3.connect('database.db')

choice = '0'
inner_choice = '0'
while choice != 'q':
    print("Main Choice: Choose 1 of 5 choices")
    print("Zarzadzanie mandatami")
    print("Choose 2 for something")
    print("Choose 3 for something")
    print("Choose 4 for something")
    print("Choose q to quit")

    choice = input("Please make a choice: ")

    if choice == "1":
        print("    Wybierz 1 aby wprowadzic mandat")
        print("    Wybierz 2 aby usunac mandat")
        print("    Wybierz 3 aby wyswietlic mandaty klienta")

        inner_choice = input("    Please make a choice: ")
        if inner_choice == "1":
            print("    wproawdzam mandat")
        if inner_choice == "2":
            print("    usuwam mandat")
        if inner_choice == "3":
            print("    wproawdzam mandat")
        else:
            print("    Nie rozpoznano polecenia")

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


