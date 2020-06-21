from datetime import datetime, timedelta

def pojazd_id(conn):
    id_choice = input("Choose id: ")
    dane = conn.execute('''
                        SELECT * FROM pojazdy WHERE nr_pojazdu = ?;
                        ''',
                        (id_choice,)).fetchone()
    # fetchone gdy jeden wiersz chcemy pobrac / fetchall gdy wszystkie wiersze spelniajace warunek chcemy
    print(dane)

#****************************************************************************dodaj mandat*******************************
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

#******************************************************************************************wyswietl mandat**************
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
        print("    " + mandat)

#**********************************************************************usun mandat**************************************
def usun_mandat(conn):
    id_choice = input("Wpisz id mandatu : ")
    dane = conn.execute('''
                        SELECT * FROM mandaty WHERE mandat_id = ?;
                        ''',
                        (id_choice,)).fetchone()
    if not dane:
        print("Nie ma takiego mandatu")
        return

    conn.execute('''
                        DELETE FROM mandaty WHERE mandat_id = ?;
                        ''',
                        (id_choice,))
    print("Mandat usuniety")

#******************************************************************************wprowadz platnosc************************
def wprowadz_platnosc(conn):
    kwota = input("Podaj kwote")
    if int(kwota) <= 0:
        print("Kwota musi byc dodatnia")
        return

    data_wprowadzenia = datetime.today().date()

    rodzaje_platnosci = {1: 'gotówka', 2: 'karta', 3: 'przelew'}
    tmp = input(f"Podaj typ platnosci 1: {rodzaje_platnosci[1]}, 2: {rodzaje_platnosci[2]}, 3: {rodzaje_platnosci[3]} ")
    if not (tmp == "1" or tmp == "2" or tmp == "3"):
        return
    typ = rodzaje_platnosci[int(tmp)]

    mandat_id = input("Wpisz id mandatu do oplacenia : ")
    dane_mand = conn.execute('''
                        SELECT * FROM mandaty WHERE mandat_id = ?;
                        ''',
                        (mandat_id,)).fetchone()
    if not dane_mand:
        print("Nie ma takiego mandatu")
        return

    conn.execute('''INSERT INTO płatności
                    (kwota, 
                    data_płatności, 
                    typ, 
                    mandat_mandat_id)
                    VALUES (?,?,?,?)
                    ''',
                 (kwota, data_wprowadzenia, typ, mandat_id)
                 )
    conn.commit()
    print("Dodano nowa platnosc")

#*******************************************************************************kontrolerzy lista***********************
def kontrolerzy_lista(conn):
    dane = conn.execute('''
                        SELECT * FROM kontrolerzy;
                        ''').fetchall()
    for kontroler in dane:
        print(kontroler)

#*******************************************************************************skanery lista***************************
def skanery_lista(conn):
    dane = conn.execute('''
                        SELECT * FROM skanery;
                        ''').fetchall()
    for skaner in dane:
        print(skaner)
#*****************************************************************************konkretna funkcja*************************
def przypisz_skaner(conn):
    legitymacja = input("   Podaj nr odznaki kontrolera, ktoremu chcesz przypisac skaner. ")
    nr_skanera = input("    Podaj nr skanera, ktory chcesz przypisac. ")

    dane = conn.execute('''
                        SELECT * FROM kontrolerzy WHERE nr_legitymacji = ?;
                        ''',
                        (legitymacja,)).fetchone()
    if not dane:
        print("    Brak kontrolera o podanym numerze odznaki.")
        return

    dane_bis = conn.execute('''
                               SELECT * FROM skanery WHERE nr_urządzenia = ? AND stan = ?;
                               ''',
                        (nr_skanera,"dostępny")).fetchone()

    if not dane_bis:
        print("    Wybrany skaner jest niedostepny. ")
        return

    # skaner dotychczas przypisany
    dane_ter = conn.execute('''
                            SELECT skanery_nr_urządzenia FROM kontrolerzy WHERE nr_legitymacji = ?;
                            ''',
                            (legitymacja,)).fetchone()

    conn.execute('''
                 UPDATE kontrolerzy SET skanery_nr_urządzenia = ? WHERE nr_legitymacji = ?;
                 ''',
                 (nr_skanera, legitymacja))

    conn.commit()

    conn.execute('''
                     UPDATE skanery SET stan = ? WHERE nr_urządzenia = ?;
                     ''',
                 ("wypożyczony", nr_skanera))

    conn.commit()

    conn.execute('''
                UPDATE skanery SET stan = ? WHERE nr_urządzenia = ?;
                 ''',
                 ("dostępny", dane_ter[0]))

    print('Kontroler zaktualizowany')

    conn.commit()

#**************************************************************aktualizuj skaner****************************************
def aktualizuj_skaner(conn):
    nr_skanera = input("    Podaj nr skanera, ktorego dane chcesz zaktualizowac. ")
    print("Wcisnij odpowiedni numer aby przejsc do wybranej opcji.")
    print("1. Aktualizacja daty ostatniego przegladu.")
    print("2. Zmiana statusu na w naprawie (tylko jesli nie jest wypozyczony).")
    choice = input("    Wprowadz numer opcji: ")

    if choice == "1":
        data_przegladu = input("Podaj nowa date.")

        conn.execute('''
                    UPDATE skanery SET ostatni_przegląd = ? WHERE nr_urządzenia = ?;
                    ''',
                     (data_przegladu, nr_skanera))

    elif choice == "2":
        dane = conn.execute('''
                            SELECT * FROM skanery WHERE nr_urządzenia = ? AND stan = ?;
                            ''',
                            (nr_skanera, "dostępny")).fetchone()
        
        if not dane:
            print("Nie mozna wyslac do naprawy podanego skanera.")
            return 
        
        conn.execute('''
                    UPDATE skanery SET stan = ? WHERE nr_urządzenia = ?;
                    ''',
                    ("w naprawie",nr_skanera ))

    print('Skaner zaktualizowany')

    conn.commit()

