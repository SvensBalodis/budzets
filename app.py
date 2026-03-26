from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

DATA_FILE = "dati.csv"
dati = []

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    return []

def save_data():
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['tips', 'summa', 'apraksts']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for ieraksts in dati:
            writer.writerow(ieraksts)

def calculate_balance():
    ienakumi = sum(float(x['summa']) for x in dati if x['tips'] == 'Ienākumi')
    izdevumi = sum(float(x['summa']) for x in dati if x['tips'] == 'Izdevumi')
    return ienakumi - izdevumi

@app.route('/')
def index():
    bilance = calculate_balance()
    return render_template("index.html", dati=dati, bilance=bilance)

@app.route('/dzest', methods=['POST'])
def dzest():
    dati.clear()
    save_data()
    return redirect('/')

@app.route('/pievienot', methods=['POST'])
def pievienot():
    summa = request.form.get('summa')
    apraksts = request.form.get('apraksts')
    tips = request.form.get('tips')


    ieraksts = {'tips': tips, 'summa': summa, 'apraksts': apraksts}
    dati.append(ieraksts)
    save_data()
    return redirect('/')

if __name__ == "__main__":
    dati = load_data()
    app.run(debug=True)