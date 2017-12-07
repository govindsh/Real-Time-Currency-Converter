from flask import Flask, render_template, request
import requests
import sqlite3 as lite
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    formatted_currency_list, formatted_currency_list_and_description = get_currency_and_description_from_db(both_queries=True)

    return render_template('index.html', currency_list=formatted_currency_list,
                            currency_list_and_description=formatted_currency_list_and_description)


@app.route('/convert_currency', methods=['post', 'get'])
def convert_currency():
    currency_i_have = None
    currency_i_want = None
    pro_or_novice = None
    messages=[]

    try:
        pro_or_novice = request.form["personType"]
    except KeyError:
        if pro_or_novice is None:
            messages.append("please choose one of the radio buttons.")
            return render_template('error.html', messages=messages)
    if pro_or_novice == "pro":
        try:
            currency_i_have = request.form["pro_currency_i_have"]
            currency_i_want = request.form["pro_currency_i_want"]
        except KeyError:
            if currency_i_have is None or currency_i_want is None:
                messages.append("Please select currency for conversion. It cannot be left empty.")
                return render_template('error.html', messages=messages)

        response = requests.get(url="http://api.fixer.io/latest?base={0}".format(currency_i_have))


    else:
        # Type is novice
        try:
            currency_i_have = request.form["novice_currency_i_have"]
            currency_short_have = str(currency_i_have).split(" - ")[0]
            currency_i_want = request.form["novice_currency_i_want"]
            currency_short_want = str(currency_i_want).split(" - ")[0]
        except KeyError:
            if currency_i_have is None or currency_i_want is None:
                messages.append("Please select currency for conversion. It cannot be left empty.")
                return render_template('error.html', messages=messages)

        response = requests.get(url="http://api.fixer.io/latest?base={0}".format(currency_short_have))

    if response.status_code != 200:
        messages.append("An Error occured - Status Code: {0}. Please try again later.".format(response.status_code))
        return render_template('error.html', messages=messages)
    output = response.json()

    days = 10
    count = 2
    response = None
    date_and_result = {}
    while count < days:
        previous_date = (datetime.datetime.today() - datetime.timedelta(days=count)).strftime("%Y-%m-%d")
        if pro_or_novice == "pro":
            response = requests.get(url="http://api.fixer.io/latest?base={0}&date={1}".format(currency_i_have, previous_date))
            date_and_result[previous_date] = response.json()["rates"][currency_i_want]
        else:
            response = requests.get(url="http://api.fixer.io/latest?base={0}&date={1}".format(currency_short_have, previous_date))
            date_and_result[previous_date] = response.json()["rates"][currency_short_want]
        count += 1

    if pro_or_novice == "pro":
        conversion_value = output["rates"][currency_i_want]
        return render_template('convert.html', pro_or_novice=pro_or_novice, currency_i_have=currency_i_have,
                           currency_i_want=currency_i_want, output=output, conversion_value=conversion_value,
                               result=date_and_result)
    else:
        conversion_value = output["rates"][currency_short_want]
        return render_template('convert.html', pro_or_novice=pro_or_novice, currency_i_have=currency_i_have,
                           currency_i_want=currency_i_want, output=output, conversion_value=conversion_value,
                               result=date_and_result)


@app.route('/list_of_supported_countries')
def supported_currencies():
    formatted_currency_list_and_description = get_currency_and_description_from_db(both_queries=False)
    return render_template('supported_currencies.html', supported_currencies=formatted_currency_list_and_description)


@app.route('/about_site')
def about_site():
    return render_template('about_site.html')

# Helper Method
def get_currency_and_description_from_db(both_queries=True):
    formatted_currency_list_and_description = []
    formatted_currency_list = []
    conn = lite.connect('currency.db')
    cursor = conn.cursor()
    if both_queries is True:

        cursor.execute('SELECT country_code from currency_list')
        currency_list = cursor.fetchall()

        for currency in currency_list:
            currency = str(currency).strip("('',)")
            formatted_currency_list.append(currency)

    cursor.execute('SELECT * from currency_list')
    currency_list_and_description = cursor.fetchall()

    for description in currency_list_and_description:
        description = str(description).strip("('','')")
        description = description.replace("', '", " - ")
        formatted_currency_list_and_description.append(description)

    if both_queries is True:
        return formatted_currency_list, formatted_currency_list_and_description
    else:
        return formatted_currency_list_and_description

if __name__ == '__main__':
    app.Debug = True
    app.secret_key = "money_money_money"
    app.run(host="0")