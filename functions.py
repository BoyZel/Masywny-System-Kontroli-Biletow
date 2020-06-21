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
