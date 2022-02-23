from random import choice
import os
from flask import Flask,render_template,request,url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

path = os.path.join(os.getcwd(),'dictionary.db')


app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{path}'
db = SQLAlchemy(app)


class Dictionary(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    english_word = db.Column(db.String, nullable=False)
    russia_word = db.Column(db.String, nullable=False)


@app.route("/")
def index():

    return render_template("index.html")

@app.route("/lst_word",methods=["GET","POST"])
def lst_word():

    if request.method == "POST":

        if request.form['btn'] == 'Добавить новое слово':


            new_word = Dictionary(

                english_word=request.form["english_word"],
                russia_word=request.form["russia_word"],
            )

            db.session.add(new_word)
            db.session.flush()
            db.session.commit()

            return render_template("lst_word.html", items=Dictionary.query.all())

        if request.form['btn'] == 'Удалить':

            *d,c = request.form

            for x in d:

                Dictionary.query.filter(Dictionary.id == "".join(x)).delete()

                db.session.commit()

            return render_template("lst_word.html", items=Dictionary.query.all())



    return render_template("lst_word.html",items=Dictionary.query.all())


menu_english = [{"name":"Полный ввод слова","url":"input_english"},{"name":"Найти слово из списка","url":"lst_english"}]

@app.route("/translate_english")
def translate_from_english():

    return render_template("translate_english.html",menu_english=menu_english)

@app.route("/input_english",methods=["GET","POST"])
def input_english():

    lst_id_word = []

    items = Dictionary.query.all()

    for x in items:

        lst_id_word.append(x.id)

    r = choice(lst_id_word)

    q = Dictionary.query.filter_by(id=r).first()

    r_q_english_word = q.english_word


    if request.method == "POST":

        print(request.form["word"])

        print(q.russia_word)


    return render_template("input_english.html",menu_english=menu_english,r_q_english_word=r_q_english_word)


@app.route("/lst_english")
def lst_english():
    return "asdf"


menu_russia = [{"name":"Полный ввод слова","url":"input_russia"},{"name":"Найти слово из списка","url":"lst_russia"}]

@app.route("/translate_russia")
def translate_from_russia():

    return render_template("translate_russia.html",menu=menu_russia)

if __name__ == "__main__":
    app.run(debug=True)