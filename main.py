from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash 

from model import db, User
from form import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = b'0fb6a8d3d92711c2925c87e6234ccbdae352e0015a18780f0c617fb5fe95ee2a'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = generate_password_hash(form.password.data)  
        existing_user = User.query.filter((User.firstname == firstname) & (User.lastname == lastname) & (User.email == email)).first() 
        if existing_user:
            error_msg = 'You have already been registered.'
            form.firstname.errors.append(error_msg)
            return render_template('registration.html', form=form)
        new_user = User(firstname=firstname, lastname=lastname, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        success_msg = 'Registration successful!'
        return success_msg
    
    return render_template('registration.html', form=form)