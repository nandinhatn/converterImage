# This is a sample Python script.
import pathlib

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, jsonify, request, json, render_template, send_from_directory
from flask_cors import CORS
from pathlib import Path
from PIL import Image
import os
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)
images = []
images_download=[]

@app.route('/')
def hello():
    return render_template('index.html', images=images)


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route("/image", methods=['GET', 'POST'])
def print_hi():
    return jsonify(
        name='fenanda',
        email='fernanda@poppt'
    )


def convert(path, filename, types):
    print(path)
    im = Image.open(f"images/{filename}").convert("RGB")
    print(types)
    if types == None:
        types = 'webp'
    print(filename.partition('.')[0])
    name = filename.partition('.')[0]
    # types_transform = f"{types}"
    # print(types_transform)
    # ********** TO DO ******** #
    # ****TROCAR O TYPES ******
    # path = f"{filename}.{types}"
    # im.save(f'C:/Users/Fernanda/Documents/convertImage/images/{path}', 'webp', quality=55)
    im.save(f"static/{name}.{types}", f"{types}", quality=55)
    # im.save(f"static/{name}.{types}", f"{types}", quality=55)
    # return jsonify({'status': 200, 'path': path})
    images_download.append(f"{name}.{types}")
    print(images_download)
    return render_template("index.html", status=200, path=path, images_donwload=images_download)






@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == 'POST':
        print(request.files['file'])
        print(request.form.get('types'))
        types = request.form.get('types')

        f = request.files['file']

        f.save(f"images/{f.filename}")
        images.append({'filename': f.filename, 'file': f, 'types': types})
        print(images)

        return render_template("index.html", images=images)
        # return convert(request.files['file'], f.filename,types)

@app.route("/change_types", methods=["GET","POST"])
def change_types():
    types = request.args.get('types')
    file = request.args.get('file')
    print(types)
    print(file)

    for i, filename in enumerate(images):
       print(types)
       if filename['filename']== file:
           print(filename)
           filename['types'] = types
           print(images)



    return jsonify(
        sucess=200

    )


@app.route("/getFiles", methods=["POST", "GET"])
def getFiles():
    for image in images:
        # convert(image['file'], image['filename'],'webp')
        #print(image['file'])
        #print(image['filename'])
        convert(image['file'], image['filename'], image['types'])
        # convert(image,image.filename,'webp')

    # return convert(request.files['file'], f.filename,types)
    return render_template("index.html", images=images, status=200, images_download=images_download)


# Press the green button in the gutter to run the script.

@app.route('/delete', methods=['GET'])
def delete_file():


    #print(request.args.get('item'))
    item = request.args.get('item')

    #print(request.args('item')['filename'])
    for i, filename in enumerate(images):

        if filename['filename']== item:
           # print("delete item:")
           # print(images[i]['filename'])
            os.unlink(images[i]['filename'])
            del images[i]
    #item = request.args.get('item')
    #images.remove(item)
    # remove o arquivo no diretório
    #os.unlink(item)

    return render_template('index.html', images=images)

def getTime():
    print(os.walk("/static"))
    res=[]
    for(dir_path, dir_names, file_names) in os.walk("static"):
            res.extend(file_names)
            print(file_names)

    images_in=[]
    for(dir_path, dir_names, file_names) in os.walk("images"):
        images_in.extend(file_names)

    now = datetime.now()

    print(now)
    limit = 8 * 60 * 60
    limit = 10
    for re in res:
        stat_info= os.stat(f"static/{re}")
        creation_time = datetime.fromtimestamp(stat_info.st_ctime)



        dif = now - creation_time
        print(dif.seconds)
        print(limit)
        if dif.seconds > limit:
            print("passow")
            print("aqui ", re)
            print(f"images/{re}")
            os.unlink(f"static/{re}")


        for images in images_in:
            stat_info = os.stat(f"images/{images}")
            creation_time = datetime.fromtimestamp(stat_info.st_ctime)
            dif = now - creation_time
            print(dif.seconds)
            print(limit)
            if dif.seconds > limit:
                print("passow")
                print(images)

                os.unlink(f"images/{images}")





        #print(creation_time)
        #print(re)



if __name__ == '__main__':
    getTime()
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
