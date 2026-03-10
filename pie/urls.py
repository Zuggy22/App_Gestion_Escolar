from django.urls import path
from . import views

app_name = 'pie'

urlpatterns = [
    # Registros PIE
    path('',                                views.lista_pie,            name='lista'),
    path('crear/',                          views.crear_registro,       name='crear'),
    path('<int:pk>/',                       views.detalle_pie,          name='detalle'),
    path('<int:pk>/editar/',                views.editar_registro,      name='editar'),

    # Especialistas
    path('<int:reg_pk>/especialista/',      views.agregar_especialista, name='agregar_especialista'),
    path('especialista/<int:pk>/eliminar/', views.eliminar_especialista,name='eliminar_especialista'),

    # PACI
    path('<int:reg_pk>/paci/',              views.agregar_paci,         name='agregar_paci'),
    path('paci/<int:pk>/editar/',           views.editar_paci,          name='editar_paci'),
    path('paci/<int:pk>/pdf/',              views.paci_pdf,             name='paci_pdf'),

    # Evaluaciones
    path('<int:reg_pk>/evaluacion/',        views.agregar_evaluacion,   name='agregar_evaluacion'),
    path('evaluacion/<int:pk>/editar/',     views.editar_evaluacion,    name='editar_evaluacion'),

    # Informes
    path('<int:reg_pk>/informe/',           views.agregar_informe,      name='agregar_informe'),
    path('informe/<int:pk>/pdf/',           views.informe_pdf,          name='informe_pdf'),
]