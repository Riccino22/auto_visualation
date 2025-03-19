from django.shortcuts import render
import pandas as pd

def inicio(request):
    return render(request, 'index.html')

def saludo(request):
    if request.method == 'POST':
        return render(request, 'grettings.html', {
            'name': request.POST['nombre']
        })
        
def graphic(request):
    df = pd.read_csv(request.FILES['dataset'])
    return render(request, 'graphic.html')