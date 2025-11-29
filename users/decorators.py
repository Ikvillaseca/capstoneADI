from django.contrib.auth.decorators import user_passes_test

def es_administrador(user):
    return user.groups.filter(name='Administradores').exists()

def es_chofer(user):
    return user.groups.filter(name='Choferes').exists()

def administrador_requerido(view_func):
    """Decorador que requiere que el usuario sea administrador"""
    decorated_view = user_passes_test(
        es_administrador,
        login_url='index',
        redirect_field_name=None
    )(view_func)
    return decorated_view

def chofer_requerido(view_func):
    """Decorador que requiere que el usuario sea chofer"""
    decorated_view = user_passes_test(
        es_chofer, login_url="index", redirect_field_name=None
    )(view_func)
    return decorated_view