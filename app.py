from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)


@app.route("/")
def index_page():
 return render_template("index.html")

@app.route("/results", methods=['GET'])
def results_page():
    # Get the genre from the query parameters
    genre = request.args.get('genre', '').lower()

    # Make a request to the /consume route with the genre as a query parameter
    response = requests.get(f'book-api-server-consume.dycqcecabah7djgd.uksouth.azurecontainer.io:5001/consume?genre={genre}')

    if response.ok:
        # If the request is successful, pass the JSON data to the template
        books = response.json()
        return render_template("results.html", books=books)
    else:
        # If there is an error, render an error template or handle it accordingly
        return "Failed to retrieve data from the service", 500


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
            return jsonify({"error": "No books found matching the criteria"}), 404
    else:
        return "Failed to retrieve data from the service", 500

    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