# ****************************************************wyswietl bilety klienta****************************************
def wyswietl_bilety_klienta(conn):
    pesel = input("Wpisz pesel klienta : ")
    dane_pesel = conn.execute('''
                            SELECT * FROM pasażerowie WHERE pesel = ?;
                            ''',
                                 (pesel,)).fetchone()
    if not dane_pesel:
        print("Nie ma takiego klienta")
        return

    dane_bilety = conn.execute('''
                            SELECT * FROM bilety_elektroniczne WHERE pasażerowie_pesel = ?;
                            ''',
                            (pesel,)).fetchall()
    if not dane_bilety:
        print("Brak biletow")
    for bilet in dane_bilety:
        print(bilet)

#*******************************************************************************dodaj klienta********************
def dodaj_klienta(conn):

    imie = input("Podaj imię pasażera")
    nazwisko = input("Podaj nazwisko pasażera")
    pesel = input("Podaj numer PESEL pasażera")

    if not pesel.isdigit() or not len(pesel) == 11:
        print('Błędne dane')
        return


    conn.execute('''INSERT INTO pasażerowie
                    (pesel,
                    imię,
                    nazwisko)
                    VALUES (?,?,?)
                    ''',
                    (pesel, imie, nazwisko)
                 )

    print('Pasażer dodany')
    conn.commit()
    
#*******************************************************************************dodaj bilet********************
def dodaj_bilet(conn):

    pasazerowie_pesel = input("Podaj numer PESEL pasażera")
    wybor = conn.execute('''
                          SELECT * FROM pasażerowie WHERE pesel = ?;
                          ''',
                          (pasazerowie_pesel,)).fetchone()

    if not wybor:
        return


    dane = conn.execute('''
                        SELECT * FROM typy_ulg;
                        ''').fetchall()
    for bilet in dane:
        print(bilet)

    typy_ulg_nazwa = input("Wpisz rodzaj ulgi")
    wybor2 = conn.execute('''
                          SELECT * FROM typy_ulg WHERE nazwa = ?;
                          ''',
                         (typy_ulg_nazwa,)).fetchone()

    if not wybor2:
        print('Błędne dane')
        return


    dane2 = conn.execute('''
                            SELECT * FROM typy_okresów;
                            ''').fetchall()
    for okres in dane2:
        print(okres)

    okres_waznosci = input("Wpisz okres ważności")
    wybor3 = conn.execute('''
                              SELECT * FROM typy_okresów WHERE okres_ważności = ?;
                              ''',
                          (okres_waznosci,)).fetchone()

    if not wybor3:
        print('Błędne dane')
        return

    data_wystawienia = datetime.today().date()
    koniec_waznosci = data_wystawienia + timedelta(days=(30 * int(okres_waznosci)))

    cena = input("Podaj cenę biletu")
    if int(cena) <= 0:
        print('Błędne dane')
        return

    cena = (int(wybor2[1]) * int(cena)) / 100
    int(cena)

    conn.execute('''INSERT INTO bilety_elektroniczne
                    (data_wystawienia,
                    koniec_ważności,
                    cena,
                    pasażerowie_pesel,
                    typy_ulg_nazwa,
                    typy_okresów_okres_ważności)
                    VALUES (?,?,?,?,?,?)
                    ''',
                    (data_wystawienia, koniec_waznosci, cena, pasazerowie_pesel, typy_ulg_nazwa, okres_waznosci)
                 )

    print('Bilet elektroniczny dodany')
    conn.commit()
    
#*******************************************************************************przedloz bilet********************
def przedloz_bilet(conn):

    id_biletu = input("Podaj id biletu pasażera")
    wybor = conn.execute('''
                          SELECT * FROM bilety_elektroniczne WHERE id_biletu = ?;
                          ''',
                          (id_biletu,)).fetchone()

    if not wybor:
        print('Nie ma takiego biletu')
        return

    cena = int(wybor[3])
    pasazerowie_pesel = wybor[4]
    typy_ulg_nazwa = wybor[5]
    okres_waznosci = wybor[6]
    data_wystawienia = datetime.today().date()
    koniec_waznosci = data_wystawienia + timedelta(days=(30 * int(okres_waznosci)))

    conn.execute('''INSERT INTO bilety_elektroniczne
                    (data_wystawienia,
                    koniec_ważności,
                    cena,
                    pasażerowie_pesel,
                    typy_ulg_nazwa,
                    typy_okresów_okres_ważności)
                    VALUES (?,?,?,?,?,?)
                    ''',
                    (data_wystawienia, koniec_waznosci, cena, pasazerowie_pesel, typy_ulg_nazwa, okres_waznosci)
                 )

    print('Bilet elektroniczny przedłóżony')
    conn.commit()
