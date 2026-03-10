import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'App_Gestion_Escolar.settings')
django.setup()

from alumnos.models import Alumno
from notas.models import Asistencia

def test_registrar_asistencia():
    # Buscamos un alumno existente
    alumno = Alumno.objects.first()
    if not alumno:
        print("❌ No hay alumnos registrados para la prueba.")
        return

    print(f"Probando con el alumno: {alumno.nombre} {alumno.apellido}")

    # Datos de prueba
    asignatura = 'Matemáticas'
    fecha = datetime.date.today()
    estado = 'Presente'

    try:
        # Intentamos registrar asistencia como lo hace la vista individual
        asistencia, creada = Asistencia.objects.update_or_create(
            alumno=alumno,
            asignatura=asignatura,
            fecha=fecha,
            defaults={'estado': estado}
        )
        if creada:
            print(f"✅ Asistencia registrada correctamente: {asistencia}")
        else:
            print(f"✅ Asistencia actualizada correctamente: {asistencia}")

        # Intentamos registrar de nuevo para asegurar que update_or_create funciona
        asistencia, creada = Asistencia.objects.update_or_create(
            alumno=alumno,
            asignatura=asignatura,
            fecha=fecha,
            defaults={'estado': 'Ausente'}
        )
        print(f"✅ Asistencia actualizada a 'Ausente': {asistencia}")

    except Exception as e:
        print(f"❌ Error al registrar asistencia: {e}")

if __name__ == "__main__":
    test_registrar_asistencia()
