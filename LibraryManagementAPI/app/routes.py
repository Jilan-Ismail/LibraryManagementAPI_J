from flask import Blueprint, request, jsonify
import json

app = Blueprint('routes', __name__)
DATA_FILE = 'books.json'


def load_books():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_books(books):
    with open(DATA_FILE, 'w') as file:
        json.dump(books, file, indent=4)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the Library Management API. Visit /api-docs for API documentation."}), 200



@app.route('/books', methods=['POST'])
def add_book():
    """
    Add a new book.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            published_year:
              type: integer
            isbn:
              type: string
            genre:
              type: string
    responses:
      200:
        description: Book added successfully
      400:
        description: Missing required fields
    """
    books = load_books()
    data = request.json
    required_fields = ['title', 'author', 'published_year', 'isbn']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required.'}), 400
    books.append(data)
    save_books(books)
    return jsonify({'message': 'Book added successfully'}), 200


@app.route('/books', methods=['GET'])
def list_books():
    """
    List all books.
    ---
    responses:
      200:
        description: A list of books
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
              author:
                type: string
              published_year:
                type: integer
              isbn:
                type: string
              genre:
                type: string
    """
    books = load_books()
    return jsonify(books), 200


@app.route('/books/search', methods=['GET'])
def search_books():
    """
    Search books.
    ---
    parameters:
      - name: author
        in: query
        type: string
        required: false
      - name: published_year
        in: query
        type: integer
        required: false
      - name: genre
        in: query
        type: string
        required: false
    responses:
      200:
        description: Filtered list of books
    """
    books = load_books()
    author = request.args.get('author')
    published_year = request.args.get('published_year')
    genre = request.args.get('genre')
    filtered_books = [
        book for book in books
        if (not author or book['author'] == author) and
           (not published_year or str(book['published_year']) == published_year) and
           (not genre or book['genre'] == genre)
    ]
    return jsonify(filtered_books), 200


@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    """
    Delete a book by ISBN.
    ---
    parameters:
      - name: isbn
        in: path
        required: true
        type: string
    responses:
      200:
        description: Book deleted successfully
      404:
        description: Book not found
    """
    books = load_books()
    updated_books = [book for book in books if book['isbn'] != isbn]
    if len(books) == len(updated_books):
        return jsonify({'error': 'Book not found'}), 404
    save_books(updated_books)
    return jsonify({'message': 'Book deleted successfully'}), 200


@app.route('/books/<isbn>', methods=['PATCH'])
def update_book(isbn):
    """
    Update book details.
    ---
    parameters:
      - name: isbn
        in: path
        required: true
        type: string
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            published_year:
              type: integer
            isbn:
              type: string
            genre:
              type: string
    responses:
      200:
        description: Book updated successfully
      404:
        description: Book not found
    """
    books = load_books()
    data = request.json
    for book in books:
        if book['isbn'] == isbn:
            book.update(data)
            save_books(books)
            return jsonify({'message': 'Book updated successfully'}), 200
    return jsonify({'error': 'Book not found'}), 404


@app.route('/books/<isbn>', methods=['GET'])
def get_book(isbn):
    """
    Get a single book by ISBN.
    ---
    parameters:
      - name: isbn
        in: path
        required: true
        type: string
    responses:
      200:
        description: Details of the requested book
      404:
        description: Book not found
    """
    books = load_books()
    for book in books:
        if book['isbn'] == isbn:
            return jsonify(book), 200
    return jsonify({'error': 'Book not found'}), 404

