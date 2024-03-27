
from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'admin'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'password',
        servidor = 'localhost',
        database = 'cadastro'
    )

db = SQLAlchemy(app) ## instanciação com aplicacao flask

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
    
## conexao do sql_alchemy com banco de dados através de classes



class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(70), nullable=False)
    disponibilidade = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float(10,2), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name



@app.route('/')
def index():
        
        if 'usuario_logado' not in session or session['usuario_logado'] == None: 
            return redirect('/login')
        
        return render_template('index.html' , titulo = 'Cadastro de Produto')

@app.route('/process')
def process():
    lista = Produtos.query.order_by(Produtos.valor)
    return render_template('lista.html', titulo = 'Lista de produtos', produtos= lista )

@app.route('/recadastrando' , methods =['POST' , ] )
def recad():
    return redirect('/')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/autenticar', methods = ['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname = request.form['usuario']).first()
    if usuario:

        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = request.form['usuario']
            flash( session['usuario_logado']  + '  logado' ) #uma mensagem rapida e unica
            return redirect('/')
    else:
        flash('Usuario não logado')
        return redirect('/login')



@app.route('/criar', methods = ['POST', ])
def criar():
    nome = request.form['nome']
    descricao = request.form['descricao']
    disponibilidade = request.form['disponibilidade']
    valor = request.form['valor']

    ## conferimos se o nome já nao é existente
    produto = Produtos.query.filter_by(nome=nome).first()
    if produto:
        flash('Jogo já existente')
        return redirect('/')
    
    new_Prod = Produtos(nome=nome, descricao=descricao,  disponibilidade=disponibilidade , valor=valor)
    db.session.add(new_Prod)
    db.session.commit()
    return redirect('/process')
    

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado')
    return redirect('/')

app.run(debug = True)
