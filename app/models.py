from app import db, login_manager
from app import bcrypt
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, ForeignKeyConstraint


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class Followers (db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    follower_id = db.Column( db.Integer, db.ForeignKey('user.id'), nullable=False)
    follows_id = db.Column( db.Integer, db.ForeignKey('user.id'), nullable=False)

    
    __table_args__ = (
        UniqueConstraint(follower_id, follows_id),
    )



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    usuario = db.Column(db.String(length=30), nullable=False, unique=True)
    profile_pic = db.Column(db.LargeBinary, nullable=True)
    banner = db.Column(db.LargeBinary, nullable=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    senha = db.Column(db.String(length=60), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)
    comunidades = db.relationship('Comunidade', backref='user', lazy=True)

    
    
    def get_followed_posts(self):
        fw_users = [user.uid for user in self.follows.all()]
        fw_users.append(self.uid)       # to include my own posts
        # print(fw_users)
        fw_posts = Post.query.order_by(Post.date_posted.desc()).filter(Post.user_id.in_(fw_users))
        return fw_posts 
      

    @property
    def senhacrip(self):
        return self.senhacrip
    
    @senhacrip.setter
    def senhacrip(self, senha_texto):
        self.senha = bcrypt.generate_password_hash(senha_texto).decode('utf-8')

    def converte_senha(self,senha_texto_claro):
        return bcrypt.check_password_hash(self.senha, senha_texto_claro)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now())
    mensagem = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    comentarios = db.relationship('PostComentarios', backref='post', lazy=True)
    comunidade_id = db.Column(db.Integer, db.ForeignKey('comunidade.id'), nullable=True)
    img = db.Column(db.LargeBinary, nullable=True)
    mimetype = db.Column(db.Text, nullable=True)

    def msg_resumo(self):
        return f"{self.mensagem[:250]}"
    
    def like_count(self):
        return int(db.session.query(Like).filter(Like.post_id==self.id).count())
    
    def isliked(self,user_id):
        return bool(db.session.query(Like).filter(Like.user_id==user_id,Like.post_id==self.id).first())
    
class PostComentarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime,default=datetime.now())
    comentario = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)

class Comunidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now())
    nome = db.Column(db.String, nullable=True)
    capa = db.Column(db.LargeBinary, nullable=True)
    banner = db.Column(db.LargeBinary, nullable=True)
    criador_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    posts = db.relationship('Post', backref='comunidade', lazy=True)

class Follow_comunidade (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    follower_id = db.Column( db.Integer, db.ForeignKey('user.id'), nullable=False)
    follows_id = db.Column( db.Integer, db.ForeignKey('comunidade.id'), nullable=False)
    __table_args__ = (
        UniqueConstraint(follower_id, follows_id),
    )

class Like (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column( db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column( db.Integer, db.ForeignKey('post.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint(user_id, post_id),
    )
    




