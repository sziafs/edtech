import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book

class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "postgres" # postgres_test
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_book = {
            'title': 'Anansi Boys',
            'author': 'Neil Gaiman',
            'rating': 5
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_get_paginated_books(self):
        res = self.client().get('/books') # response is the client getting that endpoint
        data = json.loads(res.data) # getting the response data

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books']) # assert true there is a number of certain books
        self.assertTrue(len(data['books'])) # assert there is a lenght of data books

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/books?page=1000', json={'rating': 1}) # and this json body shouldn't be used
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_book_rating(self):
        res = self.client().patch('/books/12', json={'rating': 1}) # atualizando o rating do book 5
        data = json.loads(res.data)
        book = Book.query.filter(Book.id == 12).one_or_none() # pegando o livro atualizado depois

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(book.format()['rating'], 1) # checar se a atualizacao aconteceu mesmo
        
    def test_400_for_failed_update(self):
        res = self.client().patch('/books/6') # manda atualizar sem body tem que dar 400
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
    
    # def test_delete_book(self):
    #     res = self.client().delete('/books/7') # deletar o livro 1
    #     data = json.loads(res.data)

    #     book = Book.query.filter(Book.id == 7).one_or_none() # pega o livro 1

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted']['id'], 7)
    #     self.assertTrue(data['total_books'])
    #     self.assertTrue(len(data['books']))
    #     self.assertEqual(book, None) # 81, se nao tiver vem None, checar se eh None mesmo
        
    def test_422_if_book_does_not_exist(self):
        res = self.client().delete('/books/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_create_new_book(self):
        res = self.client().post('/books', json=self.new_book) # pega o json do res??
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['books']))
    
    def test_405_if_book_creation_not_allowed(self):
        res = self.client().post('/books/45', json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_get_book_search_with_results(self):
        res = self.client().post('/books', json={'search': 'Novel'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertEqual(len(data['books']), 4)

    def test_get_book_search_without_results(self):
        res = self.client().post('/books', json={'search': 'applejacks'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_books'], 0)
        self.assertEqual(len(data['books']), 0)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()