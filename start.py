from flask import Flask, render_template,request,session,redirect,url_for,Response
import pandas as pd
from SectionExtractionModule import *
import numpy as np 
from flask import send_from_directory

app = Flask(__name__)      

app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

@app.route('/')
def home():
    message=request.args.get('message')
    return render_template('index.html',message=message)

@app.route('/getfeatures', methods = ['GET','POST'])
def get_features():
    global output
    if request.method=="POST":
        path=request.form['path']
        print path 
        output=request.form['output']
        
        output=output+".xml"
        
        
        print output
        df=GetOutput(path,output)
        return send_from_directory(".",filename=output, as_attachment=True)
        
    else:
        return redirect(url_for('home'))
    

if __name__ == '__main__':
    #app.run(host= '10.207.61.113',port=5000)
    app.run(debug=True)