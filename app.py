from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string, random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


def func():
    s1 = string.ascii_lowercase
    s2 = string.ascii_uppercase
    s3 = string.digits
    s4 = string.punctuation
    concat = s1 + s2 + s3 + s4
    password = "".join(random.sample(concat, 15))
    return password


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(50), nullable=False)
    account = db.Column(db.String(50), nullable=False)
    strong_password = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, default=datetime.now().date())


def __repr__(self) -> str:
    return (
        f"{self.sno},{self.website},{self.account},{self.strong_password},{self.date}"
    )


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        website = request.form["website"]
        account = request.form["account"]
        password = func()
        todo = Todo(website=website, account=account, strong_password=password)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)


@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    if request.method == "POST":
        website = request.form["website"]
        account = request.form["account"]
        todo = Todo.query.filter_by(sno=sno).first()
        todo.website = website
        todo.account = account
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run()
