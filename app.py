from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
Bootstrap(app)

# MySQL configurations
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['SECRET_KEY'] = os.urandom(24)

# Enable MySQL Cursor use DictCursor 'Values' instead of 'Tuples'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Fetch form data
            form = request.form
            name = form['name']
            password = form['password']
            age = form['age']
            cur = mysql.connection.cursor()
            password = generate_password_hash(password)
            cur.execute("INSERT INTO users(name,password ,age) VALUES(%s, %s, %s)", (name, password, age))
            mysql.connection.commit()
            cur.close()
            flash('User added successfully!', 'success')
        except Exception as e:
            flash('Failed to add user!', 'danger')


    return render_template('index.html')



@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users")
    if result > 0:
        users = cur.fetchall()
        return render_template('users.html', users=users)


@app.errorhandler(404)
def page_not_found(e):
    return "This page was not found", 404


if __name__ == '__main__':
    app.run(debug=True)
