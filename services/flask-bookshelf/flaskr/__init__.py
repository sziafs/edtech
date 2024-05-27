"""
    $env:FLASK_APP='app'
    $env:FLASK_ENV='development'
"""

import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

def paginate_books(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF

    books = [book.format() for book in selection]
    current_books = books[start:end]

    return current_books

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    # CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/books')
    def index():
        selection = Book.query.order_by(Book.id).all()
        current_books = paginate_books(request, selection)

        if len(current_books) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'books': current_books,
            'total_books': len(Book.query.all())
        })


    @app.route('/books/<int:book_id>')
    def show(book_id):
        book = Book.query.filter(Book.id == book_id).one_or_none()
        if book is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'book': book.format(),
            })

    # uma rota separada para search com POST quebra o create
    # @app.route('/books', methods=['POST'])
    # def search():
    #     body = request.get_json()
    #     search = body.get('search', None)

    #     try:
    #         selection = Book.query.order_by(Book.id).filter(Book.title.ilike('%{}%'.format(search)))
    #         current_books = paginate_books(request, selection)

    #         return jsonify({
    #             'success': True,
    #             'books': current_books,
    #             'total_books': len(selection.all())
    #         })

    #     except:
    #         abort(422)
            
    
    
    @app.route('/books', methods=['POST'])
    def store():
        body = request.get_json()

        new_title = body.get('title', None) # (from body, default)
        new_author = body.get('author', None)
        new_rating = body.get('rating', None)

        search = body.get('search', None)

        try:
            if search: # if there's a search on post
                selection = Book.query.order_by(Book.id).filter(Book.title.ilike('%{}%'.format(search)))
                current_books = paginate_books(request, selection)

                return jsonify({
                    'success': True,
                    'books': current_books,
                    'total_books': len(selection.all())
                })

            else:
                book = Book(title=new_title, author=new_author, rating=new_rating)
                book.insert()

                selection = Book.query.order_by(Book.id).all()
                current_books = paginate_books(request, selection)

                return jsonify({
                    'success': True,
                    'created': book.format(),
                    'books': current_books,
                    'total_books': len(Book.query.all())
                })

        except:
            abort(422)


    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def update(book_id):
        body = request.get_json() # the body from the request

        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None:
                abort(404) # not found
            
            if 'rating' in body: # only allowed info to be updated
                book.rating = int(body.get('rating'))
            
            book.update()

            return jsonify({
                'success': True,
                'updated': book.format()
            })

        except:
            abort(400)


    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None:
                abort(404)
            
            book.delete()

            selection = Book.query.order_by(Book.id).all()
            current_books = paginate_books(request, selection)

            return jsonify({
                'success': True,
                'deleted': book.format(),
                'books': current_books,
                'total_books': len(Book.query.all())
            })

        except:
            abort(422)


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
            }), 400


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            
            "error": 404,
            "message": "resource not found"
            }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "method not allowed"
            }), 405


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

    return app

