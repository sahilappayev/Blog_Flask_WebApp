import pymysql.cursors

# Db configuration
# Create db if not exist
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='12345')
 
# Simulate the CREATE DATABASE function of mySQL
try:
    with connection.cursor() as cursor:
        cursor.execute('CREATE DATABASE IF NOT EXISTS myblog')
finally:
    connection.close()

# Connect db
def connection():
    conn = pymysql.connect(host='localhost',
                             user='root',
                             password='12345',
                             db='myblog',
                             cursorclass=pymysql.cursors.DictCursor)
    return conn


# Inset user
def insert(name, surname, age, username, email, password):
    try:
        with connection().cursor() as cursor:
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

            query = "INSERT INTO user (name, surname, age, username, email, password) VALUES (%s, %s,%s, %s, %s, %s)"
            cursor.execute(query, (name, surname, age, username, email,password))
            connection().commit()
    finally:
        connection().close()