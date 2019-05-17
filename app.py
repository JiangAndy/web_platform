# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from collections import namedtuple
import os
import cv2

# 初始值及默认路径设置
UPLOAD_FOLDER = 'static/videos'
img_folder = 'static/img'
video_folder = 'static/videos'
result_folder = 'static/bad_result'
video_name = '0010'
basedir = os.path.abspath(os.path.dirname(__file__))

# app参数设置
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)


# 数据库字段设置
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))
    telephone = db.Column(db.String(20))
    administer = db.Column(db.String(3))
    superadmin = db.Column(db.String(3))


'''
def bad_car_data():
    fname = 'car_data.txt'
    with open(fname, 'r') as f:
        name = []
        data = []
        for line in f.readlines():
            curline = line.strip().split(":")
            name.append(curline[0])
            data.append(curline[-1])
    return name, data    
'''


'''
def bad_car_para():
    fname = 'car_para.txt'
    with open(fname, 'r') as f:
        name = []
        data = []
        for line in f.readlines():
            curline = line.strip().split(":")
            name.append(curline[0])
            data.append(curline[-1])
    return name, data 
'''


# 对运行结果进行分析
def analyse_result(fname):
    try:
        file = open(fname, 'r')
    except IOError:
        error = []
        return error
    lists = []
    content = file.readlines()
    length = len(content)
    for i in range(len(content)):
        content[i] = content[i][:len(content[i]) - 1]
        content[i] = content[i].strip().split(",")
        lists.append(content[i])
    file.close()

    return length, lists


ALLOWED_EXTENSIONS = ['mp4', 'webm', 'ogv']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Error Handling　
@app.errorhandler(404)
def FUN_404(error):
    return render_template("error.html")


@app.errorhandler(405)
def FUN_405(error):
    return render_template("error.html")


@app.errorhandler(500)
def FUN_500(error):
    return render_template("error.html")


# 查看相关技术支持
@app.route("/about/")
def FUN_about():
    return render_template("about.html")


# 加入我们
@app.route("/joinus")
def join_us():
    return render_template("joinus.html")


# 案例介绍
@app.route("/example")
def example():
    return render_template("example.html")


# 报错投诉
@app.route("/bug")
def bug():
    return render_template("bug.html")


# 未登录的主界面
@app.route("/")
def main():
    return render_template("main.html")


# 已登录的主界面
@app.route("/main1")
def main1():
    return render_template("main1.html")


# 登录界面
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        # 检查用户名和密码是否正确
        check1 = user.query.filter_by(username=uname).first()
        check2 = user.query.filter_by(password=passw).first()
        if not check1:
            return render_template("checkuser.html")
        if not check2:
            return render_template("checkpasswlogin.html")
        if check1 and check2:
            return redirect(url_for("main1"))
    return render_template("login.html")


# 注册界面
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']
        repassw = request.form['repassw']
        if repassw != passw:
            return render_template("checkpasswregister.html")
        phone = request.form['phone']
        admin = request.values.get("admin")
        suadmin = request.values.get("suadmin")
        check1 = user.query.filter_by(telephone=phone).first()
        if check1:
            return render_template("checkphone.html")
        register = user(username=uname, email=mail, password=passw, telephone=phone, administer=admin, superadmin=suadmin)
        db.session.add(register)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")


# 个人信息界面
@app.route("/mine", methods=["GET", "POST"])
def mine():
    u = user.query.first()
    return render_template("mine.html", username=u.username, email=u.email, telephone=u.telephone, administer=u.administer, superadmin=u.superadmin)


# 修改信息界面
@app.route("/modify", methods=["GET", "POST"])
def modify():
    if request.method == "POST":
        u = user.query.first()
        u.email = request.form['mail']
        u.password = request.form['passw']
        u.telephone = request.form['phone']
        u.administer = request.values.get("admin")
        u.superadmin = request.values.get("suadmin")
        db.session.add(u)
        db.session.commit()
        return redirect(url_for("mine", username=u.username, email=u.email, telephone=u.telephone, administer=u.administer, superadmin=u.superadmin))
    return render_template("modify.html")


