import os

from flask import Blueprint, render_template, jsonify, session, request

from app.models import User, House, Area, Facility, HouseImage
from utils.function import login_required

house_blue = Blueprint('house', __name__)


@house_blue.route('/myhouse/', methods=['GET'])
@login_required
def myhouse():
    return render_template('myhouse.html')


@house_blue.route('/myhouse_info/', methods=['GET'])
@login_required
def myhouse_info():
    user = User.query.get(session['user_id'])
    id_card = user.id_card
    # 判断是否实名认证
    if id_card:
        return jsonify({'code': 200})
    return jsonify({'code': 1001})


@house_blue.route('/newhouse/', methods=['GET'])
@login_required
def newhouse():
    return render_template('newhouse.html')


@house_blue.route('/area/', methods=['GET'])
@login_required
def area():
    # 地区信息
    area = Area.query.all()
    area_li = [n.to_dict() for n in area]
    # 房屋配置信息
    facility = Facility.query.all()
    facility_li = [n.to_dict() for n in facility]
    return jsonify({'code': 200, 'data': area_li, 'faci': facility_li})


@house_blue.route('/newhouse_info/', methods=['POST'])
@login_required
def newhouse_info():
    # 获取表单信息
    # 标题
    title = request.form.get('title')
    # 单价
    price = request.form.get('price')
    # 地址
    address = request.form.get('address')
    # 房间数目
    room_count = request.form.get('room_count')
    # 房屋面积
    acreage = request.form.get('acreage')
    # 户型描述，如几室几厅
    unit = request.form.get('unit')
    # 房屋容纳的人数
    capacity = request.form.get('capacity')
    # 房屋床铺的配置
    beds = request.form.get('beds')
    # 房屋押金
    deposit = request.form.get('deposit')
    # 最少入住天数
    min_days= request.form.get('min_days')
    # 最多入住天数
    max_days = request.form.get('max_days')
    # 房屋设施
    facilities = request.form.getlist('facility')
    # 区域
    area_id = request.form.get('area_id')
    if all([title, facilities]):
        # 创建房屋信息
        user_id = session['user_id']
        house = House()
        house.title = title
        house.price = price
        house.address = address
        house.room_count = room_count
        house.acreage = acreage
        house.unit = unit
        house.capacity = capacity
        house.beds = beds
        house.deposit = deposit
        house.min_days = min_days
        house.max_days = max_days
        house.user_id = user_id
        house.area_id = area_id
        # 保存房屋对应的设施
        for fac_id in facilities:
            fac = Facility.query.get(fac_id)
            house.facilities.append(fac)
        house.add_update()
        return jsonify({'code': 200, 'msg': '添加房屋信息成功', 'data': house.id})
    return jsonify({'code': 1001, 'msg': '请填写完整的房屋信息！'})


@house_blue.route('/house_image/', methods=['PATCH'])
@login_required
def house_image():
    # 获取项目根路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 获取媒体文件路径
    MEDIA_DIR = os.path.join(BASE_DIR, '/static/imgs/')
    # 接收图片
    img = request.files['house_image']
    # 获取图片名称
    filename = img.filename
    # 保存图片
    img.save('./static/imgs/%s' % filename)
    # 获取当前房屋对象
    house = HouseImage()
    house_id = request.form.get('house_id')
    house.house_id = house_id
    house.url = filename
    house.add_update()
    # 设置首图
    first_house = House.query.get(house_id)
    first_house.index_image_url = filename
    first_house.add_update()
    return jsonify({'code': 200, 'data': filename})


@house_blue.route('/show_house/', methods=['GET'])
@login_required
def show_house():
    user = User.query.get(session['user_id'])
    # 当前用户发布的房子
    house = House.query.filter_by(user_id=user.id).all()
    if house:
        data = [hous.to_dict() for hous in house]
        return jsonify({'code': 200, 'data': data})


@house_blue.route('/detail/<int:id>/', methods=['GET'])
@login_required
def detail(id):
    session['house_id'] = id
    return render_template('detail.html')


@house_blue.route('/my_detail/', methods=['GET'])
@login_required
def my_detail():
    house_id = session['house_id']
    # 获取房屋对象
    house = House.query.get(house_id)
    data = house.to_full_dict()
    return jsonify({'code': 200, 'data': data})