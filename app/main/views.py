from flask import render_template
from . import main
from flask_login import login_required
from app.model.SaleRecord import SaleRecord
from app.model.Product import Product
from app.model.Administrator import Administrator


@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


