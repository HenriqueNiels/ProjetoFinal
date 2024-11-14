from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models import User, Post, PostComentarios, Followers, Comunidade, Follow_comunidade, Like
from app import db
from flask_login import current_user
import os

class CadastroForm(FlaskForm):
    usuario = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email:', validators=[Email(), DataRequired()])
    senha1 = PasswordField(label='Senha:', validators=[Length(min=6), DataRequired()])
    senha2 = PasswordField(label='Confirmar Senha:', validators=[EqualTo('senha1'), DataRequired()])
    submit = SubmitField(label='Cadastrar')

    def validade_username(self, check_user):
        user = User.query.filter_by(usuario=check_user.data).first() 
        if user:
            raise ValidationError("Esse nome de usuario ja existe!")
    
    def validade_email(self, check_email):
        email = email.query.filter_by(email=check_email.data).first() 
        if email:
            raise ValidationError("Esse email ja está sendo usado!")
        
class LoginForm (FlaskForm):
    usuario = StringField(label="Usuário:", validators=[DataRequired()])
    senha = PasswordField(label="Senha:", validators=[DataRequired()])
    submit = SubmitField(label='Login')

class PostForm(FlaskForm):
     mensagem = StringField('Faça um Post', validators=[DataRequired()])
     img = FileField()
     btnSubmit = SubmitField()
     

     def save(self, user_id):
        if self.img.data:
            
            post = Post(
                mensagem=self.mensagem.data,
                img=self.img.data.read(),
                user_id=user_id
            )
        db.session.add(post)
        db.session.commit()

class PostComunidadeForm(FlaskForm):
     mensagem = StringField('Faça um Post', validators=[DataRequired()])
     btnSubmit = SubmitField('Enviar')

     def save(self, user_id, comunidade_id):
        post = Post (
             mensagem=self.mensagem.data,
             user_id=user_id,
             comunidade_id = comunidade_id
        )
        db.session.add(post)
        db.session.commit()

class PostComentarioForm(FlaskForm):
     comentario = StringField('Comentario', validators=[DataRequired()])
     btnSubmit = SubmitField('Enviar')

     def save(self, user_id, post_id):
        comentario = PostComentarios (
             comentario=self.comentario.data,
             user_id = user_id,
             post_id = post_id
        )

        db.session.add(comentario)
        db.session.commit()

class FollowForm(FlaskForm):
     btnSubmit = SubmitField('Follow')
     def save(self,usuario, user):
        follow = Followers (
             follower_id=usuario,
             follows_id=user
        )
        db.session.add(follow)
        db.session.commit()

class UnfollowForm(FlaskForm):
     def unfollow(self):
          unfollow = db.session.query(Followers).filter(Followers.follower_id==current_user.id,Followers.follows_id==user.id).first()
          db.session.delete(unfollow)
          db.session.commit()

class ComunidadeForm(FlaskForm):
     nome = StringField('Nome da Comunidade', validators=[DataRequired()])
     capa = FileField()
     banner = FileField()
     btnSubmit = SubmitField('Criar')
     

     def save(self, criador_id):
        post = Comunidade (
             nome=self.nome.data,
             capa=self.capa.data.read(),
             banner=self.capa.data.read(),
             criador_id=criador_id
             
        )
        db.session.add(post)
        db.session.commit()

class FollowComunidadeForm(FlaskForm):
     btnSubmit = SubmitField('Follow')
     def save(self,usuario, comunidade):
        follow = Follow_comunidade (
             follower_id=usuario,
             follows_id=comunidade
        )
        db.session.add(follow)
        db.session.commit()

class LikeForm(FlaskForm):
     btnSubmit = SubmitField('Laike')
     def save(self,usuario, post):
        like = Like (
             user_id=usuario,
             post_id=post
        )
        db.session.add(like)
        db.session.commit()

class Changepfp(FlaskForm):
     novapfp = FileField()

     btnSubmit = SubmitField('Enviar')

     
     


        
    