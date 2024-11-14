from flask import render_template, redirect, url_for, flash, request, jsonify, Response
from app import app
from sqlalchemy import Select
from app.models import User, Post, PostComentarios, Followers, Comunidade,Follow_comunidade, Like
from app.form import CadastroForm, LoginForm, PostForm, PostComentarioForm, FollowForm, UnfollowForm, LikeForm, ComunidadeForm,PostComunidadeForm, FollowComunidadeForm
from app import db
from flask_login import login_user, current_user, login_required, logout_user
from sqlalchemy import select, update
from datetime import datetime
from operator import attrgetter


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
        return redirect(url_for('login'))
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

            return redirect(url_for('ForYou'))
        else:
            flash('Usuário ou senha estão incorretos! Tente novamente.', category='danger')

    return render_template('login.html', form=form)

@app.route('/foryou',methods=['GET', 'POST'])
@login_required
def ForYou():
    pesquisa = request.args.get('pesquisa', '')
    if pesquisa != '':
        if pesquisa:
            return redirect('user/'+pesquisa)
    currentuser = db.first_or_404(Select(User).where(User.usuario == current_user.usuario))
    follows = db.session.query(Followers).filter(Followers.follower_id==current_user.id).all()
    followsnum = len(follows)
    posts = []
    for i in range(followsnum):
        user = db.first_or_404(Select(User).where(User.id == follows[i].follows_id))
        postsuser = user.posts
        postsusercount = len(postsuser)
        for j in range(postsusercount):
            posts.append(postsuser[j])
    currentuserposts = currentuser.posts
    posts = posts + currentuserposts
    posts.sort(key=attrgetter('id'))
    posts.reverse()
    users = db.session.query(User).order_by(User.id).all()

    form = PostForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('ForYou'))
    return render_template('foryou.html',  form=form, posts = posts, users = users, pesquisa=pesquisa)

@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def PostComentarios(id):
    post = Post.query.get(id)
    isliked = bool(db.session.query(Like).filter(Like.user_id==current_user.id,Like.post_id==post.id).first())
    pesquisa = request.args.get('pesquisa', '')
    if pesquisa != '':
        if pesquisa:
            return redirect('user/'+pesquisa)
    form = PostComentarioForm()
    if form.validate_on_submit():
        form.save(current_user.id, id)
        return redirect(url_for('PostComentarios', id=id))
    users = db.session.query(User).order_by(User.id).all()
    return render_template('post.html', post=post, form=form, users=users, isliked=isliked)

@app.route('/post/<int:id>/like', methods=['GET', 'POST'])
@login_required
def LikePost(id):
    post = Post.query.get(id)
    user = db.session.query(User).filter(User.id==Post.user_id,Post.id==post.id).first()
    like = LikeForm()
    like.save(current_user.id,post.id)
    if request.referrer == "http://127.0.0.1:5000/foryou":
        return redirect('/foryou')
    elif request.referrer == 'http://127.0.0.1:5000/post/'+str(post.id):
        return redirect('/post/'+str(post.id))
    elif request.referrer == 'http://127.0.0.1:5000/comunidade/'+str(post.comunidade_id):
        return redirect('/comunidade/'+str(post.comunidade_id))
    elif request.referrer == 'http://127.0.0.1:5000/user/'+str(user.usuario):
        return redirect('/user/'+str(user.usuario))

@app.route('/post/<int:id>/dislike', methods=['GET', 'POST'])
@login_required
def DisLikePost(id):
    post = Post.query.get(id)
    user = db.session.query(User).filter(User.id==Post.user_id,Post.id==post.id).first()
    unfollow = db.session.query(Like).filter(Like.user_id==current_user.id,Like.post_id==post.id).first()
    db.session.delete(unfollow)
    db.session.commit()
    if request.referrer == "http://127.0.0.1:5000/foryou":
        return redirect('/foryou')
    elif request.referrer == 'http://127.0.0.1:5000/post/'+str(post.id):
        return redirect('/post/'+str(post.id))
    elif request.referrer == 'http://127.0.0.1:5000/comunidade/'+str(post.comunidade_id):
        return redirect('/comunidade/'+str(post.comunidade_id))
    elif request.referrer == 'http://127.0.0.1:5000/user/'+str(user.usuario):
        return redirect('/user/'+str(user.usuario))
    

