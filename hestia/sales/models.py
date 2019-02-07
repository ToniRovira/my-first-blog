from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import datetime,date
import datetime
from django.core.exceptions import ValidationError

from django.urls import reverse

# Create your models here.
class Sala (models.Model):
    nom = models.CharField(max_length=200)
    capacitat = models.IntegerField(help_text="Màxim aforament")
    projector = models.BooleanField(default=False,verbose_name='Disposa de projector')
    PC = models.BooleanField(default=False,verbose_name='Disposa de PC')
    Wifi = models.BooleanField(default=False,verbose_name='Disposa de Wifi')
    Audio = models.BooleanField(default=False,verbose_name="Disposa d' audio")
    MicroTaula = models.BooleanField(default=False,verbose_name='Micro de taula')
    Microsensefils = models.BooleanField(default=False,verbose_name='Micro sense fils')
    Enregistraments= models.BooleanField(default=False,verbose_name='Pot fer enregistraments')
    Vídeoconferencia = models.BooleanField(default=False,verbose_name='Equip de videoconfrencia')
    PantallaLed = models.BooleanField(default=False,verbose_name='Disposa de monitor')

    FORMAT_STATUS = (
        ('t', 'Taller'),
        ('a', 'Auditori'),
        ('r', 'Reunió'),
    )

    status = models.CharField(
        max_length=1,
        choices=FORMAT_STATUS,
        blank=False,
        default='r',
        help_text='Disposició de la sala')
    
    
    def __str__(self):    
        return self.nom
   
    
    def get_absolute_url(self):
        return reverse('sala-detail', args=[str(self.id)])

import uuid # Per les instancies de peticions uniques

class Peticio(models.Model):
    """
    Model que representa una petició 
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID únic per aquesta petició")
    data_peticio = models.DateTimeField(null=False, blank=True)
    peticionari = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    assistents = models.IntegerField(help_text="Nombre d'assistents",default=0)
    data_inici = models.DateTimeField(null=False, blank=True)
    data_final = models.DateTimeField(null=False, blank=True)
    motiu = models.CharField(max_length=200,default='')
    
    FORMAT_STATUS = (
        ('t', 'Taller'),
        ('a', 'Auditori'),
        ('r', 'Reunió'),
    )

    status = models.CharField(
        max_length=1,
        choices=FORMAT_STATUS,
        blank=False,
        default='r',
        help_text='Disposició de la sala')
    
    

    class Meta:
        ordering = ["data_inici"]
        
    def __str__(self):
        return '%s (%s)' % (self.id,self.peticionari)

    def get_absolute_url(self):
        return reverse('peticio-detail', args=[str(self.id)])



class Concesio(models.Model):
    """
    Model que representa una concesió
    """
    concesionari = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    peticio_servida = models.ForeignKey(Peticio, on_delete=models.SET_NULL, null=True)
    sala_donada = models.ForeignKey(Sala, on_delete=models.SET_NULL, null=True)
    data_concesio = models.DateTimeField(null=False, blank=True)
    start_time = models.DateTimeField(default=datetime.datetime.now(),verbose_name='Data inici')
    end_time = models.DateTimeField(default=datetime.datetime.now(),verbose_name='Data final')

    class Meta:
        ordering = ["data_concesio"]
        
    def __str__(self):
        return '%s (%s,%s)' % (self.id,self.concesionari,self.data_concesio)

    def get_absolute_url(self):
        return reverse('concesio-detail', args=[str(self.id)])

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:    #edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end): #innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end: #outter limits
            overlap = True
        return overlap


    def clean(self):
        if self.end_time < self.start_time:
            raise ValidationError("Cal que l'inici sigui abans que el final")
        concedits = Concesio.objects.filter(sala_donada=self.sala_donada)
        if concedits.exists():
            for concedit in concedits:
                if self.check_overlap(concedit.start_time, concedit.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        'Hi ha conflicte amb una altra concessió: ' + str(concedit.id) + ', ' + str(
                            concedit.start_time) + '-' + str(concedit.end_time))
        
    @property
    def get_html_url(self):
        url = reverse('concesio-detail', args=(self.id,))
        return f'<a href="{url}"> {self.sala_donada} </a>'
