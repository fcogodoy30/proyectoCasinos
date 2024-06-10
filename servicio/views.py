from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import CasinoColacion, Estado, Opciones, Usuarios, TipoUsuario, Programacion
from django.contrib import messages 
from datetime import datetime, timedelta
from django.utils import timezone
from collections import defaultdict
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json


#login

def home(request):
    return render(request,'login/login.html')

# PRINCIPAL
@login_required
def principal(request):
    user_data = request.session.get('user_data', {})
    current_date = datetime.now().date()  # Obtén la fecha actual
    return render(request, 'principal.html', {
        'user_data': user_data,
        'current_date': current_date,
    })
    
#CERRAR SESION
@login_required
def cerrarsession(request):
    logout(request)
    request.session.flush()
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
                'id' : user.id,
                'username': user.username,
                'email': user.email,
                # Añade más campos según sea necesario
            }
            return redirect('principal')


# Dentro tenemos el guardado del Usuario
@login_required
def usuarios(request):
    if request.method == 'GET':
        return redirect('usuarioslistas')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                with transaction.atomic(): # Lo utilizaremos para asegurar de haber alguna falla no haga ninguna ejecucion a las tablas
                    rut = request.POST.get('username')
                    password = request.POST.get('password1')
                    first_name = request.POST.get('first_name')
                    last_name = request.POST.get('last_name')
                    tipoUsu = request.POST.get('tipousuario')
                    
                    user = User.objects.create_user(username=rut, password=password, first_name=first_name, last_name=last_name)
                    user.save()
                    
                    # Obtener la instancia de TipoUsuario
                    tipo_usuario = get_object_or_404(TipoUsuario, pk=tipoUsu)
                                            
                    usuario = Usuarios.objects.create(rut = rut, nombre = first_name, apellido=last_name,  id_user=user, tipo_usuario = tipo_usuario)
                    usuario.save()
                    messages.error(request, f'El rut {rut} se ha registrado con exito')
                    return redirect ('usuarioslistas')
            except IntegrityError as e:
                messages.error(request, f'El rut {rut} ya se ecuentra registrado')
                return redirect('usuarioslistas')
            
            except Exception as e:
                messages.error(request, f"Ocurrió un error al guardar el usuario: {e}")
                return redirect('usuarioslistas')                
        else: 
            messages.error(request, 'Contraseña no coinciden')
            return redirect('usuarioslistas')

@login_required
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
        'messages': messages.get_messages(request),
    }
    return render(request, 'adminCliente/usuarios.html', context)

# CREACION METODO SELECCION SEMANA ACTIVA
def diaDeSemana():
    # Obtener la fecha actual
    fechaActual = timezone.now().date()
    # Calcular el inicio y fin de la semana (lunes a viernes)
    inicioSem = fechaActual - timedelta(days=fechaActual.weekday())
    finSem = inicioSem + timedelta(days=4)   
    return inicioSem, finSem

#Programar menu para semana que los usuarios escogen su Menu
@login_required
def programarmenu(request):
        iniSem, finSem = diaDeSemana()
        programacion = CasinoColacion.objects.filter(fecha_servicio__range=[iniSem, finSem], id_estado = 1)
        print("AQUI OARA POR PROGRA: ", programacion)
        # Creamos un diccionario para agrupar por fecha
        programacion_dict = defaultdict(list)
        for registro in programacion:
            programacion_dict[registro.fecha_servicio].append(registro)
        
        # Convertimos el diccionario a una lista de tuplas para ordenarlos por fecha
        programacion_ordenada = sorted(programacion_dict.items())
        return render(request, 'usuario/programarmenu.html', {'programacion_ordenada': programacion_ordenada})

#AGREGAR MENU
@login_required
def agregarmenu(request):
    if request.method == 'GET':
        return redirect('menu_lista')
    else:  
        try:
            with transaction.atomic():
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
                                        id_estado = estado, id_opciones_id = opcion)
                registro.save()
                return redirect('menu_lista')
        except IntegrityError as e:
            messages.error(request, "Error al agregar el menu.")
    
#LISTA DEL MENU    
@login_required
def menu_lista(request):
    consulta = request.GET.get('q')
    if consulta:
        menu = CasinoColacion.objects.filter(titulo__icontains=consulta).order_by('fecha_servicio')
    else:
        menu = CasinoColacion.objects.all().order_by('fecha_servicio') 
    
    print(menu)
    estado = Estado.objects.all().order_by('id')
    opcion = Opciones.objects.all().order_by('id')
    context = {
        'menus': menu,
        'query': consulta,
        'estados': estado,
        'opciones': opcion
    }
    return render(request, 'admin/agregarmenu.html', context)

@csrf_exempt
def cambiar_estado_usuario(request):
    if request.method == 'POST':
        
        usuario_id = request.POST.get('usuario_id')
        activo = request.POST.get('activo')
        usuario = Usuarios.objects.get(id=usuario_id)
        usuario.activo = bool(int(activo))
        usuario.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@csrf_exempt
def cambiar_estado_menu(request):
    if request.method == 'POST':   
        id = request.POST.get('data-id')
        activo = request.POST.get('activo')
        print("ACAAAAAAAñ ",id )
        menu = CasinoColacion.objects.get(id=id)
        menu.id_estado = int(activo)
        menu.save()
        return JsonResponse({'success': True})    
    return JsonResponse({'success': False})


@csrf_exempt  # Desactiva la verificación CSRF para facilitar el desarrollo
def guardar_selecciones(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        print("ENTRAMOS :", data)
        print("authe", request.user.id)
        usuario = Usuarios.objects.get(id_user_id=request.user.id)  # Asegúrate de que el usuario esté autenticado
               
        print("ENTRAMOS2 USU:",usuario)
        
        for item in data:
            fecha_servicio = datetime.strptime(item['fecha_servicio'], '%Y-%m-%d').date()
            casino_colacion = CasinoColacion.objects.get(id=item['opcion_id'])

            Programacion.objects.create(
                usuario=usuario,
                casino_colacion=casino_colacion,
                fecha_servicio=fecha_servicio,
                cantidad_almuerzo=1,
                impreso=0
            )
        
        return redirect('principal')  # Redirige a la página principal
    return JsonResponse({'status': 'fail'}, status=400)