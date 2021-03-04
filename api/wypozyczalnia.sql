DROP DATABASE IF EXISTS wypozyczalnia;
CREATE DATABASE wypozyczalnia COLLATE = utf8_general_ci;
USE wypozyczalnia;

--tables

CREATE TABLE Filmy(
film_ID int NOT NULL AUTO_INCREMENT,
PRIMARY KEY (film_ID),
tytul varchar(255),
rezyser varchar(50),
gatunek varchar(50),
rok_prod YEAR,
opis TEXT,
cena float(10)
);

CREATE TABLE Osoby(
osoba_ID int NOT NULL AUTO_INCREMENT,
PRIMARY KEY (osoba_ID),
imie varchar(50),
nazwisko varchar(50),
pesel bigint(11),
nr_tel int(11),
e_mail varchar(50)
);

CREATE TABLE Wypozyczenia(
wypozyczenie_ID INT NOT NULL AUTO_INCREMENT,
PRIMARY KEY(wypozyczenie_ID),
Data_wypozyczenia DATETIME,
Data_oddania DATETIME, 
    fk_osoba int,
    fk_film int,
    FOREIGN KEY(fk_osoba) REFERENCES Osoby(osoba_ID),
    FOREIGN KEY(fk_film) REFERENCES Filmy(film_ID)
);

--data
INSERT INTO Filmy(film_ID, tytul, rezyser, gatunek,rok_prod, opis,cena ) VALUES('1', 'Terminator', 'James Cameron', 'science fiction', '1983', 'Tytułowy Terminator (Arnold Schwarzenegger) w pierwszej części serii jest androidem, który został wysłany w przeszłość w celu zlikwidowania Sary Connor, matki przywódcy rebeliantów, nielicznych ludzi, którzy walczą w przyszłości z cyborgami o przetrwanie.', '20.0');
INSERT INTO Filmy(film_ID, tytul, rezyser, gatunek,rok_prod, opis,cena ) VALUES('2', 'Gwiezdne wojny: Nowa nadzieja', 'George Lucas', 'science fiction', '1977', ' Ta czesc Gwiezdnych Wojen opowiada o młodym Luke’u Skywalkerze, który – podobnie jak ojciec – chce zostać rycerzem Jedi.', '20.0');
INSERT INTO Filmy(film_ID, tytul, rezyser, gatunek,rok_prod, opis,cena ) VALUES('3', 'Władca pierścieni: Drużyna Pierścienia', 'Peter Jackson', 'fantasy', '2001', ' Podróż hobbita z Shire i jego ośmiu towarzyszy, której celem jest zniszczenie potężnego pierścienia pożądanego przez Czarnego Władcę - Saurona.', '30.0');
INSERT INTO Filmy(film_ID, tytul, rezyser, gatunek,rok_prod, opis,cena ) VALUES('4', 'Władca pierścieni: Dwie Wieże', 'Peter Jackson', 'fantasy', '2002', 'Drużyna Pierścienia zostaje rozbita, lecz zdesperowany Frodo za wszelką cenę chce wypełnić powierzone mu zadanie. Aragorn z towarzyszami przygotowuje się, by odeprzeć atak hord Sarumana.', '30.0');
INSERT INTO Filmy(film_ID, tytul, rezyser, gatunek,rok_prod, opis,cena ) VALUES('5', 'Władca pierścieni: Powrót Króla', 'Peter Jackson', 'fantasy', '2003', 'Zwieńczenie filmowej trylogii wg powieści Tolkiena. Aragorn jednoczy siły Śródziemia, szykując się do bitwy, która ma odwrócić uwagę Saurona od podążających w kierunku Góry Przeznaczenia hobbitów.', '30.0');

INSERT INTO Osoby(osoba_ID, imie, nazwisko,pesel ,nr_tel ,e_mail) VALUES('1', 'Krzysztof', 'Krawczyk', '10233314512', '789456285', 'jestem_krzysiu@krawczyk.pl');
INSERT INTO Osoby(osoba_ID, imie, nazwisko,pesel ,nr_tel ,e_mail) VALUES('2', 'Maryla', 'Rodowicz',    '12362279928', '666999111', 'niesmiertelna@onet.pl');
INSERT INTO Osoby(osoba_ID, imie, nazwisko,pesel ,nr_tel ,e_mail) VALUES('3', 'Krzysztof', 'Ibisz',    '76544432112', '777555333', 'wiecznie_mlody@onet.pl');
INSERT INTO Osoby(osoba_ID, imie, nazwisko,pesel ,nr_tel ,e_mail) VALUES('4', 'Anna', 'Lawendowska',   '89873323487', '927424729', 'fit4ever@onet.pl');
INSERT INTO Osoby(osoba_ID, imie, nazwisko,pesel ,nr_tel ,e_mail) VALUES('5', 'Ewa', 'Chodakowska',    '12345678910', '345678987', 'fajterka@onet.pl');

INSERT INTO Wypozyczenia(wypozyczenie_ID, Data_wypozyczenia, Data_oddania, fk_osoba, fk_film) VALUES ('1', '2020-01-01 00:00:00','2021-01-01 00:00:00', '1', '2' );
INSERT INTO Wypozyczenia(wypozyczenie_ID, Data_wypozyczenia, Data_oddania, fk_osoba, fk_film) VALUES ('2', '2020-12-01 12:13:14','2020-12-31 12:13:14', '3', '2' );


-- selecty do wykorzystania w api

--dla klienta wypozyczalni
    --wyszukiwanie po gatunku
    -- SELECT * FROM Filmy WHERE gatunek='fantasy';
    -- SELECT * FROM Filmy WHERE gatunek='science fiction';
    
    -- wyszukiwanie gdzie rok produkcji jest z tego wieku 
    --SELECT * FROM Filmy WHERE rok_prod >'1999';
    
    --wyszukiwanie po cenie
    -- SELECT * FROM Filmy WHERE cena<'30.0';
    

    --wyszukiwanie po rezyserze
    -- SELECT * FROM Filmy WHERE rezyser='James Cameron';
    -- SELECT * FROM Filmy WHERE rezyser='George Lucas';
    -- SELECT * FROM Filmy WHERE rezyser='Peter Jackson';
    
   
    
-- ** funkcjonalnosc dla admina** 

    --> wyswietl wszystkich uzytkownikow
    -- SELECT * FROM Osoby;
    
    --sprawdzeniewypozyczen  
    --SELECT * FROM Wypozyczenia;
    
    --zliczanie uzytkownikow;
    --SELECT COUNT(*) FROM Osoby;
    
     -- pokazuje date wypozyczenia, date oddania, jaki film i nazwisko klienta:
     
    /* SELECT  Wypozyczenia.Data_wypozyczenia,Wypozyczenia.Data_oddania,Filmy.tytul, Osoby.nazwisko 
    FROM Wypozyczenia 
    INNER JOIN Filmy ON Wypozyczenia.fk_film= Filmy.film_ID
    INNER JOIN Osoby ON Wypozyczenia.fk_osoba=Osoby.osoba_ID; */

    
CREATE USER 'wypozyczalnia'@'localhost' IDENTIFIED BY 'wypozyczalnia';
GRANT ALL PRIVILEGES ON wypozyczalnia.* TO 'wypozyczalnia'@'localhost';
FLUSH PRIVILEGES;
