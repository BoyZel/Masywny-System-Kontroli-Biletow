def pojazd_id(conn):
    id_choice = input("Choose id: ")
    dane = conn.execute('''
                        SELECT * FROM pojazdy WHERE nr_pojazdu = ?;
                        ''',
                        (id_choice,)).fetchone()
    # fetchone gdy jeden wiersz chcemy pobrac / fetchall gdy wszystkie wiersze spelniajace warunek chcemy
    print(dane)
