from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib import messages
from rest_framework.parsers import JSONParser
from . models import approvals
from . serializers import approvalSerializers
import pickle
# from sklearn.externals
import joblib
import json
import numpy as np
from sklearn import preprocessing
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from .forms import approvalForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

class approvalView(viewsets.ModelViewSet):
    queryset = approvals.objects.all()
    serializer_class = approvalSerializers

def ohevalue(df):
    ohe_col = joblib.load('myapi/allcol.pkl')
    cat_columns = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']
    df_processed = pd.get_dummies(df, columns=cat_columns)
    newdict = {}
    for i in ohe_col:
        if i in df_processed.columns:
            newdict[i] = df_processed[i].values
        else:
            newdict[i] = 0
    newdf = pd.DataFrame(newdict)
    return newdf

def setGpu():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Restrict TensorFlow to only use the fourth GPU
            tf.config.experimental.set_visible_devices(gpus[0], 'GPU')

            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)

def approveReject(unit):
    try:
        setGpu()
        model = tf.keras.models.load_model('myapi/customer_loan.h5')
        scalers = joblib.load("myapi/scaler.pkl")
        unit['LoanAmount'] = int(unit['LoanAmount'])/1000
        # print(unit)
        X = scalers.transform(unit)
        y_pred = model.predict(X)
        y_pred = (y_pred > 0.58)
        newdf = pd.DataFrame(y_pred, columns=['Status'])
        newdf = newdf.replace({True: 'Approved', False: 'Rejected'})
        return 'Your status is {}'.format(newdf)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

def cxcontact(request):
    postFlag = 0
    if request.method == 'POST':
        #approvalForm is defined in forms.py
        form = approvalForm(request.POST)
        if form.is_valid():
            ob = approvals()

            Firstname = form.cleaned_data['firstname']
            Lastname = form.cleaned_data['lastname']
            Dependants = form.cleaned_data['Dependants']
            ApplicantIncome = form.cleaned_data['ApplicantIncome']
            CoapplicantIncome = form.cleaned_data['CoapplicantIncome']
            LoanAmount = form.cleaned_data['LoanAmount']
            Loan_Amount_Term = form.cleaned_data['Loan_Amount_Term']
            Credit_History = form.cleaned_data['Credit_History']
            Gender = form.cleaned_data['Gender']
            Married = form.cleaned_data['Married']
            Education = form.cleaned_data['Education']
            Self_Employed = form.cleaned_data['Self_Employed']
            Property_Area = form.cleaned_data['Property_Area']
            myDict = (request.POST).dict()
            df = pd.DataFrame(myDict, index=[0])
            answer = approveReject(ohevalue(df))
            check = answer.split()[-1]
            if check == "Rejected":
                postFlag = 2
            else:
                postFlag = 1
                ob.first_name = Firstname
                ob.last_name = Lastname
                ob.dependants = Dependants
                ob.applicant_income = ApplicantIncome
                ob.coapplicant_income = CoapplicantIncome
                ob.loan_amount = LoanAmount
                ob.loan_term = Loan_Amount_Term
                ob.credit_history = Credit_History
                ob.gender = Gender
                ob.married = Married
                ob.graduate_education = Education
                ob.self_employed = Self_Employed
                ob.property_choices = Property_Area
                ob.save()

            messages.success(request, 'Application Status: {}'.format(answer))

    form = approvalForm()
    return render(request, 'myform/cxform.html', {'form': form, 'postFlag':postFlag})

def calculator(request):
    return render(request, 'myform/calc.html')

def signup(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'myform/signup.html', {'form': form})

    # if request.method=="POST":
    #     fname = request.POST['fname']
    #     lname = request.POST['lname']
    #     uname = request.POST['uname']
    #     Email1 = request.POST['Email1']
    #     Password1 = request.POST['Password1']
        
    #     if len(uname)<10:
    #         messages.error(request, " Your user name must be under 10 characters")
    #         return render(request, 'myform/signup.html')

    #     if not uname.isalnum():
    #         messages.error(request, " User name should only contain letters and numbers")
    #         return render(request, 'myform/signup.html')
        
    #     # Create the user
    #     myuser = User.objects.create_user(uname, Email1, Password1)
    #     myuser.first_name= fname
    #     myuser.last_name= lname
    #     myuser.save()
    #     messages.success(request, " Your id has been successfully created")
    #     return render(request, 'myform/signup.html')
    # else:
    #     return HttpResponse("404 - Not found")

def login(request):
    return render(request, 'myform/login.html')

    # if request.method=="POST":
    #     uname2 = request.POST['uname2']
    #     Password2 = request.POST['Password2']

    #     user=authenticate(username= uname2, password= Password2)
    #     if user is not None:
    #         login(request, user)
    #         messages.success(request, "Successfully Logged In")
    #         return render(request, 'myform/login.html')
    #     else:
    #         messages.error(request, "Invalid credentials! Please try again")
    #         return render(request, 'myform/login.html')
    # return HttpResponse("404- Not found")

# def logout(request): 

#     messages.success(request, "Successfully Logged Out")
#     return render(request, 'myform/cxform.html')

def index(request):
    return render(request, 'myform/index2.html')

