from datetime import datetime, timedelta



def ranking_linii(conn):
    dane = conn.execute('''
                        SELECT numer, ilość_mandatów 
                        FROM linie
                        ORDER BY ilość_mandatów DESC;
                        ''',
                        ).fetchall()
    print(dane)


def statystyki_linii(conn):
    numer_choice = input("Podaj numer linii: ")
    dane = conn.execute('''
                        SELECT * FROM linie WHERE numer = ?;
                        ''',
                        (numer_choice,)).fetchone()
    # fetchone gdy jeden wiersz chcemy pobrac / fetchall gdy wszystkie wiersze spelniajace warunek chcemy
    print(dane)


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
    print(dane)
    
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
    print(dane)

def lista_kontrolerow(conn):
    dane = conn.execute('''
                        SELECT * FROM kontrolerzy WHERE mandat_id = ?;
                        ''',
                        ).fetchall()

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

def dodaj_mandat(conn):
    wystawienie = datetime.today().date()
    zaplata = wystawienie + timedelta(days=30)

    dane = conn.execute('''
                        SELECT przyczyna_wystawienia FROM typy_mandatów;
                        ''').fetchall()
    for mandat in dane:
        print(mandat)

    tmp = input("Podaj przyczynę wystawienia 1 - pierwszy wybór, 2 - drugi wybór: ")

    if tmp == "1":
        przyczyna_wystawienia = 'Brak ważnej legitymacji studenckiej'
    elif tmp == "2":
        przyczyna_wystawienia = 'Brak ważnego biletu'
    else:
        return

    linie_numer = input("Podaj numer linii")
    wybor2 = conn.execute('''
                          SELECT * FROM linie WHERE numer = ?;
                          ''',
                          (linie_numer,)).fetchone()

    if not wybor2:
        return

    pasazerowie_pesel = input("Podaj numer PESEL pasażera")
    wybor3 = conn.execute('''
                          SELECT * FROM pasażerowie WHERE pesel = ?;
                          ''',
                          (pasazerowie_pesel,)).fetchone()

    if not wybor3:
        return

    nr_legitymacji = input("Podaj swój numer legitymacji")
    wybor6 = conn.execute('''
                          SELECT * FROM kontrolerzy WHERE nr_legitymacji = ?;
                          ''',
                          (nr_legitymacji,)).fetchone()

    if not wybor6:
        return

    nr_pojazdu = input("Podaj numer pojazdu")
    wybor4 = conn.execute('''
                          SELECT * FROM pojazdy WHERE nr_pojazdu = ?;
                          ''',
                          (nr_pojazdu,)).fetchone()

    if not wybor4:
        return

    id_przystanku = input("Podaj id przystanku")
    wybor5 = conn.execute('''
                    SELECT * FROM przystanki WHERE id_przystanku = ?;
                    ''',
                          (id_przystanku,)).fetchone()

    if not wybor5:
        return

    conn.execute('''INSERT INTO mandaty
                    (data_wystawienia,
                    termin_zapłaty,
                    typy_mandatów_przyczyna_wystawienia,
                    linie_numer,
                    pasażerowie_pesel,
                    kontrolerzy_nr_legitymacji,
                    pojazdy_nr_pojazdu,
                    przystanki_id_przystanku)
                    VALUES (?,?,?,?,?,?,?,?)
                    ''',
                 (wystawienie, zaplata, przyczyna_wystawienia, linie_numer,
                  pasazerowie_pesel, nr_legitymacji, nr_pojazdu, id_przystanku)
                 )

    print('Mandat dodany')