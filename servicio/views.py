from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import colacionForm
from .models import CasinoColacion, Estado, Opciones, Usuarios, TipoUsuario
from django.contrib import messages 
from datetime import datetime, timedelta
from django.utils import timezone
from collections import defaultdict



#login
def home(request):
    return render(request,'login/login.html')

# PRINCIPAL
def principal(request):
    user_data = request.session.get('user_data', {})  # Obtener los datos del usuario de la sesión
    return render(request, 'principal.html', {'user_data': user_data})

# REGISTRAR USUARIO
def registrarusuario(request):
    
    if request.method == 'GET':
        return render(request,'login/registrar.html',
                {'form' : UserCreationForm
                 })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                       password=request.POST['password1'])
                user.save()
                
                return redirect ('home')
            except IntegrityError:
               return render(request,'login/registrar.html',
                {'form' : UserCreationForm,
                "error" : 'Usuario Existente' 
                 })
               
        else: 
            return render(request,'login/registrar.html',
                {'form' : UserCreationForm,
                "error" : 'Password no coinciden' 
                  })
    
#CERRAR SESION
def cerrarsession(request):
    logout(request)
    return redirect('home')

#INICIO SESION
def iniciosession(request):
    if request.method == 'GET':
        return render(request,'login/login.html')
    else:
        user = authenticate(request, username=request.POST['username'] , password=request.POST['password'])
        if user is None:        
            return render(request,'login/login.html',{
                          'error': 'Rut o Contraseña incorrecto'})
        else:
            login(request, user)
            request.session['user_data'] = {
                'username': user.username,
                'email': user.email,
                # Añade más campos según sea necesario
            }
            return redirect('principal')
            
#AGREGAR MENU
def agregarmenu(request):
    if request.method == 'GET':
        return redirect('menu_lista')
    else:
        titulo = request.POST.get('titulo')
        fechaSer = request.POST.get('fechaServicio')
        estado = request.POST.get('estado')
        opcion = request.POST.get('opcion')
        desc = request.POST.get('descripcion')
        
        # Validar si el título ya existe
        if CasinoColacion.objects.filter(titulo=titulo, fecha_servicio=fechaSer).exists():
            messages.error(request, "El título ya existe.")
            return redirect('menu_lista')

        # Validar si hay opciones repetidas con las mismas fechas
        if CasinoColacion.objects.filter(id_opciones_id=opcion, fecha_servicio=fechaSer).exists():
            messages.error(request, "Ya existe una opción con la misma fecha.")
            return redirect('menu_lista')
        
        
        registro = CasinoColacion(titulo = titulo ,descripcion = desc, fecha_servicio = fechaSer, 
                                  id_estado_id = estado, id_opciones_id = opcion)
        registro.save()
        return redirect('menu_lista')

#LISTA DEL MENU    
def menu_lista(request):
    consulta = request.GET.get('q')
    if consulta:
        menu = CasinoColacion.objects.filter(titulo__icontains=consulta).order_by('id')
    else:
        menu = CasinoColacion.objects.all().order_by('id') 
    
    estado = Estado.objects.all().order_by('id')
    opcion = Opciones.objects.all().order_by('id')
    context = {
        'menus': menu,
        'query': consulta,
        'estados': estado,
        'opciones': opcion
    }
    return render(request, 'admin/agregarmenu.html', context)

def usuarios(request):
    if request.method == 'GET':
        return redirect('usuarioslistas')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                rut = request.POST.get('username')
                print("AQUI ESTA EL RUT: ",  rut)
                user = User.objects.create_user(username=request.POST['username'],
                       password=request.POST['password1'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                user.save()
                            
                usuario = Usuarios.objects.create(rut = request.POST['username'], nombre = request.POST['first_name'], 
                                                  apellido=request.POST['last_name'], activo = True , id_user=user)
                print(usuario)
                
                usuario.save()
                
                return redirect ('usuarioslistas')
            except IntegrityError:
               return render(request,'adminCliente/usuarios.html',
                {'form' : UserCreationForm,
                "error" : 'Usuario Existente' 
                 })
               
        else: 
            return render(request,'adminCliente/usuarios.html',
                {'form' : UserCreationForm,
                "error" : 'Password no coinciden' 
                  })
    
def usuarioslistas(request):
    consulta = request.GET.get('q')
    if consulta:
        usuarios = Usuarios.objects.filter(rut__icontains=consulta).order_by('rut')
    else:
        usuarios = Usuarios.objects.all().order_by('rut') 
    
    tipousuario = TipoUsuario.objects.all().order_by('id')
    
    context = {
        'usuarios': usuarios,
        'query': consulta,
        'tipousuario': tipousuario,
    }
    return render(request, 'adminCliente/usuarios.html', context)

def programarmenu(request):
    return render(request,'usuario/programarmenu.html')

# CREACION METODO SELECCION SEMANA ACTIVA
def diaDeSemana():
    # Obtener la fecha actual
    fechaActual = timezone.now().date()
    # Calcular el inicio y fin de la semana (lunes a viernes)
    inicioSem = fechaActual - timedelta(days=fechaActual.weekday())
    finSem = inicioSem + timedelta(days=4)
    return inicioSem, finSem

def programarmenu(request):
    iniSem, finSem = diaDeSemana()
    programacion = CasinoColacion.objects.filter(fecha_servicio__range=[iniSem, finSem], id_estado = 1)
    
    # Creamos un diccionario para agrupar por fecha
    programacion_dict = defaultdict(list)
    for registro in programacion:
        programacion_dict[registro.fecha_servicio].append(registro)
    
    # Convertimos el diccionario a una lista de tuplas para ordenarlos por fecha
    programacion_ordenada = sorted(programacion_dict.items())
    
    
    return render(request, 'usuario/programarmenu.html', {'programacion_ordenada': programacion_ordenada})

