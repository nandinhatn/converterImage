
# This is a sample Python script.
import pathlib
import socket

from flask import Flask, jsonify, redirect, request, json, flash, jsonify, render_template, send_from_directory, url_for
from flask_cors import CORS
from pathlib import Path
from PIL import Image, ImageFilter
import rembg
import numpy as np
import os
import public_ip as ip

import pillow_avif
from requests import get

import time
from datetime import datetime
from tqdm import tqdm
from time import sleep
import logging
logging.basicConfig(filename="minhaaplicacao.log", level=logging.DEBUG, format="%(asctime)s :: %(levelname)s :: %(lineno)d :: %(message)s")
app = Flask(__name__)
application = app
app.config['SECRET_KEY']  = 'MINHA-PALAVRA-SECRETA'
CORS(app)
images = []
logging.info(f" monitora array images {images}")
images_download=[]
ipClient = {ip: ''}
import olefile






def getIp ():
   ip = get('https://api.ipify.org').text
  
   
   return ip
    

@app.route('/')
def hello():
    getTime()
    hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    # images.clear()
    # images_download.clear()
    
   
   
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

def removeBg(path, filename,types, ip):
 
    im = Image.open(f'images/{ip}/{filename}').convert('RGB')
    input_array = np.array(im)
    output_array = rembg.remove(input_array)
    output_image = Image.fromarray(output_array)
    #output_image.show()
    name = filename.split('.')[0]
    
    path=Path(f'static/images/{ip}').mkdir(parents=True, exist_ok=True)
    output_image.save(f"static/images/{ip}/{name}.png")
    
    images_download.append(f"{name}.png")
   
    return render_template("removeBackground.html", status=200, path=path, ip=ip, images_donwload=images_download)


def convert(path, filename, types, ip):
   
    print("######################################################################")
    print(path)
    im = Image.open(f"images/{ip}/{filename}").convert("RGB")

  
    
    if types == None:
        types = 'webp'
    print(filename.partition('.')[0])
    name = filename.partition('.')[0]
    logging.info(f"{types}")
   
   
    path=Path(f'static/images/{ip}').mkdir(parents=True, exist_ok=True)
    im.save(f"static/images/{ip}/{name}.{types}", f"{types}", quality=55)
  
    images_download.append(f"{name}.{types}")
   
   
   



@app.route("/upload_remove", methods=["POST", ])
def upload_file_removeBackground():
    images.clear()
    if request.method == 'POST':
       
        types = request.form.get('types')
        files = request.files.getlist("file")
        ipForm = request.form.get('ip')
        ipClient['ip'] = ipForm
        ip = ipClient['ip']
       
        f = request.files['file']

        saveFiles(files,types,ip)


        
        print(images)

        return render_template("removeBackground.html", images=images, up=True)
        



@app.route("/upload", methods=["POST", ])
def upload_file():
    images.clear()
    images_download.clear()
    if request.method == 'POST':
        
       
        types = request.form.get('types')
        files = request.files.getlist("file")
        ipForm = request.form.get('ip')
       
       
        
       
        f = request.files['file']
        
        saveFiles(files,types,ipForm)


       
        

    return render_template("index.html", images=images, up=True)
        



def saveFiles(arrayFotos,types,ip):
   
   
    path=Path(f'images/{ip}').mkdir(parents=True, exist_ok=True)
    for foto in arrayFotos:
        foto.save(f"images/{ip}/{foto.filename}")     
        images.append({'filename': foto.filename, 'file': foto,'types': types})
        logging.info(f"Add array images {images}")
    logging.info(f"For save complete {images}")
    
        


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
    print(action)  
    ipRequest = request.args.get('ip')
    
    logging.info(f"Checa se pegou o ip {ipRequest} ")
    logging.info(f"Checa imagens {images}")
    for image in images:
                        
         if action=='remBG':
            removeBg(image['file'], image['filename'], image['types'],ipRequest)
          
         else:        
            convert(image['file'], image['filename'], image['types'],ipRequest)

   
    logging.info(f"Finaliza o convert e disponibiliza as imagens {images} - {images_download}")
    return render_template("index.html", images=images, status=200, ip=ipRequest, images_download=images_download)





@app.route('/delete', methods=['GET'])
def delete_file():


   
    item = request.args.get('item')

    
    for i, filename in enumerate(images):

        if filename['filename']== item:
          
            os.unlink(f"images/{getIp()}/{images[i]['filename']}")
            del images[i]
   

    return render_template('index.html', images=images)

def getTime():
   
   
   
   
    res=[]
    images_in=[]
    res.clear()
    images_in.clear()
    for(dir_path, dir_names, file_names) in os.walk(f"images"):
         
           
          
          
           now = datetime.now()
           limit = 60 * 60
           for(dir_path, dir_names, file_names) in os.walk("images"):
             
             
              stat_info = os.stat(dir_path).st_mtime
              creation_time = datetime.fromtimestamp(stat_info)
             
              images_in.extend(file_names)
              dif = now - creation_time
             
          
             

              for image in images_in:
                 
                  stat_info = os.stat(dir_path).st_mtime
                 
                  creation_time = datetime.fromtimestamp(stat_info)
                 
                  dif = now - creation_time
               
                  if dif.seconds > limit:
                      print('passou do tempo')
                      
                      print(dir_path)
                      print(f"\{dir_path}/{image}")
                     
    
    for(dir_path, dir_names, file_names) in os.walk("static/images"):
       
        res.extend(file_names)
       
        for re in res:
          
            stat_info = os.stat(dir_path).st_mtime
            creation_time =datetime.fromtimestamp(stat_info)
            dif = now -creation_time
         
            if dif.seconds >100:
              
                os.unlink(f"{dir_path}/{re}")

      



if __name__ == '__main__':
    # getTime()
   
    app.run(threaded=True, debug=True)
   


