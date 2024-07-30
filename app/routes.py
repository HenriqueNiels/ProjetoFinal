from flask import render_template, redirect, url_for, flash, request, jsonify
from app import app
from sqlalchemy import Select
from app.models import User, Post, PostComentarios
from app.form import CadastroForm, LoginForm, PostForm, PostComentarioForm
from app import db
from flask_login import login_user, current_user, login_required, logout_user

@app.route('/', methods=['GET','POST'])
def homepage():
    return render_template('home.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        usuario = User(
            usuario = form.usuario.data,
            email = form.email.data,
            senhacrip = form.senha1.data
        )   
        
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('homepage'))
    if form.errors != {}:
        for err in form.errors.value():
            flash(f"erro ao cadastras usuario {err}")
    return render_template('cadastro.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario_logado = User.query.filter_by(usuario=form.usuario.data).first()

        if usuario_logado and usuario_logado.converte_senha(senha_texto_claro=form.senha.data):
            login_user(usuario_logado)

            flash(f'Sucesso! Seu login é: {usuario_logado.usuario}', category='success')

            return redirect(url_for('homepage'))
        else:
            flash('Usuário ou senha estão incorretos! Tente novamente.', category='danger')

    return render_template('login.html', form=form)

@app.route('/foryou',methods=['GET', 'POST'])
@login_required
def ForYou():
    form = PostForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('homepage'))
    return render_template('foryou.html',  form=form)

@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def PostComentarios(id):
    post = Post.query.get(id)
    form = PostComentarioForm()
    if form.validate_on_submit():
        form.save(current_user.id, id)
        return redirect(url_for('PostComentarios', id=id))
    return render_template('post.html', post=post, form=form)

@app.route('/logout', methods=['GET', 'POST'])
def page_logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/user/<usuario>')
@login_required
def user(usuario):
    user = db.first_or_404(Select(User).where(User.usuario == usuario))
    posts  = user.posts
    return render_template ('user.html', user=user, posts=posts)

@app.route("/follow", methods=['GET', 'POST'])
@login_required
def follow_user():
    if request.method == 'GET':
        usuario = request.args.get('usuario')
    else:
        usuario = request.form['usuario']
    print(usuario)
    user = User.query.filter_by(usuario=usuario).first()
    current_user.follow(user)
    db.session.commit()

    return jsonify(result=usuario + " followed")

@app.route("/unfollow", methods=['POST'])
@login_required
def unfollow_user():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    current_user.unfollow(user)
    db.session.commit()
    print(username)

    return jsonify(result=username + " unfollowed")
