from flask import Flask, render_template, request,flash, redirect, url_for
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, validators

app = Flask(__name__)
app.secret_key = "aepojfpoaejf"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'burhankaratas'

mysql = MySQL(app)

class IletisimForm(Form):
    name = StringField(validators=[validators.DataRequired()])
    email = StringField(validators=[validators.DataRequired()])
    content = TextAreaField(validators=[validators.DataRequired()])

@app.route("/", methods=["GET", "POST"])
def index():
    form = IletisimForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        content = form.content.data

        cursor = mysql.connection.cursor()

        insert_query = "INSERT INTO message (name, email, content) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, email, content))

        mysql.connection.commit()

        cursor.close()

        flash("Mesajınız Başarıyla Gönderildi!", "success")
        return redirect(url_for("index"))

    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
