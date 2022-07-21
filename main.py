import base64
from io import BytesIO
import json
from flask import *
import os
from PIL import Image
import sqlite3
import threading
import iris_learn, new_pic

app = Flask(__name__)

inproc = False
again = False


@app.route("/", methods=["POST"])
def index():
    img = Image.open(request.files['file'])
    point = request.form.get('point')
    info = request.form.get('info')
    park = request.form.get('park')
    url = request.form.get('url')
    location_longitude = request.args.get('location_longitude')
    location_width = request.args.get('location_width')
    if not point_in_base(point):
        if not park_in_base(park):
            add_park(park, img)
        id = add_point(get_park_id(park), get_iris_id(point), point, info, url)
        add_loc(id, location_longitude, location_width)
    add_img(point, img)
    t = threading.Thread(target=learn)
    t.start()
    return "goode"


def add_loc(id, h, w):
    db = sqlite3.connect("Database/ParKulting.db")
    cursor = db.cursor()
    sqlite_insert_query = f"""INSERT INTO location_points
                            (point_id, location_width, location_longitude)
                            VALUES (?, ?, ?);"""
    data = (id, h, w)
    count = cursor.execute(sqlite_insert_query, data)
    db.commit()


def get_park_id(name):
    db = sqlite3.connect("Database/ParKulting.db")
    cursor = db.cursor()
    id = cursor.execute(f'select id from parks where park = "{name}"').fetchall()[0][0]
    return id


def get_iris_id(name):
    fold = os.listdir("Data/pic\\")[-1]
    num = ""
    for i in fold:
        if i in "0123456789":
            num += i
    num = int(num) + 1
    os.mkdir("pic\\" + str(num) + name)
    return num


def add_point(park_id, iris_id, name, info, url):
    db = sqlite3.connect("Database/ParKulting.db")
    cursor = db.cursor()
    sqlite_insert_query = f"""INSERT INTO points_in_park
                            (id, park_id, point, info, url, iris_id)
                            VALUES (?, ?, ?, ?, ?, ?);"""
    last_id = cursor.execute('select id from points_in_park').fetchall()[-1][0]
    data = (last_id + 1, park_id, name, info, url, iris_id)
    count = cursor.execute(sqlite_insert_query, data)
    db.commit()
    return last_id + 1


def add_park(name, img):
    im_file = BytesIO()
    img.save(im_file, format="JPEG")
    im_bytes = im_file.getvalue()
    im_b64 = base64.b64encode(im_bytes)
    db = sqlite3.connect("Database/ParKulting.db")
    cursor = db.cursor()
    last_id = cursor.execute('select id from parks').fetchall()[-1]
    sqlite_insert_query = f"""INSERT INTO parks
                              (id, park, img)
                              VALUES (?, ?, ?);"""
    data_tuple = (last_id[0] + 1, name, str(im_b64))
    count = cursor.execute(sqlite_insert_query, data_tuple)
    db.commit()


def park_in_base(name):
    db = sqlite3.connect("Database/ParKulting.db")
    cursor = db.cursor()
    sql_req = f"""
                SELECT * 
                FROM parks
                WHERE park = "{name}"
                """
    res = list(cursor.execute(sql_req))
    return len(res) == 1


def point_in_base(name):
    db = sqlite3.connect("Database/ParKulting.db")
    cursor = db.cursor()
    sql_req = f"""
                SELECT * 
                FROM points_in_park
                WHERE point = "{name}"
                """
    res = list(cursor.execute(sql_req))
    if len(res) == 1:
        if res[0][5] == None:
            fold = os.listdir("Data/pic\\")[-1]
            num = ""
            for i in fold:
                if i in "0123456789":
                    num += i
            num = int(num) + 1
            os.mkdir("pic\\" + str(num) + name)
            db = sqlite3.connect("Database/ParKulting.db")
            cursor = db.cursor()

            sql_req = f"""
                        UPDATE  points_in_park
                        SET iris_id =={num}
                        WHERE point = "{name}"
                        """
            cursor.execute(sql_req)
            db.commit()
        return True
    else:
        return False


def add_img(name, img):
    folder = "pic\\" + get_folder_name(name) + "\\"
    a = sorted(os.listdir(folder), key=lambda x: int(x.split(".")[-2]))
    id = 0
    if len(a) != 0:
        id = int(a[-1].split(".")[-2])
    savename = folder + name + "." + str(id + 1) + ".jpg"
    img.save(savename)


def get_folder_name(name):
    db = sqlite3.connect("Database/ParKulting.db")
    cursor = db.cursor()
    sql_req = f"""
                    SELECT * 
                    FROM points_in_park
                    WHERE point = "{name}"
                    """
    res = list(cursor.execute(sql_req))[0]
    return str(res[5]) + name


def learn():
    global again, inproc
    if not inproc:
        again = True
        while again:
            again = False
            new_pic.new_pic()
            iris_learn.iris_learn()
            up_version()
    else:
        again = True


def up_version():
    with open('version.json', 'r+') as f:
        data = json.load(f)
        data['version'] = int(data['version']) + 1
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part


@app.route("/get/<name>")
def get_image(name):
    try:
        return send_from_directory(os.path.abspath(os.curdir), name, as_attachment=True)
    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    app.run()
