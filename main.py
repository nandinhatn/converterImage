# This is a sample Python script.
import pathlib


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, jsonify, request, json, render_template, send_from_directory
from flask_cors import CORS
from pathlib import Path
from PIL import Image, ImageFilter
import rembg
import numpy as np
import os
import socket
import public_ip as ip

import pillow_avif
from requests import get

import time
from datetime import datetime
from tqdm import tqdm
from time import sleep
app = Flask(__name__)
application = app
CORS(app)
images = []
images_download=[]



def getIp ():
   ip = get('https://api.ipify.org').text
  
   return ip
    

@app.route('/')
def hello():
    getTime()
    hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    images.clear()
    images_download.clear()
   
   
    return render_template('index.html', images=images)

@app.route('/removeBackground')
def favicon():
    images.clear()
    images_download.clear()

    return render_template('removeBackground.html')

@app.route('/static/images/<path:path>')
def serve_static(path):
    return send_from_directory('static/images', path)


@app.route("/image", methods=['GET', 'POST'])
def print_hi():
    return jsonify(
        name='fenanda',
        email='fernanda@poppt'
    )

def removeBg(path, filename,types):
    
    im = Image.open(f'images/{getIp()}/{filename}').convert('RGB')
    input_array = np.array(im)
    output_array = rembg.remove(input_array)
    output_image = Image.fromarray(output_array)
    #output_image.show()
    name = filename.split('.')[0]
    
    path=Path(f'static/images/{getIp()}').mkdir(parents=True, exist_ok=True)
    output_image.save(f"static/images/{getIp()}/{name}.png")
    
    images_download.append(f"{name}.png")
   
    return render_template("removeBackground.html", status=200, path=path, ip=getIp(), images_donwload=images_download)


def convert(path, filename, types):
    print("######################################################################")
    print(path)
    im = Image.open(f"images/{getIp()}/{filename}").convert("RGB")
    #bw = im.convert('L')
    #bw.show()
    #im1 = im.filter(ImageFilter.GaussianBlur)
    #im1.show()
    
  
    
    if types == None:
        types = 'webp'
    print(filename.partition('.')[0])
    name = filename.partition('.')[0]
    ip = getIp()
    # types_transform = f"{types}"
    # print(types_transform)
    # ********** TO DO ******** #
    # ****TROCAR O TYPES ******
    # path = f"{filename}.{types}"
    # im.save(f'C:/Users/Fernanda/Documents/convertImage/images/{path}', 'webp', quality=55)
    path=Path(f'static/images/{ip}').mkdir(parents=True, exist_ok=True)
    im.save(f"static/images/{ip}/{name}.{types}", f"{types}", quality=55)
    # im.save(f"static/{name}.{types}", f"{types}", quality=55)
    # return jsonify({'status': 200, 'path': path})
    images_download.append(f"{name}.{types}")
   
   
    #return render_template("index.html", status=200, ip='getIp()', images_donwload=images_download)



@app.route("/upload_remove", methods=["POST", ])
def upload_file_removeBackground():
    images.clear()
    if request.method == 'POST':
       
        types = request.form.get('types')
        files = request.files.getlist("file")
       
       
        f = request.files['file']

        saveFiles(files,types)


        #f.save(f"images/{f.filename}")
        #images.append({'filename': f.filename, 'file': f, 'types': types})
        print(images)

        return render_template("removeBackground.html", images=images, up=True)
        # return convert(request.files['file'], f.filename,types)



@app.route("/upload", methods=["POST", ])
def upload_file():
  
    images_download.clear()
    if request.method == 'POST':
        
       
        types = request.form.get('types')
        files = request.files.getlist("file")
        
       
        f = request.files['file']
        
        saveFiles(files,types)


       
        

        return render_template("index.html", images=images, up=True)
        



def saveFiles(arrayFotos,types):

   
    path=Path(f'images/{getIp()}').mkdir(parents=True, exist_ok=True)
    
    
   

    for foto in arrayFotos:
        foto.save(f"images/{getIp()}/{foto.filename}")     
        images.append({'filename': foto.filename, 'file': foto,'types': types})
        


