import sqlite3
import time as t

class Czytelnik:
    def __init__(self, im="Jan", nazw="Nowak", numer_karty="123"):
        self.imie = im
        self.nazwisko = nazw
        self.nr_karty = numer_karty

class Ksiazka:
    def __init__(self, autor="", tytul="", nr_isbn="", liczba_egz=0, liczba_wyp=0, ):
        self.autor = autor
        self.tytul = tytul
        self.isbn = nr_isbn
        self.liczba_egz = liczba_egz
        self.liczba_wyp = liczba_wyp

def create_db(conn):
    #tworzenie tabel jesli nie istnieja
    #cur.execute("DROP TABLE IF EXISTS czytelnik;")
    cur.executescript("""    
    CREATE TABLE IF NOT EXISTS czytelnik (
        nrKarty INTEGER PRIMARY KEY ASC,
        imie VARCHAR(250) NOT NULL,
        nazwisko VARCHAR(250) NOT NULL 
    );""")

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS ksiazka (
        isbn integer primary key asc,
        autor varchar(250) not null,
        tytul varchar(250) not null,
        liczba_egz integer,
        liczba_wyp integer,
        czytelnikId integer,
        foreign key(czytelnikId) references czytelnik(nrKarty) 
    );""")

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS wypozyczone (
        id integer primary key asc,
        data varchar(250) not null,
        foreign key(ksiazkaISBN) references ksiazka(isbn),
        foreign key(czytelnikId) references czytelnik(nrKarty)
    );""")
def close_db(conn):
    # zamykamy baze
    conn.close()

def aktualna_data():
    import datetime
    datetime.datetime.now()
    return datetime.datetime.now().date()

#sprawdza czy sa dostepne egzemplarze danej ksiazki
def sprawdz_dostep_egz(numer):
    cur.execute('select liczba_egz from ksiazka where isbn=(?);', (numer,))
    wynik = cur.fetchone()

    for wiersz in wynik:
        #print(wiersz)
        if wiersz > 0:
            return 1
        else:
            return 0


def show_users():
    cur.execute('select * from czytelnik')
    dane = cur.fetchall()
    print("Dane czytelnikow w bazie: ")
    for czytelnik in dane:
        print("Numer karty: " + str(czytelnik['nrKarty']) + "  |  " + "Nazwisko: " + str(
            czytelnik['nazwisko']) + "  |  " + "Imie: " + str(czytelnik['imie']))

def show_books():
    cur.execute('select * from ksiazka')
    dane =cur.fetchall()
    print("")
    print("Lista ksiazek w bazie: ")
    for pozycja in dane:
        print("ISBN: " + str(pozycja['isbn']) + "   |   " + "Autor: " + str(
            pozycja['autor']) + "   |   "+ "Tytul: " + str(pozycja['tytul']) + "   |   " +str(pozycja['liczba_egz'])+" szt. ")


#tworzenie polaczenia i pliku z baza
connection=sqlite3.connect('Bibliotekav2.db')
# dzieki temu odczytujemy poszczegolne pola podajac ich nazwy zamiast indeksow
connection.row_factory=sqlite3.Row
#stworzenie kursora
cur=connection.cursor()
#funkcja rysujaca tabele
create_db(connection)

#tworzymy obiekt klasy Czytelnik
czyt = Czytelnik()
ks = Ksiazka()

