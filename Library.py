# Implement Library Management System with Flask and CRUD operation using REST API with integration of MySQL.

from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_restful import Api, Resource

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Golden@2020'
app.config['MYSQL_DB'] = 'mydb'

api = Api(app)

mysql = MySQL(app)


class Book(Resource):
    def get(self, BookID):
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM books WHERE BookId = {BookID}")
        book = cur.fetchone()
        cur.close()
        if book:
            return jsonify({'BookID': book[0], 'BookName': book[1], 'Author': book[2]})
        return jsonify({'message': 'Book not found'}), 404
    
    def delete(self, BookID):
        cur = mysql.connection.cursor()
        cur.execute(f"DELETE FROM books WHERE BookId = {BookID}")
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Book deleted successfully'})

class BookPost(Resource):

    def put(self):
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute(f"UPDATE books SET BookName = '{data['BookName']}', Author = '{data['Author']}' WHERE BookId = {data['BookID']}")        
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Book updated successfully'})
    
    def post(self):
            data = request.get_json()
            cur = mysql.connection.cursor()
            cur.execute(f"INSERT INTO books (BookID, BookName, Author) VALUES ({data['BookID']}, '{data['BookName']}', '{data['Author']}')")
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'Book added successfully'})


api.add_resource(BookPost, '/books/')
api.add_resource(Book, '/books/<int:BookID>')


if __name__ == '__main__':
    app.run()
