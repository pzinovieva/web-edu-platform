from flask import (
    Blueprint, render_template, redirect
)
from app.moduls.forms import (
    LoginForm, RegistrationForm
)
from app.database.users import (
    User
)
from app.database.db_session import create_session
from flask_login import LoginManager, login_required, login_user, logout_user


login_manager = LoginManager()
bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/start')
        else:
            return render_template('signin.html', message="Неправильный логин или пароль", form=form)
    return render_template('signin.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    db_session = create_session()
    if form.validate_on_submit():
        if db_session.query(User).filter_by(login=form.login.data).count() < 1:
            if db_session.query(User).filter_by(email=form.email.data).count() < 1:
                user = User(
                    name=form.name.data,
                    type_user=form.type_user.data,
                    login=form.login.data,
                    email=form.email.data,
                )
                user.set_password(form.password.data)
                db_session.add(user)
                db_session.commit()
                return login()
            else:
                return render_template('signup.html', message="Пользователь с таким email уже существует", form=form)
        else:
            return render_template('signup.html', message="Пользователь с таким логином уже существует", form=form)
    return render_template("signup.html", form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
