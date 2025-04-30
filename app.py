from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            units INTEGER,
            rate REAL,
            total REAL,
            date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO customers (name, address) VALUES (?, ?)", (name, address))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_customer.html')

@app.route('/generate_bill', methods=['GET', 'POST'])
def generate_bill():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        units = int(request.form['units'])
        rate = 5.5  # example rate
        total = units * rate
        date = request.form['date']
        c.execute("INSERT INTO bills (customer_id, units, rate, total, date) VALUES (?, ?, ?, ?, ?)",
                  (customer_id, units, rate, total, date))
        conn.commit()
        conn.close()
        return redirect('/')
    c.execute("SELECT id, name FROM customers")
    customers = c.fetchall()
    conn.close()
    return render_template('generate_bill.html', customers=customers)

@app.route('/view_bills')
def view_bills():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        SELECT bills.id, customers.name, bills.units, bills.total, bills.date 
        FROM bills 
        JOIN customers ON bills.customer_id = customers.id
    ''')
    bills = c.fetchall()
    conn.close()
    return render_template('view_bills.html', bills=bills)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
