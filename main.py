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

    return "123"

@app.route("/lst_word",methods=["GET","POST"])
def lst_word():
    if request.method == "POST":

        new_word = Dictionary(

            english_word=request.form["english_word"],
            russia_word=request.form["russia_word"],
        )

        db.session.add(new_word)
        db.session.flush()
        db.session.commit()

        return render_template("lst_word.html", items=Dictionary.query.all())

    # if request.method == "POST":
    #
    #     print("Del")
    #
    #     return render_template("lst_word.html", items=Dictionary.query.all())


    return render_template("lst_word.html",items=Dictionary.query.all())




if __name__ == "__main__":
    app.run(debug=True)