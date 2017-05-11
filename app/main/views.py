# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import func
from app.model.User import User
from . import main
from .. import db
from flask_login import login_required, current_user, logout_user, login_user
from app.model.SaleRecord import SaleRecord
from app.model.Product import Product
import time


# 用户登录
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print request.path
        user = User.query.filter_by(username=username).first()
        print user.verify_password(password)
        if user is not None and user.verify_password(password):
            login_user(user)
            print user.role
            print "login success"
            if user.role == 1:
                return redirect(url_for('main.admin_index'))
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html')


# 用户注册
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        print username, password, repassword
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('register.html')


# 用户登出
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You hava been logged out')
    return redirect(url_for('main.login'))








# 前台首页
@main.route('/', methods=['GET'])
@login_required
def index():
    print current_user.username, current_user.role
    if current_user.role == 0:
        sale_records = current_user.sale_records
        for sr in sale_records:
            print sr.valid
        products = Product.query.all()
        for prod in products:
            print prod.id, prod.type
        return render_template('index.html', user=current_user, sale_records=sale_records, products=products)
    else:
        return 'you are admin'


# 新增销售记录
@main.route('/saleRecord/add', methods=['POST'])
@login_required
def add_sale_record():
    product_id = request.form.get('product_id')
    customer_phone = request.form.get('customer_phone')
    customer_name = request.form.get('customer_name')

    product = Product.query.get(int(product_id))
    sale_record = SaleRecord(user_id=current_user.id, product_id=product.id, customer_phone=customer_phone, customer_name=customer_name, award=product.award)
    db.session.add(sale_record)
    db.session.commit()
    return redirect(url_for('main.index'))



# 后台首页
@main.route('/admin')
@login_required
def admin_index():
    print current_user.username, current_user.role
    if current_user.role == 1:
        return "admin"
    else:
        return "you are not admin"


# 后台销售记录列表
@main.route('/admin/sale_records', methods=['GET'])
def admin_sale_records():
    sale_records = SaleRecord.query.all()

    return render_template('admin/sale_record_list.html', sale_records=sale_records, admin='admin')


# 后台审核销售记录
@main.route('/admin/sale_records/check', methods=['POST'])
def check_sale_record():
    id = request.values.get('id')
    valid = request.values.get('valid')
    sale_record = SaleRecord.query.get(id)
    sale_record.valid = valid
    db.session.add(sale_record)
    db.session.commit()
    return "sucess"



# 产品列表
@main.route('/admin/products', methods=['GET'])
def admin_products():
    products = Product.query.all()
    print len(products)
    return render_template('admin/products.html', products=products, admin='admin')

# 修改激励金
@main.route('/admin/product/update', methods=['POST'])
def update_product():
    id = request.values.get('id')
    award = request.values.get('award')
    product = Product.query.get(id)
    product.award = float(award)
    product.update_time = db.func.current_timestamp()
    db.session.add(product)
    db.session.commit()
    return jsonify({'award': str(product.award), 'update_time': str(product.update_time)})


# 激励金统计排名
@main.route('/admin/awards', methods=['GET'])
def award_stat():
    award_sum_by_user = db.session.query(SaleRecord.user_id, func.sum(SaleRecord.award), func.count('*')).filter(SaleRecord.valid == 1).group_by(SaleRecord.user_id).order_by(SaleRecord.award.desc()).all()
    award_user_list = []
    rank = 1
    for item in award_sum_by_user:
        award_user = {}
        award_user['rank'] = rank
        award_user['username'] = User.query.get(item[0]).username
        award_user['award'] = item[1]
        award_user['num'] = item[2]
        rank += 1
        print award_user
        award_user_list.append(award_user)




    award_sum_by_product = db.session.query(SaleRecord.product_id, func.sum(SaleRecord.award), func.count('*')).filter(SaleRecord.valid == 1).group_by(SaleRecord.product_id).order_by(SaleRecord.award.desc()).all()
    for item in award_sum_by_product:
        print item[0], item[1], item[2]
    return render_template('admin/award_stat.html', award_user_list=award_user_list, admin='admin')






