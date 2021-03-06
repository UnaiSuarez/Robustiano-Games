"""tiendaVideojuegos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from collections import namedtuple
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include

from tienda.views import AmigosUsuarioListView, ComentariosView, EliminarVideojuego, MensajesView, ModificarVideojuego, UsuariosListView, ValoracionView, VideojuegoListView, VideojuegosListView, VideojuegosUsuarioListView, AñadirAmigo, AñadirSaldo2, crear_tarjeta, crear_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', VideojuegosListView.as_view(), name='inicio'),
    path('<str:pk>', VideojuegosListView.as_view(), name='inicio'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('misJuegos/',VideojuegosUsuarioListView.as_view(), name ='juegosUsuario'),
    path('videojuego/<str:pk>',VideojuegoListView, name ='videojuego'),
    path('misAmigos/', AmigosUsuarioListView.as_view(), name ='misAmigos'),
    path('añadirSaldo/', AñadirSaldo2, name ='añadirSaldo'),
    path('registro/', crear_usuario, name='registro'),
    path('crearTarjeta/', crear_tarjeta, name ='crearTarjeta'),
    path('editarVideojuego/<str:pk>', ModificarVideojuego.as_view(), name='editarVideojuego'),
    path('eliminarVideojuego/<str:pk>', EliminarVideojuego.as_view(), name='eliminarVideojuego'),
    path('usuarios/', UsuariosListView.as_view(), name='usuarios'),
    path('usuario/<str:pk>', AñadirAmigo, name='usuario'),
    path('mensaje/<str:pk>', MensajesView, name='mensajes'),
    path('comentario/<str:pk>', ComentariosView, name='comentarios'),
    path('valoracion/<str:pk>', ValoracionView, name='valoracion'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)