# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash,g, session, jsonify,make_response
from werkzeug.security import generate_password_hash, \
    check_password_hash
from sqlalchemy import desc
from apps import app, db
from google.appengine.ext import db as gdb
import logging
from apps.models import (
    Rda,
    Food,
    User,
    Food_reg,
    resultAn
)
from google.appengine.api import images
from werkzeug.http import parse_options_header
from google.appengine.ext import blobstore
# photo class
class BDB(gdb.Model):
    photo = gdb.BlobProperty()

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    #로그인 되있으면 메인으로//지워뿌//

    return render_template("base.html")


#Food(모델) 에서 값 가져오기.
@app.route('/search', methods=['GET', 'POST'])
def search():
    foods=Food.query.all()
    #변수 만들기위한 껍데기 registerfood
    registerfood={"seq":1}

    session['photo']="AMIfv95RbWjkmPYBvnwi6uedBIMmzMNhyeKklM8lJ8LdIGBdxAGyGIwCVw2c1KWJyP5irLHQt0DJ-eDJoeiRwOqvAY-YF54YRWSrWubecGMR_ub7JHqSiHztyMYinINIIPQ2dBhXgCFY2iHzeEfXAT1Fws_Be5UHvA"
    return render_template("foodregister.html",photo_key=session['photo'], foods=foods, registerfood=registerfood)

#음식검색 기능만 
@app.route('/foodsearch', methods=['GET', 'POST'])
def foodsearch():
    foods=Food.query.all()
    if request.args:
        #입력값 받아오기
        textget = request.args['test_get']
        #음식데이터베이스받기
        foods=Food.query.all()
        for info in foods:
            if textget == info.food_name:
                #음식정보획득
                enterseq = info.seq
                #그 seq에 맞는 food 불러서 registerfood에 넣기
                registerfood=Food.query.get(enterseq)
                return render_template("foodregister.html",photo_key=session['photo'], foods=foods,  registerfood=registerfood)
                #에러화면 불르기...ㅠㅠ
        return render_template("error.html")
        
#Food_reg(모델)에 넣을거 정하기 
@app.route('/regi/<int:seq>', methods=['GET', 'POST'])
def regi(seq):

    if request.method == 'GET':
        # #혹수정될지모르는 음식 정보들
        # food_amount = request.args['food_amount']
        # food_cal = request.args['food_cal']
        # food_na = request.args['food_na']
        # food_sugar = request.args['food_sugar']
        # food_fat = request.args['food_fat']
        # food_satur = request.args['food_satur']
        # food_protein = request.args['food_protein']

        # editfood = Food(
        #     food_amount = food_amount,   
        #     food_cal = food_cal,
        #     food_na = food_na,
        #     food_sugar = food_sugar,
        #     food_fat = food_fat,
        #     food_satur = food_satur,
        #     food_protein = food_protein
        #     )
        # db.session.add(editfood)
    
         #사용자의 음식등록
        eat_type = request.args['eat_type']
        count = request.args['count']
        eat_date = request.args['eat_date']
        description = request.args['description']
        dayint = eat_date.split('/')
        reg = Food_reg(
            food_seq = seq,   
            eat_type = eat_type,
            eat_date_year = int(dayint[2]),
            eat_date_month = int(dayint[0]),
            eat_date_day =  int(dayint[1]),
            count = count,
            description = description,
            photo=session['photo']
            )
        db.session.add(reg)
        db.session.commit()
        # foods=Food.query.get(seq)
        # regg=Food_reg.query.all()
        return render_template("base.html")

#1,2,3(즉, 아침점심저녁)에 맞는 음식정보가져오기. 사실 날짜구분없이 아침인거 다 가져오는 시스템. 이거필요없을거같긴함.
@app.route('/graph/<int:seq>', methods=['GET', 'POST'])
def graph(seq):
    #변수초기화
    reg_foodname={"food_amount":0,"food_cal":0,"food_na":0 ,"food_sugar":0 ,"food_fat":0 ,"food_satur":0,"food_protein":0}
    regseq = {}
    #등록된 정보 불러오기
    regseq['reg'] = Food_reg.query.filter_by(eat_type=seq)
    #등록정보로 음식정보(음식이름이나 영양소) 불러6오기
    for i in regseq['reg']:
        regf = Food.query.get(i.food_seq)
        reg_foodname["food_amount"]+=regf.food_amount
        reg_foodname["food_cal"]+=regf.food_cal
        reg_foodname["food_na"]+=regf.food_na
        reg_foodname["food_sugar"]+=regf.food_sugar
        reg_foodname["food_fat"]+=regf.food_fat
        reg_foodname["food_satur"]+=regf.food_amount
        reg_foodname["food_protein"]+=regf.food_protein
    totalinput=reg_foodname["food_sugar"]+ reg_foodname["food_fat"]+reg_foodname["food_protein"]  
    persugar=(float(reg_foodname["food_sugar"])/float(totalinput))*100
    perfat=(float(reg_foodname["food_fat"])/float(totalinput))*100
    perprotein=(float(reg_foodname["food_protein"])/float(totalinput))*100
    return render_template("daily.html",regseq=regseq, reg_foodname=reg_foodname,perfat=perfat,totalinput=totalinput,persugar=persugar,perprotein=perprotein)
    
