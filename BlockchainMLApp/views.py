from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from web3 import Web3, HTTPProvider
import time
from datetime import date

global hospital
global username

global details
details=''
global contract

train = pd.read_csv('dataset.csv')
X = train.values[:, 0:13] 
Y = train.values[:, 13]
indices = np.arange(X.shape[0])
np.random.shuffle(indices)
X = X[indices]
Y = Y[indices]
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.101)
rfc = RandomForestClassifier()
rfc.fit(X, Y)
predict = rfc.predict(X_test)
accuracy = accuracy_score(predict, y_test)
print("\n\nRandom Forest Machine Learning accuracy on Healthcare Bag of words data: "+str(accuracy))

def readDetails():
    global details
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'BlockchainMLContract.json' #industrial contract code
    deployed_contract_address = '0xf44e48B4BC40aF1a8aec84fd16E0a2dF5E048714' #hash address to access industrail contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    details = contract.functions.getHealthRecord().call()
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]

def saveDataBlockChain(currentData):
    global details
    global contract
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'BlockchainMLContract.json'
    deployed_contract_address = '0xf44e48B4BC40aF1a8aec84fd16E0a2dF5E048714'
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails()
    details+=currentData
    msg = contract.functions.setHealthRecord(details).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Predict(request):
    if request.method == 'GET':
       return render(request, 'Predict.html', {})
    

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def AddPatientCondition(request):
    if request.method == 'GET':
       return render(request, 'AddPatientCondition.html', {})

def PredictAction(request):
    global rfc
    if request.method == 'POST':
        global details
        pid = request.POST.get('t1', False)
        readDetails()
        print("p det "+details)
        arr = details.split("\n")
        output = ''
        font = "<font size=3 color=black>"
        for i in range(len(arr)-1):
            array = arr[i].split(",");
            print(array[0]+"==="+pid)
            if array[0] == pid:
                output+="<tr><td>"+font+array[0]+"</td>"
                output+="<td>"+font+array[1]+"</td>"
                output+="<td>"+font+array[2]+"</td>"
                output+="<td>"+font+array[3]+"</td>"
                output+="<td>"+font+array[4]+"</td>"
                output+="<td>"+font+array[5]+"</td>"
                output+="<td>"+font+array[6]+"</td>"
                output+="<td>"+font+array[7]+"</td>"
                output+="<td>"+font+array[8]+"</td>"
                output+="<td>"+font+array[9]+"</td>"
                output+="<td>"+font+array[10]+"</td>"
                output+="<td>"+font+array[11]+"</td>"
                output+="<td>"+font+array[12]+"</td>"
                output+="<td>"+font+array[13]+"</td>"
                output+="<td>"+font+array[14]+"</td>"
                output+="<td>"+font+array[15]+"</td>"
                output+="<td>"+font+array[16]+"</td>"
                data = 'age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal\n'
                data+=array[4]+","+array[5]+","+array[6]+","+array[7]+","+array[8]+","+array[9]+","+array[10]+","+array[11]+","+array[12]+","+array[13]+","
                data+=array[14]+","+array[15]+","+array[16]
                file = open('testdata.txt','w')
                file.write(data)
                file.close()
                test = pd.read_csv('testdata.txt')
                test = test.values[:, 0:13]
                y_pred = rfc.predict(test)
                print("predict : "+str(y_pred))
                if y_pred[0] == 0.0:
                    output+="<td>"+font+"Condition is Normal"+"</td>"
                if y_pred[0] == 1.0:
                    output+="<td>"+font+"Condition is Abnormal"+"</td>"
        context= {'data':output}
        return render(request, 'Result.html', context)     
            

def AddPatientConditionAction(request):
    global username
    global hospital
    if request.method == 'POST':
        today = date.today()
        pid = request.POST.get('pid', False)
        age = request.POST.get('age', False)
        gender = request.POST.get('gender', False)
        cp = request.POST.get('cp', False)
        bps = request.POST.get('trestbps', False)
        chol = request.POST.get('chol', False)
        fbs = request.POST.get('fbs', False)
        ecg = request.POST.get('restecg', False)
        thalach = request.POST.get('thalach', False)
        exang = request.POST.get('exang', False)
        oldpeak = request.POST.get('oldpeak', False)
        slope = request.POST.get('slope', False)
        ca = request.POST.get('ca', False)
        thal = request.POST.get('thal', False)
        data= pid+","+username+","+hospital+","+str(today)+","+age+","+gender+","+cp+","+bps+","+chol+","+fbs+","+ecg+","+thalach+","+exang+","+oldpeak+","+slope+","+ca+","+thal+"\n"
        saveDataBlockChain(data)
        context= {'data':'Patient condition saved in Blockchain'}
        return render(request, 'AddPatientCondition.html', context) 

def Signup(request):
    if request.method == 'POST':
      #user_ip = getClientIP(request)
      #reader = geoip2.database.Reader('C:/Python/PlantDisease/GeoLite2-City.mmdb')
      #response = reader.city('103.48.68.11')
      #print(user_ip)
      #print(response.location.latitude)
      #print(response.location.longitude)
      username = request.POST.get('username', False)
      password = request.POST.get('password', False)
      contact = request.POST.get('contact', False)
      email = request.POST.get('email', False)
      address = request.POST.get('address', False)
      utype = request.POST.get('type', False)
      hname = request.POST.get('hospital', False)
      
      db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BlockchainML',charset='utf8')
      db_cursor = db_connection.cursor()
      student_sql_query = "INSERT INTO register(username,password,contact,email,address,usertype,hospital_name) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"','"+utype+"','"+hname+"')"
      db_cursor.execute(student_sql_query)
      db_connection.commit()
      print(db_cursor.rowcount, "Record Inserted")
      if db_cursor.rowcount == 1:
       context= {'data':'Signup Process Completed'}
       return render(request, 'Register.html', context)
      else:
       context= {'data':'Error in signup process'}
       return render(request, 'Register.html', context)    
        
def UserLogin(request):
    if request.method == 'POST':
        global username
        global hospital
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        utype = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'BlockchainML',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    hospital = row[6]
                    utype = 'success'
                    break
        if utype == 'success':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        if utype == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)
    
