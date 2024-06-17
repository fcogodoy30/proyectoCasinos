from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.shortcuts import redirect

class SessionInactivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ejecutar antes de que se procese la vista
        response = self.get_response(request)

        # Verificar si el usuario está autenticado y actualizar la actividad de sesión
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            # Verificar si se ha superado el tiempo de inactividad permitido
            if last_activity and (timezone.now() - last_activity > timedelta(seconds=settings.SESSION_INACTIVITY_TIMEOUT)):
                # Realizar alguna acción cuando el usuario esté inactivo, por ejemplo, cerrar sesión
                request.session.flush()  # Limpiar la sesión completamente
                return redirect('cerrarsession')  # Redirigir al inicio de sesión
            # Actualizar la actividad de sesión en cada solicitud
            request.session['last_activity'] = timezone.now()

        return response
