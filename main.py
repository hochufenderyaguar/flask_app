from threading import Thread
from ebaysdk.finding import Connection as finding
import schedule
from flask import Flask, render_template, redirect, request
from werkzeug.exceptions import abort
from data import db_session
from data.users import User
from data.products import Product
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.user import RegisterForm, LoginForm
from forms.products import ProductsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


# регистрация
@app.route('/join', methods=['GET', 'POST'])
def join():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


# вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/index")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# страничка для пользователей
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    products = db_sess.query(Product).filter(Product.user_id == current_user.id)
    return render_template('index.html', products=products)


@app.route('/')
def base():
    return render_template('base.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        product = Product()
        product.product = form.product.data
        product.price = form.price.data
        current_user.products.append(product)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/index')
    return render_template('add_product.html', title='Добавление товара',
                           form=form)


@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    form = ProductsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        product = db_sess.query(Product).filter(Product.id == id,
                                                Product.user == current_user
                                                ).first()
        if product:
            form.product.data = product.product
            form.price.data = product.price
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        product = db_sess.query(Product).filter(Product.id == id,
                                                Product.user == current_user
                                                ).first()
        if product:
            product.product = form.product.data
            product.price = form.price.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('edit_product.html',
                           title='Редактирование цены товара',
                           form=form
                           )


@app.route('/delete_product/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.id == id,
                                            Product.user == current_user
                                            ).first()
    if product:
        db_sess.delete(product)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def find_product_price(keywords):
    api = finding(appid='', config_file=None)
    api_request = {'keywords': keywords,
                   'outputSelector': 'UnitPriceInfo'
                   }
    response = api.execute('findItemsByKeywords', api_request)
    items = response.dict()["searchResult"]["item"]
    return items


def check_price():
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        for product in user.products:
            user_price = int(product.price)
            items = find_product_price(product.product)
            for item in items:
                if int(item["sellingStatus"]["currentPrice"]["value"]) <= user_price:
                    print(item["viewItemURL"])
                    break


def cache():
    schedule.every().day.at("10:00").do(check_price)

    while True:
        schedule.run_pending()


thread = Thread(target=cache)
thread.start()

if __name__ == '__main__':
    db_session.global_init("db/monitor.db")
    app.run(port=8080, host='127.0.0.1')
