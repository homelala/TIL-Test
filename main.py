from flask import Flask


app = Flask(__name__)

@app.route("/")
def test():
    return "success"

from view import register_app

register_app(app)

if __name__ == '__main__':
    app.run("127.0.0.1", port=8080)
