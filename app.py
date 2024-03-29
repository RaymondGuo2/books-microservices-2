from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)


@app.route("/")
def index_page():
 return render_template("index.html")


@app.route('/consume', methods=['GET'])
def consume():
    url_service = 'http://book-api-server-lab1.e3dtdraufbbmcmg3.uksouth.azurecontainer.io:5000/books'

    genre = request.args.get('genre', '').lower()

    if genre:
        url_service += f'?genre={genre}'

    response = requests.get(url_service)
    if response.ok:
        books = response.json()

        if genre:
            books = [book for book in books if genre in book.get('genre', '').lower()]
        if len(books) == 0:
            return render_template("results.html")
    else:
        return "Failed to retrieve data from the service", 500

    return render_template("results.html", books=books)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
