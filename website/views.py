from site import main
from tkinter import Menu
from unicodedata import name
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import current_user
from . import db, qwerty
from .models import Locomotive, Nov
from fileinput import filename
from flask import Flask, url_for, request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
from .models import Locomotive
Nov
import os
import shutil
from urllib.parse import urljoin
from werkzeug.security import generate_password_hash, check_password_hash


uploads_dir = os.path.join(qwerty, 'website\\static\\img')
views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    locomotives = Locomotive.query.all()

    return render_template("Glavnaya.html" , locomotives=locomotives, user=current_user )


@views.route('/locomotive/<id>')
def show_locomotive(id):
    locomotives = Locomotive.query.all()
    locomotive = Locomotive.query.filter_by(id=id).first()

    return render_template("home.html", locomotives=locomotives, locomotive=locomotive, user=current_user)

@views.route('/novosti')
def novosti_locomotive():
    locomotives = Locomotive.query.all()
    nov = Nov.query.order_by(Nov.id.desc()).all()

    return render_template("Nov.html", nov=nov, user=current_user, locomotives=locomotives)


@views.route('/locomotive/<id>/delete')
def loc_delete(id):
    locomotives = Locomotive.query.get_or_404(id)

    try:
        db.session.delete(locomotives)
        db.session.commit()
        return redirect(url_for('views.home'))
    except:
        return  "При удаление локомотива произошла ошибка" 

@views.route('/novosti/<id>/delete')
def nov_delete(id):
    nov = Nov.query.get_or_404(id)

    try:
        db.session.delete(nov)
        db.session.commit()
        return redirect(url_for('views.home'))
    except:
        return  "При удаление локомотива произошла ошибка" 
    

@views.route("/create-novost", methods=['GET', 'POST'])
def create_post():
    locomotives = Locomotive.query.all()
    if request.method == "POST":
        header = request.form.get('header')
        text = request.form.get('text')

        if not text:
            flash('Новость не должена быть пустой!', category='error')
        else:
            post = Nov(header=header, text=text)
            db.session.add(post)
            db.session.commit()
            flash('Новость создана!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user, locomotives=locomotives)




@views.route("/create-locomotive", methods=["POST", "GET"])
def create_locomotive():
    locomotives = Locomotive.query.all()
    if request.method == "POST":
        pic = request.files['pic']

        series = request.form.get('series')
        number = request.form.get('number')
        power_type = request.form.get('power_type')
        factory = request.form.get('factory')
        number_of_sections = request.form.get('number_of_sections')
        construction_speed = request.form.get('construction_speed')
        type_of_braking = request.form.get('type_of_braking')
        opisanie = request.form.get('opisanie')

        if not pic:
            flash('Фотография не загрузилась!', category='error')
        elif not series:
            flash('Поле "Серия" не должно быть пустым!', category='error')
        elif not number:
            flash('Поле "Номер" не должно быть пустым!', category='error')
        elif not power_type:
            flash('Поле "Тип Тока" не должно быть пустым!', category='error')
        elif not factory:
            flash('Поле "Завод" не должно быть пустым!', category='error')
        elif not number_of_sections:
            flash('Поле "Количество секций" не должно быть пустым!', category='error')
        elif not construction_speed:
            flash('Поле "Конструкционная скорость" не должно быть пустым!', category='error')
        elif not type_of_braking:
            flash('Поле "Тип торможения" не должно быть пустым!', category='error')
        elif not opisanie:
            flash('Поле "Описание" не должно быть пустым!', category='error')
        else:
            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype
            
            if not filename or not mimetype:
                flash('Не загрузилось !', category='error')
            else:
                loc = Locomotive(
                    series=series,
                    number=number,
                    power_type=power_type,
                    factory=factory,
                    number_of_sections=number_of_sections,
                    construction_speed=construction_speed,
                    type_of_braking=type_of_braking,
                    opisanie=opisanie,
                    mimetype=mimetype,
                    name=filename
                )
                id_arr = Locomotive.query.all()
                if len(id_arr) == 0:
                    path = os.path.normpath(os.path.join(uploads_dir, str(1)))
                else:
                    path = os.path.normpath(os.path.join(uploads_dir, str(id_arr[-1].id + 1)))
                
                os.makedirs(path, exist_ok=True)
                print(filename)

                # сохраняет картинку в заданный путь
                with open(os.path.join(path, filename), "wb") as f:
                    a = pic.read()
                    f.write(a)
                
                db.session.add(loc)
                db.session.commit()
                flash('Локомотив добавлен!', category='success')
                return redirect(url_for('views.home'))
                
    return render_template("form_locomotive.html", user=current_user, locomotives=locomotives)

@views.route('/<int:id>', methods=["GET"])
def get_img(id):
    img = Locomotive.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=Locomotive.mimetype)




