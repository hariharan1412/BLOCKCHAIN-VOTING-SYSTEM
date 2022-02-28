# from distutils.log import debug
# from email.mime import base
# from enum import unique
# import re
from flask import Flask , render_template , url_for , redirect , abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin , login_user , LoginManager , login_required , logout_user , current_user
from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField 
from wtforms.validators import InputRequired , Length , ValidationError
from flask_bcrypt import Bcrypt
from credentials import ADMIN , PASSWORD

add = [
    '0x18Ac764ACf55E9b76E4B17fe02ecDFB1e71Ca442',
    '0xAE9132159fF5b4466eE7d17C74d026543c09395e',
    '0xB70F65CAEa9A3C297e7cc690590d39B422e3Cfde',
    '0xDd5D26942aAdc076A41Ccc1Bc982F88a797540bf',
    '0x2Da9901AD8E2FF864ACE399B78F5b2b34CAd7326',
    '0x90A337c5A610290D3037F2e178bD19c55bB457a8',
    '0xf188bE3F05EE0e5AA84993df41ABC795c01303DA',
    '0x7ee4Dc6d89c09DB98Ea4445B5A4cF1268140E04D',
    '0x6467b03eC056b7fA00a5c0B01190Af77491c408a',
    '0x712AaEC0BC7a6FE7D5cD77F8652Af845D298ad16'
]


key = [
    '3659e6e278282cd0a19c6847fba3ded24186e7bf13ccd6cf59f8b10f511c5ab6',
    '240730cd0294a402ba85849a5b133b5883f015fa4964478942a3afac83dc3270',
    'ef0a908340f5447e706fd9761f774f3db9cb7675f20d54b331d1f277dbfdc62d',
    '140ca792ea22492f58cd7fd73848fdb063c26d55d685521b6f448ee4cdb1f244',
    '140ca792ea22492f58cd7fd73848fdb063c26d55d685521b6f448ee4cdb1f244',
    'beda2d6ea8e8f8ef4dac015db5eab9eea7e0d95b7d06fc489de33a955d7d0297',
    'a017a3761872fced21bfacf09117f0c13f3c7fff05ec5e30dc7cb96f5ebee983',
    'cd9678400401f21521d8d6a78b503f29393cabffed658fdbc71737d64fd252fb',
    '02b767db3de1ba7c6a8847cf8df7d9aaac338acb89af5ded8f26ca9fde1b11c3',
    'ca4922d59860e9e2a916e666a8b8560a20af84e58e037bb1cc907a9488f4239a'
]

voted = []


app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ===========================================================Login System====================================================================== 

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'THIS IS A SECRET KEY'

class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(20) , nullable=False , unique=True)
    password = db.Column(db.String(80) , nullable=False)
    address  = db.Column(db.String(80) , nullable=False , unique=True)
    key      = db.Column(db.String(80) , nullable=False , unique=True)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired() , Length(min=1 , max=20)], render_kw={"placeholder" : "Username"})
    password = PasswordField(validators=[InputRequired() , Length(min=1 , max=20)], render_kw={"placeholder" : "Password"})
    address = StringField(validators=[InputRequired() , Length(min=4 , max=80)], render_kw={"placeholder" : "address"})
    key = StringField(validators=[InputRequired() , Length(min=4 , max=80)], render_kw={"placeholder" : "key"})

    submit = SubmitField("Register")

    def validate_username(self , username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError(" USERNAME ALREADY EXISTS , PLZ CHOOSE OTHER")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired() , Length(min=1 , max=20)], render_kw={"placeholder" : "Username"})
    password = PasswordField(validators=[InputRequired() , Length(min=1 , max=20)], render_kw={"placeholder" : "Password"})

    submit = SubmitField("Log In")

# ===========================================================Login System====================================================================== 



@app.route('/login' , methods=['GET' , 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        global user
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password , form.password.data):
                login_user(user)
                return redirect(url_for('home'))
    user = None
    return render_template('login.html' , form=form)

@app.route('/register' , methods=['GET' , 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data , password=hashed_password , address=form.address.data , key=form.key.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html' , form=form)

@app.route('/' , methods=['GET' , 'POST'])
@login_required
def home():
    print(f" [ USERNAME ] {user.username} [ PASSWORD ] {user.password} [ ADDRESS ] {user.address} [ KEY ] {user.key} ")
    return render_template('home.html')

@app.route('/logout' , methods=['GET' , 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/admin/' , methods=['GET' , 'POST'])
# @login_required
def admin():
    form = LoginForm()
    if form.validate_on_submit():
        global user
        user = User.query.filter_by(username=form.username.data).first()
        try:
            if user.username == ADMIN:
                if bcrypt.check_password_hash(user.password , PASSWORD):
                    login_user(user)
                    return render_template('admin.html')
        except:
            abort(403)

    return render_template('adminLogin.html' , form=form)

@app.route('/vote' , methods=['GET' , 'POST'])
@login_required
def vote():
    return render_template('vote.html')


@app.route('/voted' , methods=['GET' , 'POST'])
def voted():
    return render_template('voted.html')



if __name__ == "__main__":
    app.run(host="0.0.0.0" ,port=5000, debug = True)

    