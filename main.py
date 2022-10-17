from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'

db = SQLAlchemy(app)

class Estudante(db.Model):

    ra = db.Column('ra', db.Integer, primary_key = True, autoincrement = True)
    nome = db.Column('Nome', db.String(150))
    idade = db.Column('Idade', db.Integer)
    curso = db.Column('Curso', db.String(150))

    def __init__(self, nome, idade, curso):
        self.nome = nome
        self.idade = idade
        self.curso = curso


@app.route('/')
def estudante():
    estudantes = Estudante.query.all()
    return render_template("estudante.html", estudantes=estudantes)

@app.route('/add', methods=["GET","POST"])
def add():

    if request.method == "POST":
        
        estudantes = Estudante(request.form["nome"], request.form["idade"], request.form["curso"])
        db.session.add(estudantes)
        db.session.commit()

        return redirect(url_for("estudante"))

    return render_template("add.html")

@app.route('/delete/<ra>')
def delete(ra):
    estudantes = Estudante.query.get(ra)
    db.session.delete(estudantes)
    db.session.commit()
    return redirect(url_for("estudante"))

@app.route('/edit/<ra>', methods= ["GET", "POST"])
def edit(ra):

    estudantes=Estudante.query.get(ra)

    if request.method=="POST":
        estudantes.nome = request.form['nome']
        estudantes.idade = request.form['idade']
        estudantes.curso = request.form['curso']
        db.session.commit()
        return redirect(url_for("estudante"))
    
    return render_template("edit.html", estudantes=estudantes)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)