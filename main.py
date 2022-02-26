from random import choice,shuffle
import os
from flask import Flask,render_template,request,url_for,flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

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

    q_english_word = q.english_word

    q_russia_word = q.russia_word

    if request.method == "POST":

        lst = []

        for x in request.form.keys():

            lst.append(x)

        if request.form["word"].strip(" ") == lst[-1]:

            flash("Перевод верный", category='success')

        else:

            flash("Перевод не верный", category='error')

    return render_template("input_english.html",menu_english=menu_english,q_english_word=q_english_word,q_russia_word=q_russia_word)


@app.route("/lst_english",methods=["GET","POST"])
def lst_english():

    lst_id_word = []

    items = Dictionary.query.all()

    for x in items:

        lst_id_word.append(x.id)

    r = choice(lst_id_word)

    q = Dictionary.query.filter_by(id=r).first()

    q_english_word = q.english_word

    q_russia_word = q.russia_word

    rus_word = q.russia_word

    q_russia_word = [q_russia_word]

    for x in range(6):

        q = Dictionary.query.filter_by(id=choice(lst_id_word)).first()

        rus = q.russia_word

        if rus not in q_russia_word:

            q_russia_word.append(rus)

    shuffle(q_russia_word)

    if request.method == "POST":

        select = request.form.get('comp_select')

        lst = []

        for x in request.form.keys():

            lst.append(x)

        if select == lst[-1]:

            flash("Перевод верный", category='success')

        else:

            flash("Перевод не верный", category='error')



    return render_template("lst_input_english.html",menu_english=menu_english,q_english_word=q_english_word,q_russia_word=q_russia_word,rus_word=rus_word)


menu_russia = [{"name":"Полный ввод слова","url":"input_russia"},{"name":"Найти слово из списка","url":"lst_russia"}]

@app.route("/translate_russia")
def translate_from_russia():

    return render_template("translate_russia.html",menu_russia=menu_russia)


@app.route("/input_russia",methods=["GET","POST"])
def input_russia():

    lst_id_word = []

    items = Dictionary.query.all()

    for x in items:

        lst_id_word.append(x.id)

    r = choice(lst_id_word)

    q = Dictionary.query.filter_by(id=r).first()

    q_english_word = q.english_word

    q_russia_word = q.russia_word

    if request.method == "POST":

        lst = []

        for x in request.form.keys():

            lst.append(x)

        if request.form["word"].strip(" ") == lst[-1]:

            flash("Перевод верный", category='success')

        else:

            flash("Перевод не верный", category='error')

    return render_template("input_russia.html",menu_russia=menu_russia,q_english_word=q_english_word,q_russia_word=q_russia_word)





@app.route("/lst_russia",methods=["GET","POST"])
def lst_russia():

    lst_id_word = []

    items = Dictionary.query.all()

    for x in items:

        lst_id_word.append(x.id)

    r = choice(lst_id_word)

    q = Dictionary.query.filter_by(id=r).first()

    q_english_word = q.english_word

    q_russia_word = q.russia_word

    eng_word = q.english_word

    q_english_word = [q_english_word]

    for x in range(6):

        q = Dictionary.query.filter_by(id=choice(lst_id_word)).first()

        eng = q.english_word

        if eng not in q_russia_word:

            q_english_word.append(eng)

    shuffle(q_english_word)

    if request.method == "POST":

        select = request.form.get('comp_select')

        lst = []

        for x in request.form.keys():

            lst.append(x)

        if select == lst[-1]:

            flash("Перевод верный", category='success')

        else:

            flash("Перевод не верный", category='error')

    return render_template("lst_input_russia.html",menu_russia=menu_russia,q_english_word=q_english_word,q_russia_word=q_russia_word,eng_word=eng_word)

if __name__ == "__main__":
    app.run(debug=True)