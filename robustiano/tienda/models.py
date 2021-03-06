from cgitb import text
from enum import Enum
from os import name, truncate
from tokenize import blank_re
from django.db import models
from django.db.models.fields import CharField
from django.urls import reverse
from datetime import date, datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.

    
class Lenguaje(models.Model):
    '''
    Lenguaje de los videojuegos
    '''
    name = models.CharField(primary_key = True, max_length=100, null=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Idioma'
        verbose_name_plural = 'Idiomas'

class Genre(models.Model):
    name = models.CharField("Genero",primary_key = True, max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genero'
        verbose_name_plural = 'Generos'

class ImagenVideojuego(models.Model):
    name= models.CharField(primary_key = True,max_length=500)
    imagen = models.FileField(upload_to='images/logos', blank=True,)

class VideoVideojuego(models.Model):
    name= models.CharField(primary_key = True,max_length=500)
    video = models.FileField(upload_to='videos/juegos', blank=True)


class Videojuego(models.Model):
    title = models.CharField(primary_key = True, max_length=250)
    summary = models.TextField(blank=True)
    precio = models.DecimalField(max_length=20, blank=True, decimal_places=2, max_digits=5)
    fecha = models.DateField(auto_now=True, null=True, help_text='Fecha de publicacion')
    imagen = models.ManyToManyField(ImagenVideojuego, blank=True, null=True)
    video = models.ManyToManyField(VideoVideojuego, blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    lenguaje = models.ManyToManyField(Lenguaje)

    def __str__(self):
        return self.title

    def muestra_genero(self):
        '''Muestra genero para admin'''
        return ', '.join([gen.name for gen in self.genre.all()[:3]])
    muestra_genero.short_description = 'Genero'

    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de videojuego
        """
        return reverse('videogame-detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Videojuego'
        verbose_name_plural = 'Videojuegos'    
        
class User(AbstractUser):
    saldo = models.DecimalField(max_length=20, blank=True, decimal_places=2, max_digits=1000)
    juegosComprados = models.ManyToManyField(Videojuego, null=True, blank=True)  
    amigos = models.ManyToManyField('self', null=True, blank=True)  
    imagen = models.ImageField(upload_to='images/avatares', blank=True)


class TarjetaRegalo(models.Model):
    saldo = models.DecimalField(max_length=5, blank=False, decimal_places=2, max_digits=100)
    codigo = models.CharField(max_length=10000, blank=False, primary_key=True)
    habilitado = models.BooleanField(blank=False, null=False)

class Mensaje(models.Model):
    codigo = models.AutoField(primary_key=True)
    mensaje = models.TextField(blank=False)
    visto = models.BooleanField(default=False)
    fecha = models.DateField(default=datetime.now)
    emisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receptor')
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emisor')

class tipoDesarrolladora(Enum):
    I = 'indie'
    E = 'empresa'

class Desarrolladora(models.Model):
    nombre = models.OneToOneField(User, on_delete=models.CASCADE)
    contacto = models.TextField(blank=True)
    tipo = models.CharField(max_length=2, choices=[(tag, tag.value) for tag in tipoDesarrolladora])

class Comentario(models.Model):
    codigo = models.AutoField(primary_key=True)
    comentario = models.TextField(blank=False)
    fecha = models.DateField(default=datetime.now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)

class Valoracion(models.Model):
    codigo = models.AutoField(primary_key=True)
    valoracion = models.IntegerField(blank=False, max_length=5)
    fecha = models.DateField(default=datetime.now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)

class DLC(models.Model):
    codigo = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    summary = models.TextField(blank=True)
    precio = models.DecimalField(max_length=20, blank=True, decimal_places=2, max_digits=5, default=0)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)