from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from send_notification import send_email
from update_stock import update_stock
import sqlite3

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = '4490b730e7f9b46182e20f6c7de5f4de'

# ---- Home Route ----
@app.route('/')
def index():
    conn = get_db_connection()
    medicines = conn.execute('SELECT * FROM medicines').fetchall()
    conn.close()

    return render_template('index.html', medicines=medicines)

# ---- Search Route ----
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicines WHERE name LIKE ? OR category LIKE ?", 
                       ('%' + query + '%', '%' + query + '%'))
        medicines = cursor.fetchall()
        conn.close()
        return render_template('index.html', medicines=medicines)
    return redirect(url_for('index'))


# ---- Update Stock Route ----
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    try:
        new_stock = int(request.form['stock'])
        conn = get_db_connection()

        #Call the updated function
        result = update_stock(conn, id, new_stock)
        
        if result:
            flash(f"Stock for {result['name']} updated successfully!", "success")

        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Error updating stock: {str(e)}", "danger")
        return redirect(url_for('index'))


# ---- Add New Medicine Route ----
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    category = request.form['category']
    stock = request.form['stock']
    pharmacy = request.form['pharmacy']
    location = request.form['location']

    try:
        stock = int(stock)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medicines (name, category, stock, pharmacy, location) VALUES (?, ?, ?, ?, ?)", 
                       (name, category, stock, pharmacy, location))
        conn.commit()
        conn.close()
        flash(f"{name} added successfully!", "success")
        return redirect(url_for('index'))
    except ValueError:
        flash("Invalid stock value. Please enter a valid integer.", "error")
        return redirect(url_for('index'))


# ---- Delete Medicine Route ----
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicines WHERE id = ?", (id,))
        result = cursor.fetchone()

        if result:
            cursor.execute("DELETE FROM medicines WHERE id = ?", (id,))
            conn.commit()
            flash(f"✅ {result['name']} deleted successfully!", "success")  #Ensure flash message is defined correctly
        else:
            flash("❌ Medicine not found.", "danger")

        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"❌ Error deleting medicine: {str(e)}", "danger")
        return redirect(url_for('index'))

def get_medicine_by_id(id):
    conn = get_db_connection()
    medicine = conn.execute('SELECT * FROM medicines WHERE id = ?', (id,)).fetchone()
    conn.close()
    return medicine

# ---- Stock Charts ----
import plotly.express as px
from flask import Flask, render_template
import sqlite3
import pandas as pd
import numpy as np

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/stock_chart_data')
def stock_chart_data():
    conn = get_db_connection()
    medicines = conn.execute('SELECT * FROM medicines').fetchall()
    conn.close()

    names = [medicine['name'] for medicine in medicines]
    stocks = [medicine['stock'] for medicine in medicines]

    bar_chart = {
        'data': [{
            'x': names,
            'y': stocks,
            'type': 'bar',
            'name': 'Stock Levels',
            'marker': {'color': '#63e6fa'}
        }],
        'layout': {
            'title': 'Stock Levels',
            'xaxis': {'title': 'Medicine'},
            'yaxis': {'title': 'Stock Level'}
        }
    }

    pie_chart = {
        'data': [{
            'labels': names,
            'values': stocks,
            'type': 'pie'
        }],
        'layout': {
            'title': 'Stock by Category'
        }
    }

    return jsonify(bar_chart=bar_chart, pie_chart=pie_chart)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# ---- Run the Flask App ----
if __name__ == '__main__':
    app.run(debug=True)