from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)
CSV_FILE = 'inventory.csv'

def load_data():
    return pd.read_csv(CSV_FILE)

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

def calc_status(stock):
    if stock >= 3:
        return "〇"
    elif stock >= 1:
        return "△"
    else:
        return "×"

@app.route('/')
def index():
    df = load_data()
    df["状態"] = df["在庫数"].apply(calc_status)
    return render_template("index.html", items=df.to_dict(orient="records"))

@app.route('/update', methods=['POST'])
def update():
    df = load_data()
    idx = int(request.form['index'])
    action = request.form['action']
    if action == 'use' and df.at[idx, '在庫数'] > 0:
        df.at[idx, '在庫数'] -= 1
    elif action == 'add':
        df.at[idx, '在庫数'] += 1
    save_data(df)
    return redirect('/')

@app.route('/reset_check', methods=['POST'])
def reset_check():
    df = load_data()
    df["チェック済み"] = False
    save_data(df)
    return redirect('/')

@app.route('/toggle_check/<int:index>', methods=['POST'])
def toggle_check(index):
    df = load_data()
    df.at[index, 'チェック済み'] = not df.at[index, 'チェック済み']
    save_data(df)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