while(True):
    print("")
    print("Menu:")
    print("""
    1. Dodaj czytelnika
    2. Usun czytelnika
    3. Dodaj ksiazke
    4. Usun ksiazke
    5. Wypozycz ksiazke
    6. Oddaj ksiazke
    7. Lista czytelnikow
    8. Lista Ksiazek
    99. Koniec
    """)

    wybor=input()

    #dodaj czytelnika
    if wybor == '1':
        czyt.im = input("Podaj imie: ")
        czyt.nazw = input("Podaj nazwisko: ")
        cur.execute('insert into czytelnik values(NULL, ?, ?);', (czyt.im, czyt.nazw))
        connection.commit() # zamykamy baze i zapisujemy zmiany
        # bez przecinka python widzi C1.nazw jako ciag znakow
        cur.execute('select nrKarty from czytelnik where nazwisko=(?);', (czyt.nazw,))
        czyt.nr_karty = cur.fetchall()
        # wszystkie pasujace rekordy zwrocone w fetchall zapisujemy do zmiennej czytelnik jako tupla
        print("")
        print("Pomyslnie dodano nowego czytelnika: ")
        for czytelnik in czyt.nr_karty:
            print("Numer karty: " + str(czytelnik['nrKarty']) +"   |   " + "Imie: " + czyt.im +"   |   "+"Nazwisko: " + czyt.nazw)
        t.sleep(3)

    #usun czytelnika
    elif wybor == '2':
        show_users()
        print("")
        usun = input("Podaj numer karty czytelnika, ktorego chcesz usunac: ")
        cur.execute('delete from czytelnik where nrKarty=(?);',(usun,))
        connection.commit()
        print("Pomyslnie usunieto uzytkownika o numerze karty: "+usun)
        t.sleep(3)

    #dodaj ksiazke
    elif wybor == '3':
        ks.tytul = input("Podaj tytul: ")
        ks.autor = input("Podaj autora: ")
        ks.liczba_egz = input("Podaj liczbe dostepnych egzemplarzy: ")
        cur.execute('insert into ksiazka values(NULL, ?, ?, ?, NULL, NULL);', (ks.tytul, ks.autor, ks.liczba_egz))
        connection.commit()  # zamykamy baze i zapisujemy zmiany
        # bez przecinka python widzi C1.nazw jako ciag znakow
        cur.execute('select isbn from ksiazka where tytul=(?);', (ks.tytul,))
        ks.isbn = cur.fetchall()
        print("")
        print("Pomyslnie dodano nowa ksiazkę: ")
        # wszystkie pasujace rekordy zwrocone w fetchall zapisujemy do zmiennej pozycja jako tupla
        for pozycja in ks.isbn:
            print("ISBN: " + str(pozycja['isbn'])+ "   |   " + "Autor: " + ks.autor+"   |   "+
                  "Tytul: "+ks.tytul+"   |   "+ks.liczba_egz+" szt.")

        t.sleep(3)

    #usun ksiazke
    elif wybor == '4':
        show_books()
        print("")
        usun = input("Podaj numer isbn ksiazki, ktora chcesz usunac: ")
        cur.execute('delete from ksiazka where isbn=(?);', (usun,))
        connection.commit()
        print("Pomyslnie usunieto ksiazke o numerze isbn: " + usun)
        t.sleep(3)

    #wypozycz ksiazke
    elif wybor == '5':
        show_users()
        print("")
        uzytkownik = input("Wpisz numer karty uzytkownika, ktory wypozycza ksiazke: ")
        show_books()
        print("")
        ksiazka = input("Wpisz numer isbn ksiazki, ktora chce wypozyczyc: ")
        ksiazka=int(ksiazka)

        # sprawdza czy ksiazka ma dostepne egzemplarze, jesli tak to przypisuje ksiazke do uzytkownika i odejmuje
        # 1 szt. od liczby dostepnych egzemplarzy
        if sprawdz_dostep_egz(ksiazka) == 1:
            cur.execute('insert into wypozyczone values(NULL, ?, ?, ?);', (aktualna_data(), ksiazka, uzytkownik))
            cur.execute('update ksiazka set liczba_egz=liczba_egz-1 where isbn=(?)', (ksiazka,))
            connection.commit()
            print("Ksiazka zostala pomyslnie przypisana do wybranego uzytkownika.")
        elif sprawdz_dostep_egz(ksiazka) == 0:
            print("")
            print("Brak dostepnych egzemplarzy ksiazek do wypozyczenia.")
            t.sleep(3)

    #lista czytelnikow
    elif wybor == '7':
        show_users()

    # do testow - do usuniecia
    elif wybor == '0':
        print(sprawdz_dostep_egz(13))

    #lista ksiazek
    elif wybor == '8':
        show_books()

    #zamkniecie programu i bazy danych
    elif wybor == '99':
        # funkcja zamykajaca polaczenie z baza
        close_db(connection)
        exit()



