import os
import random
import re
import uuid

from flask import Blueprint, render_template, jsonify, session, request
from flask_login import login_user
from werkzeug.security import check_password_hash

from app.models import User
from utils.function import login_required

user_blue = Blueprint('user', __name__)


@user_blue.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@user_blue.route('/register/', methods=['POST'])
def my_register():
    # 获取参数
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    # 1.验证参数是否都填写了
    if not all([mobile, imagecode, passwd, passwd2]):
        return jsonify({'code': 1001, 'msg': '请填写完整的参数！'})
    # 2.验证手机号正确
    if not re.match(r'^1[3456789]\d{9}$', mobile):
        return jsonify({'code': 1002, 'msg': '手机号格式错误！'})
    # 3.验证图片验证码
    if session['img_code'] != imagecode:
        return jsonify({'code': 1003, 'msg': '验证码错误！'})
    # 4.密码和确认密码是否一致
    if passwd != passwd2:
        return jsonify({'code': 1004, 'msg': '两次输入密码不一致！'})
    # 验证手机号是否被注册
    user = User.query.filter_by(phone=mobile).first()
    if user:
        return jsonify({'code': 1005, 'msg': '该手机号已经被注册！'})
    # 创建注册信息
    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = passwd
    user.add_update()

    return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/code/', methods=['GET'])
def get_code():
    # 获取验证码
    # 方式1：后端生成图片，并返回验证码图片的地址
    # 方式2：后端只生成随机参数，返回给页面，在页面中再生成图片(前端做)
    s = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for i in range(4):
        code += random.choice(s)
    session['img_code'] = code
    return jsonify({'code': 200, 'msg': '请求成功', 'data': code})


@user_blue.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@user_blue.route('/my_login/', methods=['GET'])
def my_login():
    # 获取参数
    mobile = request.args.get('mobile')
    passwd = request.args.get('passwd')
    # 1.验证参数是否都填写了
    if not all([mobile, passwd]):
        return jsonify({'code': 1001, 'msg': '请填写完整的账号密码！'})
    # 2.验证是该账号是否注册
    user = User.query.filter_by(phone=mobile).first()
    if not user:
        return jsonify({'code': 1002, 'msg': '账号不存在，请先注册！'})
        # 2.判断密码是否正确
    if not user.check_pwd(passwd):
        return jsonify({'code': 1003, 'msg': '密码错误'})
    # 3.登录标识设置
    session['user_id'] = user.id
    return jsonify({'code': 200, 'msg': '登陆成功！'})


@user_blue.route('/my/', methods=['GET'])
@login_required
def my():
    return render_template('my.html')


@user_blue.route('/user_info/', methods=['GET'])
@login_required
def user_info():
    # 获取用户基本信息
    user_id = session['user_id']
    user = User.query.get(user_id)
    user = user.to_basic_dict()
    return jsonify({'code': 200, 'msg': '请求成功!', 'data': user})


@user_blue.route('/logout/', methods=['GET'])
@login_required
def logout():
    del session['user_id']
    return jsonify({'code': 200, 'msg': '请求成功', 'errno': 0})


@user_blue.route('/profile/', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')


@user_blue.route('/profile/', methods=['PATCH'])
@login_required
def my_profile():
    # 获取项目根路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 获取媒体文件路径
    MEDIA_DIR = os.path.join(BASE_DIR, '/static/media/')
    # 接收图片
    ico = request.files['avatar']
    # 获取图片名称
    filename = ico.filename
    # 保存图片
    ico.save('./static/media/%s' % filename)
    # 当前登录的用户
    user_id = session['user_id']
    user = User.query.get(user_id)
    # 修改用户头像
    user.avatar = filename
    user.add_update()
    return jsonify({'code': 200})


@user_blue.route('/mm_profile/', methods=['POST'])
@login_required
def mm_profile():
    name = request.form.get('name')
    user_id = session.get('user_id')
    user = User.query.filter_by(name=name).first()
    if user:
        return jsonify({'code': 1001, 'msg': '用户名已经存在！'})
    user = User.query.get(user_id)
    user.name = name
    user.add_update()
    return jsonify({'code': 200, 'msg': '更改成功！'})


@user_blue.route('/auth/', methods=['GET'])
@login_required
def auth():
    return render_template('auth.html')


@user_blue.route('/auth_info/', methods=['GET'])
@login_required
def auth_info():
    # 当前登录用户
    user = User.query.get(session['user_id'])
    id_card = user.id_card
    real_name = user.id_name
    data = {'id_card': id_card, 'real_name': real_name}
    # 已经实名认证
    if id_card:
        return jsonify({'code': 200, 'data': data})
    # 未进行实名认证
    return jsonify({'code': 1001, 'msg': '未进行实名认证'})


@user_blue.route('/my_auth/', methods=['POST'])
@login_required
def my_auth():
    real_name = request.form.get('real_name')
    id_card = request.form.get('id_card')
    # 获取当前登录用户
    user_id = session['user_id']
    user = User.query.get(user_id)
    print(real_name)
    # 第一次实名认证
    if not all([real_name, id_card]):
        return jsonify({'code': 1004, 'msg': '请填写完整的身份信息！'})
    # 认证成功
    if len(real_name) <= 10 and re.match(r'[\u4e00-\u9fa5]+', real_name) and re.match(r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', id_card):
        user.id_name = real_name
        user.id_card = id_card
        user.add_update()
        return jsonify({'code': 200, 'msg': '认证成功'})
    if len(real_name) > 10:
        return jsonify({'code': 1001, 'msg': '姓名最多十个字符！'})
    if not re.match(r'[\u4e00-\u9fa5]+', real_name):
        return jsonify({'code': 1002, 'msg': '姓名只能是中文！'})
    return jsonify({'code': 1003, 'msg': '请输入正确的身份证号！'})