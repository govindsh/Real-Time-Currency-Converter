import sqlite3 as lite
import sys

conn = lite.connect('currency.db')


def create_table():
    with conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE currency_list (country_code TEXT PRIMARY KEY, description TEXT);")
        conn.commit()


def insert_currency(currency_code, description):
    with conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO currency_list VALUES('{0}', '{1}')".format(currency_code, description))
        conn.commit()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "create":
            create_table()
    currency_dict = {}
    currency_dict["AUD"] = "Australian Dollar"
    currency_dict["BGN"] = "Bulgarian Lev"
    currency_dict["BRL"] = "Brazilian Real"
    currency_dict["CAD"] = "Canadian Dollar"
    currency_dict["CHF"] = "Swiss Franc"
    currency_dict["CNY"] = "Chinese Yuan"
    currency_dict["CZK"] = "Czech Koruna"
    currency_dict["DKK"] = "Danish Krone"
    currency_dict["GBP"] = "Great Britain Pound"
    currency_dict["HKD"] = "Hong Kong Dollar"
    currency_dict["HRK"] = "Croatian Kuna"
    currency_dict["HUF"] = "Hungarian Forint"
    currency_dict["IDR"] = "Indonesian Rupiah"
    currency_dict["ILS"] = "Israeli New Shekel"
    currency_dict["INR"] = "Indian Rupee"
    currency_dict["JPY"] = "Japanese Yen"
    currency_dict["KRW"] = "South Korean Won"
    currency_dict["MXN"] = "Mexican Peso"
    currency_dict["MYR"] = "Malaysian Ringgit"
    currency_dict["NOK"] = "Norwegian Krone"
    currency_dict["NZD"] = "New Zealand Dollar"
    currency_dict["PHP"] = "Philippine Peso"
    currency_dict["PLN"] = "Polish Zloty"
    currency_dict["RON"] = "Romanian Leu"
    currency_dict["RUB"] = "Russian Ruble"
    currency_dict["SEK"] = "Swedish Krona"
    currency_dict["SGD"] = "Singapore Dollar"
    currency_dict["THB"] = "Thai Baht"
    currency_dict["TRY"] = "Turkish Lira"
    currency_dict["ZAR"] = "South African Rand"
    currency_dict["EUR"] = "Euro"
    currency_dict["USD"] = "US Dollar"

    for key, value in currency_dict.items():
        insert_currency(key, value)
    conn.close()
