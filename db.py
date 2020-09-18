import pymysql.cursors
from flask import flash, session
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
def insert_user(name, surname, age, username, email, password):
    try:
        conn = connection()
        with conn.cursor() as cursor:
            # Create table if not exists
            sqlQuery = '''CREATE TABLE IF NOT EXISTS `user` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                        `surname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                        `age` date NULL DEFAULT NULL,
                        `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                        `username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                        `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                        PRIMARY KEY (`id`) USING BTREE
                        ) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic'''
            cursor.execute(sqlQuery)

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
                session['logged_in'] = False
                if bcrypt.verify(password, real_password):
                    flash("Successful login!", 'success')
                    session['logged_in'] = True
                    session['username'] = username
                    session['user_id'] = data['id']
                    session['user'] = (data['name'] + ' ' + data['surname'])
                    return True
                else:
                    flash("Password is incorrect!", 'danger')
                    return False
            else:
                flash("There is no user by this username!", 'danger') 
                return False

    finally:
        conn.close()

# Inset article
def insert_article(title, content, user_id):
    try:
        conn = connection()
        with conn.cursor() as cursor:
            # Create table if not exists
            sqlQuery = '''CREATE TABLE IF NOT EXISTS `article` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
                        `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
                        `created_date` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        `user_id` int(11) NOT NULL,
                        PRIMARY KEY (`id`) USING BTREE,
                        INDEX `author`(`author`) USING BTREE,
                        CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `myblog`.`user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
                        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic'''
            cursor.execute(sqlQuery)

            query = 'INSERT INTO article (title, content, user_id) VALUES (%s, %s, %s)'
            cursor.execute(query, (title, content, user_id))
            conn.commit()
            flash("Process complete successfully!", 'success')
    finally:
        conn.close()

# select articles

def select_articles():

    try:
        conn = connection()
        with conn.cursor() as cursor:
            query = 'SELECT DISTINCT A.title, A.content, A.created_date, U.name, U.surname from article A INNER JOIN user U on U.id = A.user_id'
            result = cursor.execute(query)
            if result > 0:
                articles = cursor.fetchall()
                return articles
            else:
                return None

    finally:
        conn.close()

# select articles by author

def select_articles_by_outhor(user_id):
    try:
        conn = connection()
        with conn.cursor() as cursor:
            query = 'SELECT * from article A WHERE A.user_id = %s'
            result = cursor.execute(query, (user_id,))
            if result > 0:
                articles = cursor.fetchall()
                return articles
            else:
                return None
    finally:
        conn.close()