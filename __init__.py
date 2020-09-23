from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'userdb.c1dtyhre7zvh.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'database123'
app.config['MYSQL_DB'] = 'userdb'

mysql = MySQL(app)





@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM users")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', users=data)



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Added Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, phone,address) VALUES (%s, %s, %s,%s)", (name, email, phone, address))
        mysql.connection.commit()
        return redirect(url_for('Index'))




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Data Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE users
               SET name=%s, email=%s, phone=%s, address=%s
               WHERE id=%s
            """, (name, email, phone, address, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))









if __name__ == "__main__":
    app.run(debug=True)
