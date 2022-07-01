from flask import Flask, jsonify, request
from datetime import date

def to_datetime(date_string):
    date_list = date_string.split("-")
    date_list = list(map(lambda x: int(x), date_list))
    a,m,d = date_list
    return date(a,m,d)

def format_date(date_string):
    date_list = date_string.split("-")
    a,m,d = date_list
    return f"{d}/{m}/{a}"

app = Flask(__name__)

@app.route('/age', methods=['POST'])
def age_post():
    data = dict(request.get_json())
    name, birth, dateThen = [value for value in data.values()]

    birth_datetime = to_datetime(birth)
    dateThen_datetime = to_datetime(dateThen)

    ageNow = (date.today() - birth_datetime).days // 365
    ageThen = (dateThen_datetime - birth_datetime).days // 365

    dateThen = format_date(dateThen)

    quote = f"Olá, {name}! Você tem {ageNow} anos e em {dateThen} você terá {ageThen} anos."
    
    response = {
        "quote": quote,
        "ageNow": ageNow,
        "ageThen": ageThen
    }

    return jsonify(response)

app.run()