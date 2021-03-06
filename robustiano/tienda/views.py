from contextlib import nullcontext
from django.shortcuts import redirect, render
from django.conf import settings
import os
from django.views import generic
from tienda.forms import ComentarioForm, ContactForm, CrearTarjetaForm, EnviarMensajeForm, UserForm, ValoracionForm, AñadirSaldoForm
from tienda.models import  Comentario, Genre, Mensaje, TarjetaRegalo, User, Valoracion, Videojuego
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required


# Create your views here.
def _datos():
    return {'genero': [l.name for l  in Genre.objects.all()]}

datos = _datos()



class VideojuegosListView(generic.ListView):
    '''
    Vista genérica para nuestro listado de autores
    '''
    model = Videojuego
    paginate_by = 8
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super(VideojuegosListView, self).get_context_data(**kwargs)
        context['juegos'] = Videojuego.objects.all()
        return context
    
    def get_queryset(self):
        busqueda = self.request.GET.get('q')
        if busqueda:
            videojuegos = Videojuego.objects.filter(title__icontains=busqueda)
        else:
            pk = self.request.GET.get('pk')
            if pk:
                videojuegos = Videojuego.objects.filter(genre__name=pk)
            else:
                videojuegos = Videojuego.objects.all()
                
        return videojuegos
            
    
    
def VideojuegoListView(request, pk):
    if request.method == 'GET':
        form = ComentarioForm()
        formv = ValoracionForm()
        videojuego = Videojuego.objects.filter(title = pk)
        valoraciones = Valoracion.objects.filter(videojuego = pk)
        val = 0
        for valoracion in valoraciones:
            val = val + valoracion.valoracion
        if len(valoraciones) != 0:
            val = val / len(valoraciones)
        else:
            val = 0
        
        for videoj in videojuego:
            comentarios = Comentario.objects.filter(videojuego = videoj)
        datos.update({'videojuego_list': videojuego, 'pk':pk, 'comentarios':comentarios, 'form':form, 'formv':formv, 'val':val})
    elif request.method == 'POST':
        usuario = request.user
        if usuario.is_anonymous:
            messages.add_message(request, messages.SUCCESS,'Usted no ha iniciado sesion')
            return redirect('/accounts/login')
        else:
            videojuegos = Videojuego.objects.filter(title = pk)
            for videojuego in videojuegos:
                if videojuego in usuario.juegosComprados.all():
                   messages.add_message(request, messages.SUCCESS,'Usted ya tiene comprado este videojuego.')
                else:
                    if usuario.saldo >= videojuego.precio:
                        usuario.saldo = usuario.saldo - videojuego.precio
                        usuario.juegosComprados.add(videojuego)
                        messages.add_message(request, messages.SUCCESS,'Juego comprado.')
                        usuario.save()
                    else:
                     messages.add_message(request, messages.SUCCESS,'No tienes dinero suficiente.')
        
            
        return redirect('/')
    
    return render(request, 'videojuego.html', context=datos)
    
    
    
class VideojuegosUsuarioListView(LoginRequiredMixin, generic.ListView):
    '''
    Vista genérica para nuestro listado de autores
    '''
    model = User
    paginate_by = 6
    template_name = 'juegosDelUsuario.html'
    
class AmigosUsuarioListView(LoginRequiredMixin, generic.ListView):
    '''
    Vista genérica para nuestro listado de autores
    '''
    model = User
    paginate_by = 6
    template_name = 'amigos.html'

# en este momento no funcional, no lo borro ya que es otra posibilidad
# class AñadirSaldo(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
#     model = User
#     fields = ['saldo']
#     template_name = 'añadirSaldo.html'
#     success_url = '/'
#     success_message = " se ha añadido el saldo correctamente"
#     def get_initial(self):
#         return {'saldo': ''}
    
#     def get_object(self):
#         usuario  = super().get_object()
#         self.saldoanterior = usuario.saldo
#         return usuario

