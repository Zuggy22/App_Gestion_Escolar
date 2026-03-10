from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Curso
from .forms import CursoForm


@login_required
def lista_cursos(request):
    # Buscador: filtra por nombre del ramo o nivel
    busqueda = request.GET.get('q', '')
    if busqueda:
        cursos = Curso.objects.filter(
            nombre_ramo__icontains=busqueda
        ) | Curso.objects.filter(
            nivel__icontains=busqueda
        )
    else:
        cursos = Curso.objects.all()

    return render(request, 'cursos/lista_cursos.html', {
        'cursos':   cursos,
        'titulo':   'Lista de Cursos',
        'busqueda': busqueda,
    })


@login_required
def crear_curso(request):
    if request.method == 'POST':
        formulario = CursoForm(request.POST)
        if formulario.is_valid():
            curso = formulario.save()
            messages.success(request, f'✅ El curso {curso.nombre_ramo} fue creado exitosamente.')
            return redirect('cursos:lista')
    else:
        formulario = CursoForm()
    return render(request, 'cursos/crear_curso.html', {
        'formulario': formulario
    })


@login_required
def editar_curso(request, pk):
    curso = Curso.objects.get(pk=pk)
    if request.method == 'POST':
        formulario = CursoForm(request.POST, instance=curso)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, f'✅ El curso {curso.nombre_ramo} fue actualizado.')
            return redirect('cursos:lista')
    else:
        formulario = CursoForm(instance=curso)
    return render(request, 'cursos/crear_curso.html', {
        'formulario': formulario
    })


@login_required
def eliminar_curso(request, pk):
    curso = Curso.objects.get(pk=pk)
    if request.method == 'POST':
        nombre = curso.nombre_ramo
        curso.delete()
        messages.error(request, f'🗑️ El curso {nombre} fue eliminado del sistema.')
        return redirect('cursos:lista')
    return render(request, 'cursos/confirmar_eliminar.html', {
        'objeto': curso
    })
