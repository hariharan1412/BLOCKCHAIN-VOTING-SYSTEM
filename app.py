
from brownie import Contract
from flask import Flask , render_template , url_for , redirect , abort , request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin , login_user , LoginManager , login_required , logout_user , current_user
from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField 
from wtforms.validators import InputRequired , Length , ValidationError
from flask_bcrypt import Bcrypt
from credentials import ADMIN , PASSWORD
from web3 import Web3
import json
import time

# =========================================================== WEB3 ====================================================================== 

network_url = "HTTP://127.0.0.1:7545"
web = Web3(Web3.HTTPProvider(network_url))


truffleFile = json.load(open('./build/contracts/Election.json'))

abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

global end
end = False



# =========================================================== WEB3 ====================================================================== 

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
                    return redirect(url_for('adminPortal'))
        except:
            abort(403)

    return render_template('adminLogin.html' , form=form)

@app.route('/adminPortal' , methods=['GET' , 'POST'])
# @login_required
def adminPortal():

    if  request.method == 'POST':
        if request.form['adBtn'] == 'START':
                    print("[ START ]")
                                        
                    def deploy(owner , signature):
                        election = web.eth.contract(abi=abi , bytecode=bytecode)
                        
                        transaction_body = {
                            'nonce':web.eth.get_transaction_count(owner),
                            'gas'   :1728712,
                            'gasPrice':web.toWei(8 , 'gwei')
                        }
                        
                        deployment = election.constructor().buildTransaction(transaction_body)
                        signed_transaction = web.eth.account.sign_transaction(deployment , signature)
                        result = web.eth.send_raw_transaction(signed_transaction.rawTransaction)
                        tx_receipt = web.eth.wait_for_transaction_receipt(result)

                        return tx_receipt.contractAddress

                    owner = user.address
                    signature = user.key

                    address = deploy(owner , signature)
                    global election
                    election = web.eth.contract(address=address , abi=abi)
                    print(address , election)

                    logout_user()
                    return redirect(url_for('login'))

        if request.form['adBtn'] == 'RESULT':
                    print("[ RESULT ]")

                    aang = election.caller().candidates(1)[2]
                    korra = election.caller().candidates(2)[2]
                    roku = election.caller().candidates(3)[2]
                    return render_template('result.html' , aang=aang , korra=korra , roku=roku)

        elif request.form['adBtn'] == 'END':
                    print("[ END ]")
                    
                    global end
                    end = True
                    # election.functions.end().call() 

                    return render_template('admin.html')
    
    elif request.method == 'GET':
        print("[ SOMETHING HAPPENING ]")
        return render_template('admin.html')


@app.route('/vote' , methods=['GET' , 'POST'])
@login_required
def vote():
    
    if end == False:
        def vote(owner , signature , to_vote): #Voting
            transaction_body = {
                'nonce':web.eth.get_transaction_count(owner),
                'gas'   :1728712,
                'gasPrice':web.toWei(8 , 'gwei')
            }

            v = election.functions.vote(to_vote).buildTransaction(transaction_body)
            signed_transaction = web.eth.account.sign_transaction(v , signature)
            try:
                result = web.eth.send_raw_transaction(signed_transaction.rawTransaction)
                print(result)
            except:
                print(" EXCEPT ")
                return render_template('admin.html')


        if  request.method == 'POST':
            if request.form['voteBtn'] == 'AANG':
                        print("[ candidate1 ]")

                        vote(user.address , user.key , 1)
                        return redirect(url_for('voted'))

            elif request.form['voteBtn'] == 'KORRA':
                        print("[ candidate2 ]")
                        vote(user.address , user.key , 2)
                        return redirect(url_for('voted'))

            elif request.form['voteBtn'] == 'ROKU':
                        print("[ candidate3 ]")
                        vote(user.address , user.key , 3)
                        return redirect(url_for('voted'))
        
        elif request.method == 'GET':
            return render_template('vote.html')

    return "<h1> ELECTION was ENDED </h1>"

@app.route('/voted' , methods=['GET' , 'POST'])
def voted():
    logout_user()
    return render_template('voted.html')



if __name__ == "__main__":
    app.run(host="0.0.0.0" ,port=5000, debug = True)

    