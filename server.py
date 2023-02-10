from flask import Flask, render_template, request, redirect
import mysql.connector

cnx = mysql.connector.connect(
    user='root', password="toor", database='mca_2_db')
cursor = cnx.cursor()

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        cursor.execute("SELECT * FROM `students`")
        students = [dict(id=row[0], name=row[1], roll_no=row[2],
                         email=row[3]) for row in cursor]
        return render_template('index.html', students=students)
    elif request.method == 'POST':
        cursor.execute(
            "DELETE FROM `students` WHERE `id` = %s", (request.form['id'],))
        cnx.commit()
        return redirect('/')


@app.route('/create', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        cursor.execute(
            "INSERT INTO `students` (`name`, `roll_no`, `email`) VALUES (%s, %s, %s)",
            (request.form['name'], request.form['roll_no'], request.form['email']))
        cnx.commit()
        return redirect('/')


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        cursor.execute(F"SELECT * FROM `students` WHERE `id` = {id}")
        student = cursor.fetchone()
        student = {
            'id': student[0],
            'name': student[1],
            'roll_no': student[2],
            'email': student[3]
        }
        print(student)
        return render_template('update.html', student=student)
    elif request.method == 'POST':
        cursor.execute(
            "UPDATE `students` SET `name` = %s, `roll_no` = %s, `email` = %s WHERE `id` = %s",
            (request.form['name'], request.form['roll_no'], request.form['email'], id))
        cnx.commit()
        return redirect('/')
    return "OK"


if __name__ == '__main__':
    app.run(debug=True)
