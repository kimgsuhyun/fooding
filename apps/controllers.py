# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash,g, session, jsonify
from werkzeug.security import generate_password_hash, \
    check_password_hash
from sqlalchemy import desc
from apps import app, db


from apps.models import (
    Rda,
    Food,
    User,
    Food_reg,
    resultAn
)



@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'info' in session:
        return render_template("input.html")
    return render_template("info.html")

@app.route('/info', methods=['GET', 'POST'])
def info():
    if request.args:
        weight = request.args['weight']
        height = request.args['height']
        if weight > 80 and height >170:
            rda=Rda.query.get(1)
            session.permanent = True
            session['info'] = rda.seq
            session['h'] = weight
            session['w'] = height
            return redirect(url_for('index'))

@app.route('/foodenter', methods=['GET', 'POST'])
def foodenter():
    if request.args:
        #입력값 받아오기
        textget = request.args['test_get']
        #음식 데이터베이스 다받아오기
        foods=Food.query.filter(Food.food_name)
        food_info={}
        #신체정보 획득
        height = session['h']
        weight = session['w']
        userinfo = session['info']
        rda=Rda.query.get(userinfo)
        cal=rda.kcal
        #필요한거골라내기
        named = []
        nad = [] 
        for i in foods:
            if textget in i.food_name:
                #음식정보획득
                entername=i.food_name
                enterna=i.food_na
                named.append(entername)
                nad.append(enterna)
        #넘기기위해.
        food_info['name']=named
        food_info['na']=nad
        return render_template("base.html", food=food_info,name=food_info['name'],na=food_info['na'], height=height, weight=weight, useca=cal )

#문제점 : 속도. 그리고 억지 ㅋㅋㅋ