import flask
from flask import *  # request, jsonify, render_template
import mysql.connector
from mysql.connector import errorcode
import bcrypt

# Połączenie z bazą danych:
try:
    conn = mysql.connector.connect(user='aghsql',
                                   password='c@AstU4r',
                                   database='new_schema',
                                   port=3306,
                                   host='glownymsql.mysql.database.azure.com',
                                   ssl_disabled=False,
                                   ssl_ca='./TajnyPlikNieOtwierac.crt.pem')
    print("\n### DATABASE CONNECTION STATUS: OK ###\n - Połączono z bazą danych.\n\n")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("\n### DATABASE CONNECTION ERROR ###\n -Błędna nazwa użytkownika lub hasło.\n\n")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("\n### DATABASE CONNECTION ERROR ###\n - Baza danych nie istnieje.\n\n")
    else:
        print(err)
else:
    cursor = conn.cursor(buffered=True)

    # Odczyt z tabeli Filmy
    query = "SELECT * FROM Filmy;"

    # admin query
    query0 = "SELECT  Wypozyczenia.Data_wypozyczenia,Wypozyczenia.Data_oddania,Filmy.tytul, Osoby.nazwisko FROM " \
             "Wypozyczenia INNER JOIN Filmy ON Wypozyczenia.fk_film= Filmy.film_ID INNER JOIN Osoby ON " \
             "Wypozyczenia.fk_osoba=Osoby.osoba_ID; "

    # wyszukiwanie gdzie rok produkcji jest z tego wieku
    query1 = "SELECT * FROM Filmy WHERE rok_prod >'1999'; "

    # wyszukiwanie po cenie
    query2 = " SELECT * FROM Filmy WHERE cena<'30.0';"

    # wyszukiwanie po rezyserze
    query3 = " SELECT * FROM Filmy WHERE rezyser='James Cameron';"
    query4 = " SELECT * FROM Filmy WHERE rezyser='George Lucas';"
    query5 = " SELECT * FROM Filmy WHERE rezyser='Peter Jackson';"

    cursor.execute(query)
    rows = cursor.fetchall()
    print("Read", cursor.rowcount, "row(s) of data.")

    # Wypisanie wszystkiego z tabeli Filmy
    for row in rows:
        print("Data row = (%s, %s, %s, %s, %s, %s)" % (
            str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5])))

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# start (przekierowanie na /home)
@app.route('/', methods=['GET'])
def start():
    return redirect("/home")


# strona glowna
@app.route('/home', methods=['GET'])
def home():
    return render_template("home.html")


# wszystkie filmy
@app.route('/api/v1/resources/filmy/all', methods=['GET'])
def api_all():
    return render_template("filmy.html", rows=rows)


# rok produkcji z tego wieku
@app.route('/filmy/opt1', methods=['GET'])
def opt1():
    cursor.execute(query1)
    rows = cursor.fetchall()
    return render_template("filmy.html", rows=rows)


# filmy za mniej niz 30
@app.route('/filmy/opt2', methods=['GET'])
def opt2():
    cursor.execute(query2)
    rows = cursor.fetchall()
    return render_template("filmy.html", rows=rows)


# rezyser nr1
@app.route('/filmy/opt3', methods=['GET'])
def opt3():
    cursor.execute(query3)
    rows = cursor.fetchall()
    return render_template("filmy.html", rows=rows)


# rezyser nr2
@app.route('/filmy/opt4', methods=['GET'])
def opt4():
    cursor.execute(query4)
    rows = cursor.fetchall()
    return render_template("filmy.html", rows=rows)


# rezyser nr3
@app.route('/filmy/opt5', methods=['GET'])
def opt5():
    cursor.execute(query5)
    rows = cursor.fetchall()
    return render_template("filmy.html", rows=rows)


# admin query
@app.route('/admin', methods=['GET'])
def admin():
    cursor.execute(query0)
    rows = cursor.fetchall()
    return render_template('wypozyczeniaAdmin.html', rows=rows)


# rejestracja
@app.route('/register', methods=['GET', 'POST'])
def Autenticate():
    if request.method == 'GET':
        return render_template('register_form.html')
    else:
        imie = str(request.form['imie'])
        nazwisko = str(request.form['nazwisko'])
        pesel = str(request.form['pesel'])
        nr_tel = str(request.form['nr_tel'])
        e_mail = str(request.form['e_mail'])
        passwd = str(request.form['passwd'].encode('utf-8'))
        
        #sprawdzanie danych
        contains_digit=False
        for character in imie:
            if character.isdigit():
                contains_digit=True
                if contains_digit ==True:
                    return "Blad przy wpisywaniu imienia, zawiera cyfry "

        for character in nazwisko:
            if character.isdigit():
                contains_digit=True  
                if contains_digit ==True:
                    return "Blad przy podawaniu nazwiska, zawiera cyfry "      

        pesel_lower = pesel.lower()
        contains_letter = pesel_lower.islower()
        if contains_letter == True: 
                 return "Blad: pesel zawiera litery" 
        
        tel_lower = nr_tel.lower()
        contains_letter = tel_lower.islower()
        if contains_letter == True: 
                 return "Blad: nr telefonu zawiera litery"  

        malpa = e_mail.find("@")  
        if malpa == -1 :
            return "blad przy wpisywaniu e-mail: brakuje @"
        
        
        
        # hashowanie hasla
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(passwd.encode('utf-8'), salt)

        cursor.execute(
            """INSERT INTO Osoby (imie,nazwisko,pesel,nr_tel,e_mail,passwd) VALUES (%(imie)s,%(nazwisko)s,%(pesel)s,
            %(nr_tel)s,%(e_mail)s,%(passwd)s)""",
            {'imie': imie,
             'nazwisko': nazwisko,
             'pesel': pesel,
             'nr_tel': nr_tel,
             'e_mail': e_mail,
             'passwd': hash_password})

        conn.commit()
        print("po execute")
        session['imie'] = imie
        session['nazwisko'] = nazwisko
        session['pesel'] = pesel
        session['nr_tel'] = nr_tel
        session['e_mail'] = e_mail
        return redirect("/home")


# logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        e_mail = str(request.form['e_mail'])
        passwd = str(request.form['passwd'].encode('utf-8'))
       
        #sprawdzanie danych 
        malpa = e_mail.find("@")  
        if malpa == -1 :
            return "blad przy wpisywaniu e-mail: brakuje @"

        cursor.execute("""SELECT * FROM Osoby WHERE e_mail = %(e_mail)s  """, {'e_mail': e_mail})
        conn.commit()
        user = cursor.fetchone()
        print("logowanie dziala")
        admin ='admin@admin.pl'
        hashed = bcrypt.hashpw(passwd.encode('utf-8'), user[6].encode('utf-8')).decode('utf-8')
        if hashed == user[6]:
            print("zalogowano!")
            session['imie'] = user[1]
            session['osoba_ID']=user[0]
            if user[5] == admin:
                return redirect("/admin")
            else:    
                return redirect("/home")
            #return redirect("/home")
    else:
        return render_template('login_form.html')


# filmy użytkownika
@app.route('/user', methods=['GET'])
def user():
   fk_osoba = session['osoba_ID']
   if request.method == 'GET':
       cursor.execute(""" SELECT Wypozyczenia.wypozyczenie_ID, Wypozyczenia.Data_wypozyczenia, Wypozyczenia.Data_oddania ,Filmy.tytul, Wypozyczenia.fk_osoba FROM Wypozyczenia INNER JOIN Filmy ON Wypozyczenia.fk_film= Filmy.film_ID 
         WHERE Wypozyczenia.fk_osoba=%(fk_osoba)s """, {'fk_osoba': fk_osoba} )
       conn.commit()
       rows = cursor.fetchall()
       return render_template('wypozyczeniaUser.html', rows=rows)


# wylogowywanie sie
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/home")


# wypozyczanie filmu
@app.route('/wypozycz', methods=['GET', 'POST'])
def getmovie():
    if request.method == 'GET':
        return render_template("wypozycz.html", rows=rows)
    else:
        fk_film = str(request.form['fk_film'])
        fk_osoba = session['osoba_ID']
        Data_wypozyczenia = str(request.form['Data_wypozyczenia'])
        Data_oddania = str(request.form['Data_oddania'])
        
        #sprawdzanie poprawnosci wprowadzonych danych
        fk_lower = fk_film.lower()
        contains_letter = fk_lower.islower()
        if contains_letter == True: 
            return "Blad: ID filmu zawiera litery"

        data1_lower = Data_oddania.lower()
        contains_letter = data1_lower.islower()
        if contains_letter == True: 
            return "Blad: Data zawiera litery"    
        
        data2_lower = Data_wypozyczenia.lower()
        contains_letter = data2_lower.islower()
        if contains_letter == True: 
            return "Blad: Data zawiera litery"  
        

        cursor.execute(
            """INSERT INTO Wypozyczenia ( Data_wypozyczenia, Data_oddania, fk_osoba, fk_film) VALUES (%(
            Data_wypozyczenia)s, %(Data_oddania)s, %(fk_osoba)s, %(fk_film)s )""",
            {'Data_wypozyczenia': Data_wypozyczenia,
             'Data_oddania': Data_oddania,
             'fk_osoba': fk_osoba,
             'fk_film': fk_film } )
        conn.commit()
        return redirect("/user")  


# zwracanie filmow
@app.route('/oddaj', methods=['GET', 'POST', 'DELETE'])
def returnmovie():
    fk_osoba = session['osoba_ID']
    if request.method == 'GET':
        cursor.execute(""" SELECT Wypozyczenia.wypozyczenie_ID, Wypozyczenia.Data_wypozyczenia, Wypozyczenia.Data_oddania ,Filmy.tytul, Wypozyczenia.fk_osoba FROM Wypozyczenia INNER JOIN Filmy ON Wypozyczenia.fk_film= Filmy.film_ID 
         WHERE Wypozyczenia.fk_osoba=%(fk_osoba)s """, {'fk_osoba': fk_osoba})
        rows = cursor.fetchall()
        return render_template("oddaj.html", rows=rows)
    else:
        wypozyczenie_ID = str(request.form['wypozyczenie_ID'])
        
        #sprawdzanie poprawnosci wprowadzonych danych
        _lower = wypozyczenie_ID.lower()
        contains_letter = _lower.islower()
        if contains_letter == True: 
            return "Blad: ID wypozyczenia zawiera litery"
        
        fk_osoba = session['osoba_ID']
        cursor.execute(""" DELETE FROM Wypozyczenia WHERE wypozyczenie_ID= %(wypozyczenie_ID)s""",
                       {'wypozyczenie_ID': wypozyczenie_ID})
        conn.commit()
        print("po execute")
        return redirect("/user")  


@app.route('/contact')
def contact():
    return render_template("contact.html")

app.secret_key = " tr3yg4iwyhbfskcb74yir3hufw"
app.run()
