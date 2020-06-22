from datetime import datetime, timedelta



def ranking_linii(conn):
    dane = conn.execute('''
                        SELECT numer, ilość_mandatów 
                        FROM linie
                        ORDER BY ilość_mandatów DESC;
                        ''',
                        ).fetchall()
    for linia in dane:
        print(f"Numer linii: {linia[0]}  wystawionych mandatów: {linia[1]}")


def statystyki_linii(conn):
    numer_choice = input("Podaj numer linii: ")
    dane = conn.execute('''
                        SELECT * FROM linie WHERE numer = ?;
                        ''',
                        (numer_choice,)).fetchone()
    if not dane:
        print("    Nie ma takiej linii")
        return
    print(f"Na linii {dane[0]} wystawiono {dane[1]} mandatów")

def wyswietl_mandat(conn):
    id_choice = input("    Wpisz id mandatu : ")
    dane = conn.execute('''
                        SELECT * FROM mandaty WHERE mandat_id = ?;
                        ''',
                        (id_choice,)).fetchall()
    if not dane:
        print("    Brak mandatow o danym id")
        return
    
    print(f'''
            ID mandatu: {dane[0][0]}
            data wystawienia: {dane[0][1]}
            termin zapłaty: {dane[0][2]}
            przyczyna wystawienia: {dane[0][3]}
            numer linii na której został wystawiony: {dane[0][4]}
            PESEL pasażera: {dane[0][5]}
            Nr legitymacji kontrolera: {dane[0][6]}
            Nr pojazdu: {dane[0][7]}
            ID przystanku: {dane[0][8]}
          ''')

def wyswietl_mandaty(conn):
    dane = conn.execute('''
                        SELECT m.mandat_id 
                        FROM
                        (
                            SELECT mandaty.mandat_id, typy_mandatów.wysokość_kary
                            FROM mandaty LEFT JOIN typy_mandatów 
                            ON mandaty.typy_mandatów_przyczyna_wystawienia = typy_mandatów.przyczyna_wystawienia 
                        ) m LEFT JOIN
                        płatności p ON m.mandat_id = p.mandat_mandat_id
                        WHERE m.wysokość_kary > p.kwota;
                        ''',
                        ).fetchall()
    print("Nieopłacone mandaty: ")
    for mandat in dane:
        print(f"ID mandatu: {mandat[0]} ")
    
def mandat_typ(conn):
    type_choice = input('''
                    Wpisz 1 jeżeli chcesz zobaczyć mandaty wystawione przez brak legitymacji studenckiej
                    Wpisz 2 jeżeli chcesz zobaczyć mandaty wystawione przez brak ważnego biletu
                    
                    ''')
    if type_choice == '1':
        dane = conn.execute('''
                            SELECT mandat_id FROM mandaty 
                            WHERE typy_mandatów_przyczyna_wystawienia = 'Brak ważnej legitymacji studenckiej';
                            ''',
                            ).fetchall()
    elif type_choice == '2':
       dane = conn.execute('''
                            SELECT mandat_id FROM mandaty WHERE typy_mandatów_przyczyna_wystawienia = 'Brak ważnego biletu';
                            ''',
                            ).fetchall() 
    if not dane:
        print("    Brak mandatow o danym typie")
        return
    for mandat in dane:
        print(f"ID mandatu: {mandat[0]} ")


def bilety_typ(conn):
    typ_choice = input("    Wpisz typ: ")
    dane = conn.execute('''
                        SELECT COUNT (*) FROM bilety_elektroniczne WHERE typy_ulg_nazwa  = ?;
                        ''',
                        (typ_choice,)).fetchall()
    if not dane:
        print("    Brak biletow w tym typie")
        return
    print(dane[0][0])



def wyswietl_bilet(conn):
    pesel_choice = input("    Wpisz pesel: ")
    dane = conn.execute('''
                        SELECT * FROM bilety_elektroniczne WHERE pasażerowie_pesel  = ?;
                        ''',
                        (pesel_choice,)).fetchall()
    if not dane:
        print("    Brak biletow w tym typie")
        return
    for dana in dane:
        print(dana)

def bilety_okres(conn):
    typ_choice = input("    Wpisz typ: ")
    dane = conn.execute('''
                        SELECT COUNT (*) FROM bilety_elektroniczne WHERE typy_okresów_okres_ważności = ?;
                        ''',
                        (typ_choice,)).fetchall()
    if not dane:
        print("    Brak biletow w tym typie")
        return
    print(dane[0][0])
    
def bilety_wiek(conn):
    wiek_choice = int(input("   Wpisz wiek: "))
    
    if wiek_choice > 0 and wiek_choice <= 20:
        pesel_numbers = str(20-wiek_choice+20)
        print(pesel_numbers)
        dane = conn.execute('''
                        SELECT id_biletu FROM bilety_elektroniczne WHERE SUBSTR(pasażerowie_pesel, 1, 2) = ?;
                        ''',
                        (pesel_numbers,)).fetchall()
    elif wiek_choice > 20:
        pesel_numbers = str(99 - wiek_choice + 21)
        print(pesel_numbers)
        dane = conn.execute('''
                        SELECT id_biletu FROM bilety_elektroniczne WHERE SUBSTR(pasażerowie_pesel, 1, 2) = ?;
                        ''',
                        (pesel_numbers,)).fetchall()
    for dana in dane:
        print(dana[0])

def ranking_kontrolerow(conn):
    dane = conn.execute('''
                        SELECT nr_legitymacji, ilość_mandatów_wystawionych FROM kontrolerzy ORDER BY ilość_mandatów_wystawionych DESC;
                        ''',
                        ).fetchall()
    for kontroler in dane:
        print(f"ID kontrolera: {kontroler[0]}  wystawionych mandatów: {kontroler[1]}")
        
def lista_kontrolerow(conn):
    dane = conn.execute('''
                        SELECT * FROM kontrolerzy;
                        ''',
                        ).fetchall()
    for kontroler in dane:
        print(f"ID kontrolera: {kontroler[0]}  Imie kontrolera: {kontroler[1]}  Nazwisko kontrolera: {kontroler[2]}  Ilość wystawionych mandatów: {kontroler[3]}  Numer przypisanego skanera: {kontroler[4]}")
        
def wyswietl_kontrolera(conn):
    ID_choice = input("    Wpisz nr legitymacji kontrolera: ")
    dane = conn.execute('''
                        SELECT * FROM kontrolerzy WHERE nr_legitymacji = ?;
                        ''',
                        (ID_choice,)).fetchall()
    if not dane:
        print("    Brak kontrolera o podanym numerze legitymacji")
        return
    print(f"ID kontrolera: {dane[0][0]}  Imie kontrolera: {dane[0][1]}  Nazwisko kontrolera: {dane[0][2]}  Ilość wystawionych mandatów: {dane[0][3]}  Numer przypisanego skanera: {dane[0][4]}")
