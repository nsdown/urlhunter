from flask import Blueprint, render_template, redirect, url_for, flash, request
from urlhunter.forms import LoginForm, RegisterForm
from urlhunter.models import User
from urlhunter.extensions import db
from flask_login import current_user, login_user, logout_user


bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('该用户不存在！', 'danger')
        elif not user.check_password(password=form.password.data):
            flash('密码错误！', 'danger')
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route('/logout')
def log_out():
    logout_user()
    return redirect(url_for('main.index'))