#날짜로 음식등록정보 검색하기.
@app.route('/date', methods=['GET', 'POST'])
def datesearch():
    eat_date = request.args['eat_date']
    #초기화
    reg_foodname={"food_amount":0,"food_cal":0,"food_na":0 ,"food_sugar":0 ,"food_fat":0 ,"food_satur":0,"food_protein":0}
    #/ 로 년월일 구분하는거
    dayint = eat_date.split('/')
    regseq = {}
    if Food_reg.query.filter_by(eat_date_year=int(dayint[2])):
        regseq['year']=Food_reg.query.filter_by(eat_date_year=int(dayint[2]))
        for i in regseq['year']:

            if i.eat_date_month == int(dayint[0]):
                #월만 구분한 다음에 day에맞는거 필터걸어서 가져옮(Food_reg 안에있는거 가져옮)
                regseq['reg']=Food_reg.query.filter_by(eat_date_day=int(dayint[1]))
                #그다음 day가 같은 거의 food 정보(Food 모델안에있는걸 가져옮) 끌어오기 위한거.
                if i.eat_date_day == int(dayint[1]):          
                    regf = Food.query.get(i.food_seq)
                    reg_foodname["food_amount"]+=regf.food_amount
                    reg_foodname["food_cal"]+=regf.food_cal
                    reg_foodname["food_na"]+=regf.food_na
                    reg_foodname["food_sugar"]+=regf.food_sugar
                    reg_foodname["food_fat"]+=regf.food_fat
                    reg_foodname["food_satur"]+=regf.food_amount
                    reg_foodname["food_protein"]+=regf.food_protein
        totalinput=reg_foodname["food_sugar"]+ reg_foodname["food_fat"]+reg_foodname["food_protein"]  
        persugar=(float(reg_foodname["food_sugar"])/float(totalinput))*100
        perfat=(float(reg_foodname["food_fat"])/float(totalinput))*100
        perprotein=(float(reg_foodname["food_protein"])/float(totalinput))*100
        return render_template("daily.html",regseq=regseq, reg_foodname=reg_foodname,perfat=perfat,totalinput=totalinput,persugar=persugar,perprotein=perprotein)
    
    #에러창 뜲...
    return render_template("error.html")
    
    
#여기서 사진 세션 등록.. 
@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
    upload_uri = blobstore.create_upload_url('/article/create/')

    if request.method == 'POST':

        f = request.files['photo']
        header = f.headers['Content-Type']
        parsed_header = parse_options_header(header)
        blob_key = parsed_header[1]['blob-key']
        # 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
        # reg = Food_reg.quety.get(seq=40)
        session['photo'] = blob_key
        session['photocheck'] = "1"

        #여기서 바로 음식등록으로 넘어가게 만듬
        foods=Food.query.all()
        #변수 만들기위한 껍데기 registerfood
        registerfood={"seq":1}
        return render_template("foodregister.html",photo_key=session['photo'], foods=foods, registerfood=registerfood)

    return render_template('image.html',  upload_uri=upload_uri, active_tab='article_create')

#
@app.route('/photo/resized/<path:blob_key>/', methods=['GET'])
def photo_get_resized(blob_key):
    if blob_key:
        blob_info = blobstore.get(blob_key)
        logging.warn(blob_info)
        if blob_info:
            img = images.Image(blob_key=blob_key)
            img.resize(width=300, height=300)
            img.im_feeling_lucky()
            thumbnail = img.execute_transforms(output_encoding=images.PNG)
            logging.info(thumbnail)

            response = make_response(thumbnail)
            response.headers['Content-Type'] = blob_info.content_type
            return response


@app.route('/abc', methods=['GET', 'POST'])
def abc():
    if request.args:
        age = request.args['age']
        kcal = request.args['cal']
        protein = request.args['pro']
        sugar = request.args['su']
        na = request.args['na']
        fat = request.args['fat']
        gender = request.args['sex']


        rda = Rda(
            age = age,   
            kcal = kcal,
            na = na,
            sugar = sugar,
            protein =  protein,
            fat = fat,
            gender = gender
            )
        db.session.add(rda)
        db.session.commit()
        # foods=Food.query.get(seq)
        # regg=Food_reg.query.all()
        return render_template("upload.html")
    return render_template("upload.html")