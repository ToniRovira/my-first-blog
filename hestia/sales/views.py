from django.shortcuts import render
from django.http import HttpResponse
import datetime
import pyodbc # per inseriri a msqlserver i enviar correu

from django.utils import timezone
from django.shortcuts import redirect
from django.shortcuts import get_list_or_404, get_object_or_404

# Create your views here.

from .models import Sala, Peticio, Concesio
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PeticioForm,ConcesioForm


def index(request):
    """
    Funció vista inicio del lloc.   
    """
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    # Genera contadores de algunos de los objetos principales
    num_sales=Sala.objects.all().count()
    num_peticions=Peticio.objects.all().count()
    #num_peticions_pendents = 0
    peticions_pendents = []
    # miro cada peticio, si està servida no la compto
    for pp in Peticio.objects.all():
        cc = pp.concesio_set.all()
        if len(cc) == 0:
            #num_peticions_pendents = num_peticions_pendents +1
            peticions_pendents.append(pp)
    num_peticions_pendents = len(peticions_pendents)
    num_concessions=Concesio.objects.all().count()
   
    num_peticions_per_user=0
    llistat_peticions_per_user=[]
    if request.user.is_authenticated:
        num_peticions_per_user=Peticio.objects.filter(peticionari=request.user).count()
        llistat_peticions_per_user = Peticio.objects.filter(peticionari=request.user)
    
  
    '''
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # El 'all()' esta implícito por defecto.
    '''
    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context={'num_sales':num_sales,'num_peticions':num_peticions,
                 'num_concessions':num_concessions,'num_peticions_pendents':num_peticions_pendents,
                 'num_peticions_per_user':num_peticions_per_user,
                 'llistat_peticions_per_user':llistat_peticions_per_user,
                 'peticions_pendents':peticions_pendents,'num_visits':num_visits,
                 }
    )

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class PeticioListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Peticio
           
class PeticioDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Peticio

class ConcesioDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Concesio
    
class ConcesioListView(generic.ListView):
    model = Concesio


def enviar_correu_peticio( peticio, cuser):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.136.193.190;DATABASE=de112;UID=test;PWD=testtest')
    cursor = cnxn.cursor()
    vincle = "http://10.136.193.168:8000/sales/peticio/"+str(peticio)  
    text = "INSERT INTO perenviar(per,subject,body) VALUES ('"
    text = text +str(cuser)+ "','prova des de  django','"
    text = text + vincle + "')"
    cursor.execute(text)
    cnxn.commit()
    cursor.close()
    cnxn.close()
   

def enviar_correu_concesio( concesio, cuser):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.136.193.190;DATABASE=de112;UID=test;PWD=testtest')
    cursor = cnxn.cursor()
    vincle = "http://10.136.193.168:8000/sales/concesio/"+str(concesio)  
    text = "INSERT INTO perenviar(per,subject,body) VALUES ('"
    text = text +str(cuser)+ "','prova des de  django','"
    text = text + vincle + "')"
    cursor.execute(text)
    cnxn.commit()
    cursor.close()
    cnxn.close()
   

def peticio_new(request):
    if request.method == "POST":
        form = PeticioForm(request.POST)
        if form.is_valid():
            peticio = form.save(commit=False)
            peticio.peticionari = request.user
            peticio.data_peticio = timezone.now()
            peticio.save()
            # provo d'enviar un correu aqui
            #enviar_correu(str(peticio.pk),str(request.user.email))
            # aquesta per enviar resposta al peticionari en fer l'assignació
            enviar_correu_peticio(str(peticio.pk),"rosa.alabart@gencat.cat")
            # fi de correu
            return redirect('peticio-detail', pk=peticio.pk)
    else:
        form = PeticioForm()
    return render(request, 'sales/peticio_edit.html', {'form': form})


def peticio_servir(request, pk):
    peticio = get_object_or_404(Peticio, pk=pk)
    if request.method == "POST":
        form = ConcesioForm(request.POST)
        if form.is_valid():
            concesio = form.save(commit=False)
            concesio.concesionari = request.user
            concesio.peticio_servida = peticio
            concesio.data_concesio = timezone.now()
            concesio.save()
            # no va, el correu cal enviar-lo al de peticio.peticionari
            enviar_correu_concesio(str(concesio.pk),str(request.user.email))
            return redirect('concesio-detail', pk=concesio.pk)
        else:
            form = ConcesioForm(request.POST)
            return render(request, 'sales/peticio_servir.html', {'form': form})
    else:
        #form = ConcesioForm(request.POST) # antic
        form = ConcesioForm(request.POST)
        #https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/
        #Providing initial values ?
        return render(request, 'sales/peticio_servir.html', {'form': form})



'''
            cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.136.193.190;DATABASE=de112;UID=test;PWD=testtest')
            cursor = cnxn.cursor()
            vincle = "http://127.0.0.1:8000/sales/peticio/"+str(peticio.pk)
            text = "INSERT INTO perenviar(per,subject,body) VALUES ('antoni.rovira@gencat.cat','prova des de  django','"
            text = text + vincle + "')"
            cursor.execute(text)
            cnxn.commit()
            cursor.close()
            cnxn.close()
'''
