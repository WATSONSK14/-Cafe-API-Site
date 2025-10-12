from flask import render_template, redirect, request, flash, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from form import RegisterForm, LoginForm, CafeForm
from model import db, User, create_and_store_api_key_for_user, decrypt_key, Cafe

normal_bp = Blueprint('normal', __name__)

@normal_bp.route('/')
def home():
    result = db.session.execute(db.select(Cafe))
    cafes = result.scalars().all()
    return render_template('home.html', cafes=cafes)

@normal_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        fields = ["can_take_calls", "coffee_price", "country", "has_sockets", "has_toilet",
                  "has_wifi", "img_url", "location", "map_url", "name"]
        map_url = form.data.get('map_url')
        map_check = db.session.execute(db.select(Cafe).filter_by(map_url=map_url)).scalar()
        if map_check:
            flash('Bu Kafe Zaten Mevcut',"warning")
            return redirect(url_for('normal.add_cafe'))
        try:
            new_cafe_data = {}
            for field in fields:
                new_cafe_data[field] = form.data.get(field)
            new_cafe_data['user_id'] = current_user.id
            new_cafe = Cafe(**new_cafe_data)
            db.session.add(new_cafe)
            db.session.commit()
            flash('Kafe Başarıyla Eklendi',"success")
            return redirect(url_for('normal.home'))
        except Exception as e:
            return f"error: {e}"

    return render_template('add_cafe.html', form=form)


@normal_bp.route('/update/<int:cafe_id>', methods=['GET', 'POST'])
@login_required
def update_cafe(cafe_id):
    cafe = db.session.get(Cafe, cafe_id)
    fields = ["can_take_calls", "coffee_price", "country", "has_sockets", "has_toilet",
              "has_wifi", "img_url", "location", "map_url", "name"]

    if not cafe:
        flash('Kafe Bulunamadı','error')
        return redirect(url_for('normal.user_cafes'))

    if cafe.user_id != current_user.id:
        flash('Bu kafeyi düzenleme yetkiniz yok!', 'error')
        return redirect(url_for('normal.user_cafes'))
    
    form = CafeForm()
    
    if request.method == 'GET':
        for field in fields:
            getattr(form, field).data = getattr(cafe, field)
    
    if form.validate_on_submit():
        try:
            for field in fields:
                setattr(cafe, field, form.data.get(field))
            
            db.session.commit()
            flash('Kafe Başarıyla Güncellendi','success')
            return redirect(url_for('normal.user_cafes'))
        except Exception as e:
            db.session.rollback()
            flash('Kafe güncellenirken hata oluştu','error')
            print(f"Update error: {e}")
    
    return render_template('update_cafe.html', cafe=cafe, form=form)





@normal_bp.route('/delete/<int:cafe_id>', methods=['POST'])
@login_required
def delete_cafe(cafe_id):
    cafe = db.session.execute(db.select(Cafe).filter_by(id=cafe_id)).scalar()
    if not cafe:
        flash('Kafe Bulunamadı','error')
        return redirect(url_for('normal.user_cafes'))
    
    if cafe.user_id != current_user.id:
        flash('Bu kafeyi silme yetkiniz yok!','error')
        return redirect(url_for('normal.user_cafes'))
    
    try:
        db.session.delete(cafe)
        db.session.commit()
        flash('Kafe Başarıyla Silindi','success')
    except Exception as e:
        db.session.rollback()
        flash('Kafe silinirken hata oluştu','error')
        print(f"Delete error: {e}")
    
    return redirect(url_for('normal.user_cafes'))

@normal_bp.route('/user/panel', methods=['GET', 'POST'])
@login_required
def user_panel():
    api_key = decrypt_key(current_user.api_key_enc)
    return render_template('user_panel.html', api_key=api_key)


@normal_bp.route('/cafe_detail/<int:cafe_id>', methods=['GET', 'POST'])
def cafe_detail(cafe_id):
    cafe = db.session.execute(db.select(Cafe).filter_by(id=cafe_id)).scalar()
    if not cafe:
        flash("Kafe bulunamadı!", "error")
        return redirect(url_for('normal.home'))
    return render_template('cafe_detail.html', cafe=cafe)

@normal_bp.route('/user_cafes', methods=['GET', 'POST'])
@login_required
def user_cafes():
    cafes = current_user.cafes
    return render_template('user_cafes.html', cafes=cafes)

@normal_bp.route('/locations')
def all_locations():
    result = db.session.execute(db.select(Cafe))
    cafes = result.scalars().all()
    
    # Tüm konumları al ve say
    locations = {}
    for cafe in cafes:
        location = cafe.location
        if location in locations:
            locations[location] += 1
        else:
            locations[location] = 1
    
    # Konumları kafe sayısına göre sırala
    sorted_locations = sorted(locations.items(), key=lambda x: x[1], reverse=True)
    
    return render_template('all_locations.html', locations=sorted_locations)


@normal_bp.route('/register',methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        email_check = db.session.execute(db.Select(User).filter_by(email=email)).scalar()
        username_check = db.session.execute(db.Select(User).filter_by(username=username)).scalar()

        if email_check:
            flash("Email already registered", "warning")
            return redirect(url_for('normal.register'))
        if username_check:
            flash("Username already registered", "warning")
            return redirect(url_for('normal.register'))

        password = form.password.data
        password_hash = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=password_hash,
        )
        db.session.add(new_user)
        db.session.commit()
        create_and_store_api_key_for_user(new_user)

        flash("Account created successfully!", "success")
        return redirect(url_for('normal.register'))
    return render_template('register.html', form=form)


@normal_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for('normal.home'))

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Not Found User", "warning")
            return redirect(url_for('normal.login'))
        if not check_password_hash(user.password, password):
            flash("Username or password is incorrect", "warning")
            return redirect(url_for('normal.login'))

        login_user(user)
        flash("Login Successful!", "success")
        return redirect(url_for('normal.home'))

    return render_template('login.html', form=form)

@normal_bp.route("/logout",methods= ["GET","POST"])
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Logout Successful!", "success")
    return redirect(url_for('normal.home'))



