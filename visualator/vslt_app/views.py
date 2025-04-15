from django.shortcuts import render, redirect
import pandas as pd
from . import llm_tools as llm
# deepseek-r1-distill-llama-70b
import random
import string
import os
import json
from django.http import JsonResponse, HttpResponse
import csv
from datetime import datetime
from .models import CSVData
from django.contrib import messages
from .models import CSVData


def generate_filename(longitud=20):
    caracteres = string.ascii_letters + string.digits  # Letras mayúsculas, minúsculas y números
    return ''.join(random.choices(caracteres, k=longitud))

def get_data(request):
    # API test
    # Send to response a pandas dataframe in json format
    title = request.GET.get('title')
    csv_data = CSVData.objects.get(title=title)
    data = csv_data.data_json
    df = pd.DataFrame(json.loads(data))
    table_content = df.sample(20).to_dict(orient="records")
    llm_response = llm.generate_response(title=title, table_content=table_content, user_descrption=csv_data.description)
    print(llm_response)
    return JsonResponse({
        'data': json.loads(data),
        'suggested_graphics': json.loads(llm_response.replace('```json', '').replace('```', ''))
    }, safe=False)


def inicio(request):
    return render(request, 'index.html')

def saludo(request):
    if request.method == 'POST':
        return render(request, 'grettings.html', {
            'name': request.POST['nombre']
        })
        
def graphic(request):

    filename = f'{generate_filename()}.csv'
    df = pd.read_csv(request.FILES['dataset'])
    csv_data = CSVData(
        title=filename,
        data_json=df.to_json(orient='records'),
        description=request.POST['description']
    )
    csv_data.save()
    
    # with open(request.FILES['dataset'].file.name) as file:
    #    print(file.read().split('\n')[2])
    return render(request, 'graphic.html', {
        'filename': filename,
        #'llm_response': json.loads(llm_response.replace('```json', '').replace('```', ''))
    })

def upload_csv_to_db(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        # Check if file is CSV
        if not csv_file.name.endswith('.csv'):
            return HttpResponse("Please upload a CSV file", status=400)
            
        try:
            # Read the CSV file using pandas
            df = pd.read_csv(csv_file)
            
            # Create a new CSVData instance
            csv_data = CSVData(
                title=request.POST.get('title', csv_file.name),
                file_name=csv_file.name,
                data_json=json.loads(df.to_json(orient='records'))
            )
            
            # Save to database
            csv_data.save()
            
            return HttpResponse(f"CSV file '{csv_file.name}' successfully saved to database with ID {csv_data.id}")
            
        except Exception as e:
            return HttpResponse(f"Error processing the CSV file: {str(e)}", status=500)
    
    # If GET request, show upload form
    return render(request, 'upload_csv.html')