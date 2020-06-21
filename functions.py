from datetime import datetime, timedelta

def pojazd_id(conn):
    id_choice = input("Choose id: ")
    dane = conn.execute('''
                        SELECT * FROM pojazdy WHERE nr_pojazdu = ?;
                        ''',
                        (id_choice,)).fetchone()
    # fetchone gdy jeden wiersz chcemy pobrac / fetchall gdy wszystkie wiersze spelniajace warunek chcemy
    print(dane)


def wyswietl_mandat(conn):
    pesel_choice = input("    Wpisz pesel : ")
    dane = conn.execute('''
                        SELECT * FROM mandaty WHERE pasażerowie_pesel = ?;
                        ''',
                        (pesel_choice,)).fetchall()
    if not dane:
        print("    Brak mandatow dla wybranego peselu")
        return
    for mandat in dane:
        print("    "+mandat)
       
    
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
    else: return

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
