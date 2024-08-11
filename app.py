from flask import Flask

app = Flask(__name__)

with app.app_context():
    from src import routes as routes  # noqa:401

if __name__ == "__main__":
    app.run(host="0.0.0.0")