#     def form_valid(self, form):
#         saldoanterior = self.saldoanterior
#         saldoanterior = saldoanterior
#         nuevo = int(form.cleaned_data['saldo'])
#         form.instance.saldo = saldoanterior + nuevo
#         return super().form_valid(form)
    
#     def get_context_data(self, **kwargs):
#         context = super(AñadirSaldo, self).get_context_data(**kwargs)
#         return context

def crear_usuario(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            password = form.cleaned_data['password']
            passwordCi = make_password(password)
            form.instance.password = passwordCi
            form.instance.saldo = 0
            form.save()
            messages.add_message(request, messages.SUCCESS,'Usuario creado.')
            return redirect('/')
    else:
        form = UserForm()
    datos.update({'form': UserForm()})
    return render(request, 'registrarUsuario.html', context=datos)

class EliminarVideojuego(SuccessMessageMixin, LoginRequiredMixin, generic.DeleteView):
    model = Videojuego
    success_url = '/'
    success_message = "El Videojuego se ha borrado correctamente"
    template_name = 'viedojuego_confirmar_borrado.html'
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EliminarVideojuego, self).delete(request, *args, **kwargs)
    
class ModificarVideojuego(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Videojuego
    fields = '__all__'
    template_name = 'modificar_videojuego.html'
    success_url = '/'
    success_message = "%(title)s se ha modificado correctamente"

@login_required
def crear_tarjeta(request):
    if request.method == 'POST':
        form = CrearTarjetaForm(request.POST)
        if form.is_valid():
            form.instance.codigo = form.cleaned_data['codigo']
            form.instance.saldo = form.cleaned_data['saldo']
            form.instance.habilitado = True
            form.save()
            messages.add_message(request, messages.SUCCESS,'Tarjeta regalo creado.')
            return redirect('/')
    else:
        form = CrearTarjetaForm()
    datos.update({'form': CrearTarjetaForm()})
    return render(request, 'crearTarjetaregalo.html', context= datos)

@login_required
def AñadirSaldo2(request):
    añadirSaldo = False
    usuario = request.user
    if request.method == 'POST':
        form = AñadirSaldoForm(request.POST)
        if form.is_valid():
            codigos = TarjetaRegalo.objects.all()
            for codigo in codigos:
                if codigo.codigo == form.cleaned_data['codigo']:
                    if codigo.habilitado == True:
                        añadirSaldo = True
                        break
            if añadirSaldo:
                saldoAntiguo = usuario.saldo
                saldoNuevo = saldoAntiguo + codigo.saldo
                usuario.saldo = saldoNuevo
                usuario.save()
                codigo.habilitado = False
                codigo.save()
                messages.add_message(request, messages.SUCCESS,'Se ha añadido saldo a su cuenta')
                return redirect('/')
            else:
                messages.add_message(request, messages.SUCCESS,'El codigo introducido ya ha sido introducido o no existe')
    else:
        form = AñadirSaldoForm()
    datos.update({'form': AñadirSaldoForm()})
    return render(request,'añadirSaldo2.html', context=datos)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        messages.add_message(request, messages.SUCCESS,'Se ha enviado su mensaje')
        return redirect('/')
    else:
        form = ContactForm()
    datos.update({'form': ContactForm()})
    return render(request,'contact.html', context=datos)


class UsuariosListView(generic.ListView):
    '''
    Vista genérica para nuestro listado de autores
    '''
    model = User
    paginate_by = 10
    template_name = 'usuarios.html'
    
    def get_queryset(self):
        busqueda = self.request.GET.get('q')
        if busqueda:
            usuarios = User.objects.filter(username__icontains=busqueda)
        else:
            usuarios = User.objects.all()
        return usuarios


def AñadirAmigo(request, pk):
    if request.method == 'GET':
        usuario = request.user
        amigoNuevo = User.objects.filter(username = pk)
        datos.update({'usuario': amigoNuevo, 'pk':pk, 'usuarioActual':usuario})
    elif request.method == 'POST':
        usuario = request.user
        if usuario.is_anonymous:
            messages.add_message(request, messages.SUCCESS,'Usted no ha iniciado sesion')
            return redirect('/accounts/login')
        else:
            amigoNuevo = User.objects.filter(username = pk)
            for amigoN in amigoNuevo:
                if amigoN in usuario.amigos.all():
                   messages.add_message(request, messages.SUCCESS,'Usted ya tiene agregada a esta persona.')
                else:
                    amigoN.amigos.add(usuario)
                    usuario.amigos.add(amigoN)
                    messages.add_message(request, messages.SUCCESS,'Amigo añadido.')
                    usuario.save()
                    amigoN.save()
        
            
        return redirect('/')
    
    return render(request, 'agregarAmigo.html', context=datos)

@login_required
def MensajesView(request, pk):
    if request.method == 'GET':
        form = EnviarMensajeForm()
        emisor = User.objects.filter(username = pk)
        # mensajes = Mensaje.objects.filter(receptor = amigoMen)
        for amigoMen in emisor:
            mensajesEnviados = Mensaje.objects.filter(receptor = amigoMen, emisor = request.user)
            mensajesRecibidos = Mensaje.objects.filter(emisor = amigoMen, receptor = request.user)
            for mensajeEnviado in mensajesEnviados:
                mensajeEnviado.visto = True
                mensajeEnviado.save()
        mensajes = mensajesRecibidos.union(mensajesEnviados)
        datos.update({'emisor': emisor, 'pk':pk, 'mensajes':mensajes, 'receptor': request.user, 'form':form})
    elif request.method == 'POST':
        usuario = request.user
        if usuario.is_anonymous:
            messages.add_message(request, messages.SUCCESS,'Usted no ha iniciado sesion')
            return redirect('/accounts/login')
        else:
            emisor = User.objects.filter(username = pk)
            form = EnviarMensajeForm(request.POST)
            if form.is_valid():
                mensaje = Mensaje()
                mensaje.mensaje = form.cleaned_data['mensaje']
                mensaje.receptor = usuario
                for amigoMen in emisor:
                    mensaje.emisor = amigoMen
                    cod = amigoMen
                mensaje.save()
                form.cleaned_data['mensaje'] = nullcontext
        
        return redirect('/mensaje/'+ pk)
    
    return render(request, 'mensajes.html', context=datos)


@login_required
def ComentariosView(request, pk):
    form = ComentarioForm()
    datos.update({'form': form, 'pk':pk})
    if request.method == 'POST':
        usuario = request.user
        if usuario.is_anonymous:
            messages.add_message(request, messages.SUCCESS,'Usted no ha iniciado sesion')
            return redirect('/accounts/login')
        else:
            form = ComentarioForm(request.POST)
            if form.is_valid():  
                print('--------------------------------------------------------------')
                comentario = Comentario()
                comentario.comentario = form.cleaned_data['comentario']
                comentario.usuario = usuario
                videojuegos = Videojuego.objects.filter(title = pk)
                for videojuego in videojuegos:
                    comentario.videojuego = videojuego
                comentario.save()
                messages.add_message(request, messages.SUCCESS,'comentario guardado')
            
        return redirect('/videojuego/'+pk)
    return render(request, 'comentarios.html', context=datos)
        
@login_required
def ValoracionView(request, pk):
    form = ValoracionForm()
    datos.clear()
    datos.update({'formv': form, 'pk':pk})
    if request.method == 'POST':
        usuario = request.user
        if usuario.is_anonymous:
            messages.add_message(request, messages.SUCCESS,'Usted no ha iniciado sesion')
            return redirect('/accounts/login')
        else:
            form = ValoracionForm(request.POST)
            if form.is_valid():  
                print('--------------------------------------------------------------')
                valoracion = Valoracion()
                valoracion.valoracion = form.cleaned_data['valoracion']
                valoracion.usuario = usuario
                videojuegos = Videojuego.objects.filter(title = pk)
                for videojuego in videojuegos:
                    valoracion.videojuego = videojuego
                valoracion.save()
                messages.add_message(request, messages.SUCCESS,'valoracion guardada')
            
        return redirect('/videojuego/'+pk)
    return render(request, 'valoracion.html', context=datos)
        