# 注销界面
@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template("logout.html")


# 上传车辆视频（保留功能）
@app.route("/car_data", methods=["GET", "POST"])
def car_data():

    if request.method == "POST":
        video = request.form.get("video_type")
        f = request.files['carfile']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            upload = os.path.join(UPLOAD_FOLDER, filename)
            f.save(upload)
            if video:
                is_success = True
                return render_template("main1.html", is_success=is_success)
            '''
            else:
                is_failed = True
                return render_template("main1.html", is_failed=is_failed)
            '''
        '''
            # return render_template("main1.html",video=video,img_src = newdir,length=length, dirlist=dirlist)
        
        if f:
            filename = secure_filename(f.filename)
            basename=filename.rsplit('.',1)[0]
            filedir=os.path.join(UPLOAD_FOLDER,basename)
            isExists=os.path.exists(filedir)
            if not isExists:
                os.makedirs(filedir)
            upload=os.path.join(filedir, filename)
            f.save(upload)
            img=cv2.imread(upload)
            cv2.imwrite(upload,img)
            if video:
                return render_template("main1.html",video=video,img_src = upload)
        '''


# 查看车辆视频
@app.route("/car_video", methods=["GET", "POST"])
def car_video():
    if request.method == "POST":
        f = request.files['videofile']
        if f and allowed_file(f.filename):
            # videoname = request.form.get("video")
            videoname = secure_filename(f.filename)
            videodir = os.path.join(video_folder)
            # videos = os.listdir(videodir)

            video_dir = os.path.join(videodir, videoname)
            print(videoname)
            print(video_dir)
            return render_template("main2.html", video_dir=video_dir)
        # return render_template("main2.html")

    '''
        # car_id = request.form.get("car_id")
        imgdir = request.form.get("videoimg")
        img_dir=os.path.join(img_folder,imgdir)
        imgs=os.listdir(img_dir)
        length=len(imgs)+1
        newdir=[]
        for img in imgs:
            imgpath=os.path.join(img_dir,img)
            img=cv2.imread(imgpath)
            cv2.imwrite(imgpath,img)
            newdir.append(imgpath)
        
        dirlist=os.listdir(img_folder)
        if imgdir:
            return render_template("main2.html",imgdir=imgdir,img_src = newdir,length=length, dirlist=dirlist)
        #if car_id:
            #return render_template("main2.html",carid=car_id,img_src = newdir,length=length, dirlist=dirlist)
   '''


# 交通行为分析结果
@app.route("/traffic_behavior_analysis", methods=["GET", "POST"])
def analysis():
    if request.method == "POST":
        video_num = request.form.get("video_num")
        video_type = request.form.get("video_type")

        # os.system("python ../multi_camera_tracking_mp_yolo/tracking_multi_view_with_ysort.py --data_name DJI "
        #          "--result_path ../car --load_path %s --video_name %s --video_type MOV "
        #         "--show_image False --save_image False --gpu 4" % (video_folder, video_name))
        filename = os.path.join(result_folder, 'analyse_result.txt')
        length, final = analyse_result(filename)
        if video_num and video_type:
            return render_template("main3.html", video_num=video_num, video_type=video_type, final=final, length=length)


# 查看不良交通行为车辆信息
@app.route("/bad_traffic_behavior", methods=["GET", "POST"])
def show_bad():
    if request.method == "POST":
        car_id = request.form.get("car_id")
        fname = car_id + '.txt'
        dirs = os.listdir(result_folder)
        if fname in dirs:
            id_isexist = True
            filename = os.path.join(result_folder, fname)
            length, final = analyse_result(filename)
            if car_id:
                return render_template("main4.html", length=length, final=final, id_isexist=id_isexist)
        else:
            id_isnotexist = True
            return render_template("main4.html", id_isnotexist=id_isnotexist)


if __name__ == "__main__":
    # 创建初始的数据库
    db.create_all()
    app.run(host='192.168.61.122', port=5000, debug=True)
    # host是用户自己的IP地址，port是用户自己的端口号，默认为5000，debug默认为False
    # app.run()
