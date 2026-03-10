from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/',        admin.site.urls),
    path('',              views.inicio,    name='inicio'),
    path('login/',        auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/',       auth_views.LogoutView.as_view(), name='logout'),
    path('alumnos/',      include('alumnos.urls')),
    path('profesores/',   include('profesores.urls')),
    path('cursos/',       include('cursos.urls')),
    path('predicciones/', include('predicciones.urls')),
    path('notas/',        include('notas.urls')),  # ← nueva línea
    path('apoderados/', include('apoderados.urls')),
    path('planificaciones/', include('planificaciones.urls')),
    path('pie/', include('pie.urls')),
]