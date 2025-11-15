from django.shortcuts import render, HttpResponsePermanentRedirect, get_object_or_404

# Create your views here

# Relative import of forms
from.models import vehiculo
from .forms import vehiculoForm

def home_view(request):
    return render(request, 'vehiclesapp/home.html')

def create_view(request):
    context = {}
    form = vehiculoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponsePermanentRedirect('/')

    context['form'] = form
    return render(request, 'vehiclesapp/create_view.html', context)
    
def list_view(request):
    context = {}
    context['dataset'] = vehiculo.objects.all()
    return render(request, 'vehiclesapp/list_view.html', context)

def update_view(request, id):
    context = {}

    obj = get_object_or_404(vehiculo, id=id)

    form = vehiculoForm(request.POST or None, instance=obj)
    
    if form.is_valid():
        form.save()
        return HttpResponsePermanentRedirect('/')
    
    context['form'] = form
    return render(request, 'vehiclesapp/update_view.html', context)

def delete_view(request, id):
    context = {}
    obj = get_object_or_404(vehiculo, id=id)
    if request.method == 'POST':
        obj.delete()
        return HttpResponsePermanentRedirect('/')
    
    context['object'] = obj
    return render(request, 'vehiclesapp/delete_view.html', context)
