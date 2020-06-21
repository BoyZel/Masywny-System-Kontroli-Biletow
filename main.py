import sqlite3

# importuj wszystkie funkcje z pliku functions
from functions import *

# utworzenie polaczenia
conn = sqlite3.connect('database.db')

choice = '0'
inner_choice = '0'
while choice != 'q':
    print("\nWcisnij odpowiedni numer aby przejsc do wybranej opcji.")
    print("1. Zarzadzanie mandatami.")
    print("2. Zarzadzanie kontrolerami i skanerami.")
    print("3. Zarzadzanie klientami i biletami elektronicznymi.")
    print("4. Zarzadzanie platnosciami.")
    print("5. Wcisnij q aby opuscic program")

    choice = input("Wprowadz numer opcji: ")

    if choice == "1":
        print("    Wybierz 1 aby wprowadzic mandat.")
        print("    Wybierz 2 aby usunac mandat.")
        print("    Wybierz 3 aby wyswietlic mandaty klienta.")

        inner_choice = input("    Please make a choice: ")
        if inner_choice == "1":
            print("    Wprowadzam mandat.")
        elif inner_choice == "2":
            print("    Usuwam mandat.")
        elif inner_choice == "3":
            wyswietl_mandat(conn)
        else:
            print("    Nie rozpoznano polecenia.")

    elif choice == "2":
        print("Wybierz 1 aby przypisac wybranemu kontrolerowi skaner.")
        print("Wybierz 2 aby wyświetlic liste kontrolerow wraz z przypisanymi im skanerami.")
        print("Wybierz 3 aby wyswietlic liste skanerow.")
        print("Wybierz 4 aby zaktualizowac dane skanera.")

        inner_choice = input("     Wprowadz numer opcji:")
        if inner_choice == "1":
            print("    Przypisuje skaner.")
        elif inner_choice == "2":
            print("    Wyswietlam liste kontrolerow:")
        elif inner_choice == "3":
            print ("   Wyswietlam liste skanerow:")
        elif inner_choice == "4":
            print("    Aktualizuje dane skanera.")
        else:
            print("    Nie rozpoznano polecenia.")

    elif choice == "3":
        print("Wybierz 1 aby dodac nowego klienta do bazy danych.")
        print("Wybierz 2 aby dodac nowy bilet elektroniczny.")
        print("Wybierz 3 aby przedluzyc waznosc wybranego bilet elektroniczny.")

        inner_choice = input("    Wprowadz numer opcji: ")
        if inner_choice == "1":
            print("    Dodaje klienta.")
        elif inner_choice == "2":
            print("    Dodaje bilet elektroniczny.")
        elif inner_choice == "3":
            print("    Przedluzam waznosc biletu.")
        else:
            print("    Nie rozpoznano polecenia.")

    elif choice == "4":
        print("Wybierz 1 aby wprowadzic (zrealizowac) platnosc.")
        print("Wybierz 2 aby sprawdzic okresy waznosci wybranego biletu elektronicznego.")

        inner_choice = input("    Wprowadz numer opcji:")
        if inner_choice == "1":
            print("    Wprowadzam platnosc.")
        elif inner_choice == "2":
            print("    Sprawdzam okresy waznosci wybranego biletu elektronicznego.")
        else:
            print("    Nie rozpoznano polecenia.")

    elif choice == "q":
        print("Good bye")
    else:
        print("Nie rozpoznano polecenia!")


conn.close()