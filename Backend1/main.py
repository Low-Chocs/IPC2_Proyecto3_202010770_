from flask import Flask, request, jsonify
from flask.json import jsonify
from read_file import load_XML
from dictionary import getters

app = Flask(__name__)
load_xml = load_XML()
total_messages = []


@app.route('/')
def index():
    return "Hola soy una Api"

@app.route('/readfile', methods=['POST'])
def reading():
    xml = request.get_data().decode('utf-8')
    return load_xml.element_tree(xml, total_messages)

@app.route('/getMessages', methods=['GET'])
def get_messages():
    hola = getters(total_messages)
    return hola.json_generator_messages()

@app.route('/getCompany', methods=['GET'])
def get_messages_company():
    hola = getters(total_messages)
    return hola.json_generator_company()

@app.route('/getPositive', methods=['GET'])
def get_messages_positive():
    hola = getters(total_messages)
    return hola.json_generator_status_positive()

@app.route('/getNegative', methods=['GET'])
def get_messages_negative():
    hola = getters(total_messages)
    return hola.json_generator_status_negative()


if __name__ == '__main__':
    app.run(debug = True, port = 4000)