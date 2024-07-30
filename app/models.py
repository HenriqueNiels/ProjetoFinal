from app import db, login_manager
from app import bcrypt
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

followers = db.Table('followers',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('follows_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    usuario = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    senha = db.Column(db.String(length=60), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)
    follows = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.user_id == id),
        secondaryjoin=(followers.c.follows_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
      
    def is_following(self, user):
        l = self.follows.filter(followers.c.follows_id == user.id).count()
        return l > 0


    def follow(self, user):
        if self.id != user.id:
            if not self.is_following(user):
                self.follows.append(user)


    def unfollow(self, user):
        if self.is_following(user):
            self.follows.remove(user)


    def get_followers(self, user):
        return User.query.filter(User.follows.any(id=user.id)).all()


    def get_followers_count(self, user):
        return len(self.get_followers(user))


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

    
class PostComentarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime,default=datetime.now())
    comentario = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)