@app.route("/change_types", methods=["GET","POST"])
def change_types():
    types = request.args.get('types')
    file = request.args.get('file')
   

    for i, filename in enumerate(images):
      
       if filename['filename']== file:
         
           filename['types'] = types
           



    return jsonify(
        sucess=200

    )


@app.route("/getFiles", methods=["POST", "GET"])
def getFiles():
   
    action = request.args.get('action')
   

    print(len(images))

  
    for image in images:
         #convert(image['file'], image['filename'],'webp')
        #print(image['file'])
        #print(image['filename'])
         print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
         
         if action=='remBG':
           ip = getIp()
           print(action)
           removeBg(image['file'], image['filename'], image['types'])
           #return render_template("removeBackground.html", images=images,  ip=ip, status=200, images_download=images_download)
         else:
          ip = getIp()
          print("*******")           
          convert(image['file'], image['filename'], image['types'])
          #return render_template("index.html", images=images, status=200, ip=ip, images_download=images_download)
        # convert(image,image.filename,'webp')
        #pbar.set_description("Processing %s" % image)
        #status = pbar.set_description("Processing %s" % image)
        #print(status)

    # return convert(request.files['file'], f.filename,types)
    return render_template("index.html", images=images, status=200, images_download=images_download)


# Press the green button in the gutter to run the script.

@app.route('/delete', methods=['GET'])
def delete_file():


   
    item = request.args.get('item')

    
    for i, filename in enumerate(images):

        if filename['filename']== item:
          
            os.unlink(f"images/{getIp()}/{images[i]['filename']}")
            del images[i]
    #item = request.args.get('item')
    #images.remove(item)
    # remove o arquivo no diretório
    #os.unlink(item)

    return render_template('index.html', images=images)

def getTime():
    ip = getIp()
   
   
   
    res=[]
    images_in=[]
    for(dir_path, dir_names, file_names) in os.walk(f"static/images"):
           #res.extend(dir_path)
           print('aqui')
          
           #print(dir_names)
           #print(os.stat(f"static/images"))
           #print(os.stat("/images/"))
           #print(file_names)
           now = datetime.now()
           limit = 60 * 60
           for(dir_path, dir_names, file_names) in os.walk("images"):
              #print(file_names)
              #print(dir_names)
              print(os.stat(dir_path).st_mtime)
              stat_info = os.stat(dir_path).st_mtime
              creation_time = datetime.fromtimestamp(stat_info)
              print(creation_time)
              print(dir_path)
              images_in.extend(file_names)
              dif = now - creation_time
              print(dir_names)
              print(dir_path)
              #print(dif.seconds)
              print(images_in)

              for image in images_in:
                  #print(image)
                  stat_info = os.stat(dir_path).st_mtime
                  #print(stat_info)
                  creation_time = datetime.fromtimestamp(stat_info)
                  #print(creation_time)
                  dif = now - creation_time
                  print(dif.seconds)
                  if dif.seconds > 100:
                      print('passou do tempo')
                      #os.unlink(image)
                      #os.remove(dir_path)
                      print(dir_path)
                      print(f"\{dir_path}/{image}")
                      os.unlink(f"{dir_path}/{image}")
                     #os.unlink(f"/images/179.215.120.204/Becksaerea0000.jpg")
                     
                      
                      #os.unlink("images/179.215.120.204/allanfachada.jpg")
                      #os.unlink(f"images/179.215.120.204/968a82af-cf77-4b62-b01f-2912c7ef0612.jpeg")
    
    for(dir_path, dir_names, file_names) in os.walk("static/images"):
        print(dir_path)
        res.extend(file_names)
        print(res)
        for re in res:
            print(re)
            stat_info = os.stat(dir_path).st_mtime
            creation_time =datetime.fromtimestamp(stat_info)
            dif = now -creation_time
            print(dif.seconds)
            if dif.seconds >100:
                print('passou  tempo do static')
                print(dir_path)
                os.unlink(f"{dir_path}/{re}")

      



if __name__ == '__main__':
    getTime()
    getIp()

    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
