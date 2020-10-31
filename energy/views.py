from django.http import JsonResponse
from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import User,energyMonthlyUsage
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
import os
import datetime
import pandas as pd
from google.cloud import bigquery

# variables
gcp_project = 'my-project-cloud-app'
bq_dataset = 'consumption'

credential_path = "my-project-cloud-app-b2076257f9d0.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# connections
client = bigquery.Client(project=gcp_project)
dataset_ref = client.dataset(bq_dataset)


# results to dataframe function
def gcp2df1(sql,client_id,year,month):
    query_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('limit', 'INTEGER', 100),
            bigquery.ScalarQueryParameter('client_id', 'INTEGER', client_id),
            bigquery.ScalarQueryParameter('year', 'INTEGER', year),
            bigquery.ScalarQueryParameter('month', 'INTEGER', month),
        ]
    )
    query = client.query(sql,job_config=query_config)

    results = query.result()
    energyMonthlyUsages=[]
    for f in results:
        print(f)
        energyMonthlyUsages.append( energyMonthlyUsage(f[0],f[2]))
    return energyMonthlyUsages


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created successfully')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request,'energy/register.html',{'form':form})


def customer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'energy/login.html',
                  context={'customer_login_form': AuthenticationForm()})


def customer_logout(request):
    logout(request)
    return render(request, 'energy/logout.html')


def home(request):
    return render(request,'energy/home.html')


def dashboard(request):
    return render(request, 'energy/dashboard.html')


def usage_data(request,year,month):
    login_user = User.objects.get(username=request.user)
    #print(login_user.username)
    client_id=login_user.username
    #year=2020
    #month=10
    #print("Year {}".format(year))

    query = """
        SELECT Date, Client_ID, sum(Usage),
        FROM `my-project-cloud-app.consumption.Consumption2` where Client_ID=@client_id and EXTRACT(YEAR FROM Date)= @year and EXTRACT(MONTH FROM Date)= @month
        group by Date, Client_ID 
        order by Date 
        LIMIT @limit
        """
    dataframe=gcp2df1(query,client_id,year,month)
    #print(type(dataframe.Date.tolist()))
    data = []
    labels = []
    total = 0
    for d in dataframe:
        labels.append(d.dayOfMonth)
        data.append(d.usage)
        total = total + d.usage
        total = round(total, 2)
        #print(f'Total consumption{total:.2f}')
    return JsonResponse(data={
        'labels':labels,
        'data': data,
        'total': total,
        'title':datetime.datetime(year,month,1).strftime("%B %Y")
    })






