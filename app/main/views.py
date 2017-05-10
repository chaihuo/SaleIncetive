# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, jsonify
from . import main
from .. import db
from flask_login import login_required, current_user
from app.model.SaleRecord import SaleRecord
from app.model.Product import Product
from app.model.Administrator import Administrator
import time



@main.route('/', methods=['GET'])
@login_required
def index():
    print current_user.username
    sale_records = current_user.sale_records
    for sr in sale_records:
        print sr.valid
    products = Product.query.all()
    for prod in products:
        print prod.id, prod.type
    return render_template('index.html', user=current_user, sale_records=sale_records, products=products)


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


# 销售记录列表
@main.route('/admin/sale_records', methods=['GET'])
def admin_sale_records():
    sale_records = SaleRecord.query.all()

    return render_template('admin/sale_record_list.html', sale_records=sale_records)


# 审核销售记录
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
    return render_template('admin/products.html', products=products)

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






