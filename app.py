from flask import Flask, render_template, request
from flask_mail import Mail, Message
import sqlite3


app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'

mail = Mail(app)

def send_notification(name, email, phone):
    msg = Message('New User Data', sender='your-email@gmail.com', recipients=['your-email@gmail.com'])
    msg.body = f'Name: {name}\nEmail: {email}\nPhone: {phone}'
    mail.send(msg)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (name TEXT, email TEXT, phone TEXT)''')
    c.execute('INSERT INTO users (name, email, phone) VALUES (?, ?, ?)', (name, email, phone))
    conn.commit()
    conn.close()

    send_notification(name, email, phone)

    return 'The data has been successfully saved to the database and notification has been sent to your email!'

if __name__ == '__main__':
    app.run(debug=True)
