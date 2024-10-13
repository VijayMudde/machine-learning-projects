from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_protect

import joblib
import numpy as np
import pandas as pd

from .models import diabetes_prediction

# Load the model and scaler
model = joblib.load('knn_model.joblib')
scaler = joblib.load('knn_scaler.joblib')

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        capitalized_username = request.user.username.capitalize()
        return render(request, 'index.html', {'username': capitalized_username})
    else:
        return render(request, 'home.html')


def predict(request):
    return render(request, 'predict.html')

def contact(request):
    return render(request,'contact.html')

def about_us(request):
    return render(request,'about_us.html')

def services(request):
    return render(request,'services.html')

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def prediction(request):
    if request.method == 'GET':
        try:
            # Collect input data from the request
            v1 = request.GET.get('pregnancies')
            v2 = request.GET.get('glucose')
            v3 = request.GET.get('blood_pressure')
            v4 = request.GET.get('skin_thickness')
            v5 = request.GET.get('insulin')
            v6 = request.GET.get('bmi')
            v7 = request.GET.get('diabetes_pedigree_function')
            v8 = request.GET.get('age')

            # Check if any field is empty
            if not all([v1, v2, v3, v4, v5, v6, v7, v8]):
                messages.error(request, "All fields are required.")
                return redirect('home')

            # Convert input to float
            v1 = float(v1)
            v2 = float(v2)
            v3 = float(v3)
            v4 = float(v4)
            v5 = float(v5)
            v6 = float(v6)
            v7 = float(v7)
            v8 = float(v8)

            # Create a DataFrame with the input data
            data = pd.DataFrame({
                'Pregnancies': [v1],
                'Glucose': [v2],
                'BloodPressure': [v3],
                'SkinThickness': [v4],
                'Insulin': [v5],
                'BMI': [v6],
                'DiabetesPedigreeFunction': [v7],
                'Age': [v8]
            })

            # Scale the input data
            data = scaler.transform(data)

            # Make the prediction
            prediction = model.predict(data)
            result = prediction[0]

            # Save the data to the database
            diabetes_prediction.objects.create(
                pregnancies=v1,
                glucose=v2,
                blood_pressure=v3,
                skin_thickness=v4,
                insulin=v5,
                bmi=v6,
                diabetes_pedigree_function=v7,
                age=v8,
                prediction_result=result
            )
            
            return render(request, 'result.html', {'result': result})
        except Exception as e:
            return HttpResponse(f"Error: {e}")

    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                
                user.save()
                auth.login(request, user)  # Log in the user after registration
                capitalized_username = user.username.capitalize()
                return render(request, 'index.html', {'username': capitalized_username})
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            capitalized_username = user.username.capitalize()
            return render(request, 'index.html', {'username': capitalized_username})
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')
