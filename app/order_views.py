import os

from flask import Blueprint, render_template, jsonify, session, request

from app.models import User, House, Area, Facility, HouseImage
from utils.function import login_required

order_blue = Blueprint('order', __name__)


@order_blue.route('/booking/<int:id>/', methods=['GET'])
@login_required
def booking(id):
    session['house_id'] = id
    return render_template('booking.html')


@order_blue.route('/my_booking/', methods=['GET'])
@login_required
def my_booking():
    house_id = session['house_id']
    house = House.query.get(house_id)
    data = house.to_dict()
    return jsonify({'code': 200, 'data': data})


@order_blue.route('/index/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')