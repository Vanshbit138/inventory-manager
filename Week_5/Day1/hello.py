from flask import Flask

# Create a Flask application instance
app = Flask(__name__)


@app.route("/")
def hello_world():
    """
    Description:
        This endpoint returns a simple "Hello, World!" message.
        It demonstrates how a Flask route works and how to handle GET requests.

    HTTP Method:
        GET

    URL:
        http://127.0.0.1:5000/

    Returns:
        str: A greeting message.
    """
    return "Hello, World!"


if __name__ == "__main__":
    # Run the Flask application on localhost:5000
    app.run(debug=True)
