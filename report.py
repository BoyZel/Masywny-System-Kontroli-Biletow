import sqlite3

# importuj wszystkie funkcje z pliku functions
from ftoreport import *

# utworzenie polaczenia
conn = sqlite3.connect('database.db')

choice = '0'
inner_choice = '0'
while choice != 'q':
    print("\nWcisnij odpowiedni numer aby przejsc do wybranej opcji.")
    print("1. Statystyki wystawionych mandatów.")
    print("2. Statystyki kontrolerów.")
    print("3. Statystyki sprzedazy biletow.")
    print("5. Wcisnij q aby opuscic program")

    choice = input("Wprowadz numer opcji: ")

    if choice == "1":
        print("    Wybierz 1 aby zobaczyć na których liniach wystawiono najwięcej mandatów.")
        print("    Wybierz 2 aby zobaczyć ile mandatów wystawiono na danej linii.")
        print("    Wybierz 3 aby zobaczyć listę nieuregulowanych mandatów.")
        print("    Wybierz 4 aby zobaczyć informację o danym mandacie")
        print("    Wybierz 5 aby zobaczyć listę wystawionych mandatów w zależności od typu")

        inner_choice = input("    Please make a choice: ")
        if inner_choice == "1":
            ranking_linii(conn)
        elif inner_choice == "2":
            statystyki_linii(conn)
        elif inner_choice == "3":
            wyswietl_mandaty(conn)
        elif inner_choice == "4":
            wyswietl_mandat(conn)
        elif inner_choice == "5":
            mandat_typ(conn)

        else:
            print("    Nie rozpoznano polecenia.")

    elif choice == "2":
        print("Wybierz 1 aby wyswietlić pełną listę kontrolerów.")
        print("Wybierz 2 aby wyświetlic ranking kontrolerów wg skuteczności.")
        print("Wybierz 3 aby wyswietlic statystyki pojedynczego kontrolera.")

        inner_choice = input("     Wprowadz numer opcji:")
        if inner_choice == "1":
            lista_kontrolerow(conn)
        elif inner_choice == "2":
            ranking_kontrolerow(conn)
        elif inner_choice == "3":
            wyswietl_kontrolera(conn)
        else:
            print("    Nie rozpoznano polecenia.")

    elif choice == "3":
        print("Wybierz 1 aby wyswietlic liczbe sprzedanych biletow o danej dlugosci okresu.")
        print("Wybierz 2 aby wyswietlic dane pojedynczego biletu.")
        print("Wybierz 3 aby wyswietlić sprzedane bilety w zależności od typu")
        print("Wybierz 4 aby wyświetlić bilety w zależności od wieku kupującego")
        inner_choice = input("    Wprowadz numer opcji: ")
        if inner_choice == "1":
            bilety_okres(conn)
        elif inner_choice == "2":
            wyswietl_bilet(conn)
        elif inner_choice == "3":
            bilety_typ(conn)
        elif inner_choice == "4":
            bilety_wiek(conn)
        else:
            print("    Nie rozpoznano polecenia.")

    elif choice == "q":
        print("Good bye")
    else:
        print("Nie rozpoznano polecenia!")


conn.close()
