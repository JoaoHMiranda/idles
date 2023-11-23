from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    return sqlite3.connect('banco.db')

def check_word_from_database(verif):
    with get_db_connection() as connection:
        print(verif)
        cursor = connection.cursor()
        consulta = "SELECT palavra FROM palavras WHERE palavra = ?"
        verif.upper()
        cursor.execute(consulta, (verif,))
        resultados = cursor.fetchall()
        print(resultados)
        if resultados:
            return 1
        return -1

def get_word_from_database():
    with get_db_connection() as connection:
        cursor = connection.cursor()
        consulta = "SELECT palavra FROM palavras ORDER BY RANDOM() LIMIT 1;"
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        print(resultados[0][0].upper())
        return resultados[0][0].upper()

def get_login_from_database(login, password):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        consulta = "SELECT count(*) FROM user WHERE username=? AND password=?;"
        login.lower()
        cursor.execute(consulta, (login, password))
        resultados = cursor.fetchall()
        print(resultados[0][0])
        return resultados[0][0]
    
def get_username_from_database(login):
     with get_db_connection() as connection:
        cursor = connection.cursor()
        login.lower()
        consulta = "SELECT count(*) FROM user WHERE username=?;"
        cursor.execute(consulta, (login))
        resultados = cursor.fetchall()
        if resultados:
            return -1
        return 1
    
def insert_login_in_database(login, password):
    with get_db_connection() as connection:
        if get_username_from_database(login):
            login.lower()
            cursor = connection.cursor()
            consulta = "insert into user(username,password) values(?,?);"
            cursor.execute(consulta, (login, password))
            return 1
        return -1
    
def delete_login_in_database(login, password):
    with get_db_connection() as connection:
        if get_login_from_database(login,password):
            login.lower()
            cursor = connection.cursor()
            consulta = "delete from user WHERE username=?;"
            cursor.execute(consulta, (login, password))
            return 1
        return -1        

def update_login_username_database(login, password,newlogin):
    with get_db_connection() as connection:
        if get_login_from_database(login,password):
            login.lower()
            cursor = connection.cursor()
            consulta = "update user set usermane =? where username=?;"
            cursor.execute(consulta, (newlogin, login))
            return 1
        return -1

def update_login_senha_database(login, password,newpassword):
    with get_db_connection() as connection:
        if get_login_from_database(login,password):
            login.lower()
            cursor = connection.cursor()
            consulta = "update user set password=? where username=?;"
            cursor.execute(consulta, (newpassword, login))
            return 1
        return -1
    
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/get_data')
def get_data():
    palavra = get_word_from_database()
    return jsonify({'data': palavra})

@app.route('/get_login', methods=['POST'])
def get_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    conf = get_login_from_database(login=username, password=password)
    return jsonify({'data': conf})

@app.route('/check_word', methods=['POST'])
def check_word():
    data = request.get_json()
    conf = check_word_from_database(verif=(data.get("word")))
    return jsonify({'data': conf})

if __name__ == '__main__':
    app.run(debug=True)
