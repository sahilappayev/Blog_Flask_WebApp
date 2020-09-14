import pymysql.cursors
from flask import flash
from passlib.hash import bcrypt

# Db configuration
try:
    # Create db if not exist
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='12345')
    # Simulate the CREATE DATABASE function of mySQL
    with connection.cursor() as cursor:
        cursor.execute('CREATE DATABASE IF NOT EXISTS myblog')
        connection.commit()
finally:
    connection.close()

# Connect db
def connection():
    con = pymysql.connect(host='localhost',
                                user='root',
                                password='12345',
                                db='myblog',
                                cursorclass=pymysql.cursors.DictCursor)
    return con

# Inset user
def insert(name, surname, age, username, email, password):
    try:
        conn = connection()
        with conn.cursor() as cursor:
            # Create table if not exists
            sqlQuery = '''CREATE TABLE IF NOT EXISTS `user` (
                                            `id` int(11) NOT NULL AUTO_INCREMENT,
                                            `name` varchar(255) NOT NULL,
                                            `surname` varchar(255) NOT NULL,
                                            `age` date DEFAULT NULL,
                                            `email` varchar(255) NOT NULL,
                                            `username` varchar(50) NOT NULL,
                                            `password` varchar(255) NOT NULL,
                                            PRIMARY KEY (`id`)
                                            ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8'''
            cursor.execute(sqlQuery)

            print(cursor)

            query = "INSERT INTO `user` (`name`, `surname`, `age`, `username`, `email`, `password`) VALUES (%s, %s, %s, %s, %s, %s)"
            print("Args:  ",(name, surname, age, username, email, password))
            cursor.execute(query, (name, surname, age, username, email, password))
            conn.commit()
            flash("Register complete successfully!", 'success')
    finally:
        conn.close()

# login user
def user_login(username, password):
    try:
        conn = connection()
        with conn.cursor() as cursor:
            query = 'SELECT * FROM user WHERE username = %s'
            result = cursor.execute(query, (username,))

            if result > 0:
                data  = cursor.fetchone()
                real_password = data['password']
                if bcrypt.verify(password, real_password):
                    flash("Successful login!", 'success')
                    return True
                else:
                    flash("Password is incorrect!", 'danger')
                    return False
            else:
                flash("There is no user by this username!", 'danger') 
                return False

    finally:
        conn.close()