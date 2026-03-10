from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profesor
from .forms import ProfesorForm


@login_required
def lista_profesores(request):
    # Buscador: obtiene el parámetro 'q' de la URL (?q=nombre)
    busqueda = request.GET.get('q', '')
    if busqueda:
        profesores = Profesor.objects.filter(
            nombre__icontains=busqueda
        ) | Profesor.objects.filter(
            especialidad__icontains=busqueda
        )
    else:
        profesores = Profesor.objects.all()

    return render(request, 'profesores/lista_profesores.html', {
        'profesores': profesores,
        'titulo':     'Lista de Profesores',
        'busqueda':   busqueda,
    })


@login_required
def crear_profesor(request):
    if request.method == 'POST':
        formulario = ProfesorForm(request.POST)
        if formulario.is_valid():
            profesor = formulario.save()
            messages.success(request, f'✅ El profesor {profesor.nombre} fue registrado exitosamente.')
            return redirect('profesores:lista')
    else:
        formulario = ProfesorForm()
    return render(request, 'profesores/crear_profesor.html', {
        'formulario': formulario
    })


@login_required
def editar_profesor(request, pk):
    profesor = Profesor.objects.get(pk=pk)
    if request.method == 'POST':
        formulario = ProfesorForm(request.POST, instance=profesor)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, f'✅ Los datos de {profesor.nombre} fueron actualizados.')
            return redirect('profesores:lista')
    else:
        formulario = ProfesorForm(instance=profesor)
    return render(request, 'profesores/crear_profesor.html', {
        'formulario': formulario
    })


@login_required
def eliminar_profesor(request, pk):
    profesor = Profesor.objects.get(pk=pk)
    if request.method == 'POST':
        nombre = profesor.nombre
        profesor.delete()
        messages.error(request, f'🗑️ El profesor {nombre} fue eliminado del sistema.')
        return redirect('profesores:lista')
    return render(request, 'profesores/confirmar_eliminar.html', {
        'objeto': profesor
    })