@app.route('/logout', methods=['GET', 'POST'])
def page_logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/user/<usuario>', methods=['GET', 'POST'])
@login_required
def user(usuario):
    pesquisa = request.args.get('pesquisa', '')
    if pesquisa != '':
        if pesquisa:
            return redirect(pesquisa)
    user = db.first_or_404(Select(User).where(User.usuario == usuario))
    follows = bool(db.session.query(Followers).filter(Followers.follower_id==current_user.id,Followers.follows_id==user.id).first())
    flwcount = db.session.query(Followers).filter(Followers.follows_id==user.id).count()
    db.session.commit()
    follow = FollowForm()
    if follow.is_submitted():
        follow.save(current_user.id,user.id)
        return redirect('/user/'+user.usuario)
    posts  = user.posts
    entities = select(Post.data_criacao).order_by(Post.data_criacao)
    return render_template ('user.html', user=user, posts=posts, follow=follow, follows = follows, flwcount=flwcount)

@app.route('/user/<usuario>/unfollow', methods=['GET', 'POST'])
def unfollow(usuario):
          user = db.first_or_404(Select(User).where(User.usuario == usuario))
          unfollow = db.session.query(Followers).filter(Followers.follower_id==current_user.id,Followers.follows_id==user.id).first()
          db.session.delete(unfollow)
          db.session.commit()
          return redirect('/user/'+user.usuario)

@app.route('/comunidades',methods=['GET', 'POST'])
def comunidades():
    pesquisa = request.args.get('pesquisa', '')
    if pesquisa != '':
        if pesquisa:
            return redirect('user/'+pesquisa)
    comunidades = db.session.query(Comunidade).order_by(Comunidade.data_criacao).all()
    return render_template ('comunidades.html', comunidades=comunidades)

@app.route('/comunidades/criar',methods=['GET', 'POST'])
@login_required
def comunidades_criar():
    pesquisa = request.args.get('pesquisa', '')
    if pesquisa != '':
        if pesquisa:
            return redirect('user/'+pesquisa)
    form = ComunidadeForm()
    if form.validate_on_submit():
        form.save(int(current_user.id))
        return redirect(url_for('comunidades'))
    
    return render_template('comunidade_criar.html',  form=form)

@app.route('/comunidade/<int:id>', methods=['GET', 'POST'])
@login_required
def ComunidadeComentarios(id):
    pesquisa = request.args.get('pesquisa', '')
    if pesquisa != '':
        if pesquisa:
            return redirect('user/'+pesquisa)
    comunidade = db.first_or_404(Select(Comunidade).where(Comunidade.id == id))
    follows = bool(db.session.query(Follow_comunidade).filter(Follow_comunidade.follower_id==current_user.id,Follow_comunidade.follows_id==comunidade.id).first())
    if follows ==True:
        form = PostComunidadeForm()
        if form.validate_on_submit():
            form.save(current_user.id, id)
            return redirect(url_for('ComunidadeComentarios', id=id))
    else:
        form = FollowComunidadeForm()
        if form.is_submitted():
            form.save(current_user.id,comunidade.id)
            return redirect('/comunidade/'+str(comunidade.id))
    comunidade = Comunidade.query.get(id)
    
    users = db.session.query(User).order_by(User.id).all()
    data = datetime.now()
    return render_template('comunidade.html', comunidade=comunidade, form=form, users=users, data=data, follows=follows)

@app.route('/comunidade/<int:id>/unfollow', methods=['GET', 'POST'])
def unfollow_comunidade(id):
          comunidade = db.first_or_404(Select(Comunidade).where(Comunidade.id == id))
          unfollow = db.session.query(Follow_comunidade).filter(Follow_comunidade.follower_id==current_user.id,Follow_comunidade.follows_id==comunidade.id).first()
          db.session.delete(unfollow)
          db.session.commit()
          return redirect('/comunidade/'+str(comunidade.id))

@app.route('/imagem/<int:id>')
def post_img(id):
    post = Post.query.filter_by(id=id).first()
    img = post.img
    
    return Response(img, mimetype='PNG')

@app.route('/comunidade/banner/<int:id>')
def com_banner_img(id):
    comunidade = Comunidade.query.filter_by(id=id).first()
    img = comunidade.banner
    
    return Response(img, mimetype='PNG')

@app.route('/comunidade/capa/<int:id>')
def com_capa_img(id):
    comunidade = Comunidade.query.filter_by(id=id).first()
    img = comunidade.capa
    
    return Response(img, mimetype='PNG')

@app.route('/user/<int:id>/changepfp', methods=['GET', 'POST'])
@login_required
def ChangePFP(id):
    post = Post.query.get(id)
    user = db.session.query(User).filter(User.id==Post.user_id,Post.id==post.id).first()
    unfollow = db.session.query(Like).filter(Like.user_id==current_user.id,Like.post_id==post.id).first()
    db.session.delete(unfollow)
    db.session.commit()
    return redirect('/user/'+str(user.usuario))

    
