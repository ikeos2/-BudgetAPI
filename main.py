from flask import Flask, request
import sqlalchemy
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Test'


@app.route('/add', methods=['POST'])
def add_item():
    data = request.data
    return request.form.get("key")


@app.route('/update')
def update_item():
    return "update"
w