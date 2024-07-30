from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models import User, Post, PostComentarios
from app import db
import os
from werkzeug.utils import secure_filename

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
     mensagem = StringField('Mensagem', validators=[DataRequired()])
     btnSubmit = SubmitField('Enviar')

     def save(self, user_id):
        post = Post (
             mensagem=self.mensagem.data,
             user_id=user_id
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

        
    