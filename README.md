# 🏫 App Gestión Escolar — Django
> Bootcamp Full Stack Python · Instructor: Felipe Cuevas

---

## ¿Qué contiene este proyecto?

```
App_Gestion_Escolar/          ← Raíz del proyecto (aquí vive manage.py)
│
├── manage.py                 ← El "capataz": recibe tus órdenes en terminal
│
├── requirements.txt          ← Lista de paquetes necesarios (Django)
│
├── App_Gestion_Escolar/      ← "Cerebro" del proyecto
│   ├── settings.py           ← Configuración central (apps, templates, static)
│   └── urls.py               ← Mapa de pasillos principal
│
├── alumnos/                  ← Pabellón de Alumnos
│   ├── views.py              ← Recepcionista: envía la lista al HTML
│   ├── urls.py               ← Letrero: conecta /alumnos/ con la vista
│   └── templates/alumnos/
│       └── lista_alumnos.html
│
├── profesores/               ← Pabellón de Profesores
│   ├── views.py
│   ├── urls.py
│   └── templates/profesores/
│       └── lista_profesores.html
│
├── cursos/                   ← Pabellón de Cursos
│   ├── views.py
│   ├── urls.py
│   └── templates/cursos/
│       └── lista_cursos.html
│
├── templates/                ← Templates globales
│   └── base.html             ← Plano Maestro: navbar + footer comunes
│
└── static/css/
    └── estilos.css           ← CSS centralizado (colores institucionales)
```

---

## 🚀 Cómo ejecutar el proyecto en tu computador

### Paso 1: Instalar Django

```bash
pip install django
```

### Paso 2: Entrar a la carpeta del proyecto

```bash
cd App_Gestion_Escolar
```

### Paso 3: Encender el servidor

```bash
python manage.py runserver
```

### Paso 4: Abrir en el navegador

Visita estas URLs:

| Sección     | URL                            |
|-------------|--------------------------------|
| Alumnos     | http://127.0.0.1:8000/alumnos/ |
| Profesores  | http://127.0.0.1:8000/profesores/ |
| Cursos      | http://127.0.0.1:8000/cursos/  |

---

## 📚 Conceptos clave que aprendiste

| Concepto | Archivo donde se aplica | Qué hace |
|---|---|---|
| **Registrar Apps** | `settings.py` → `INSTALLED_APPS` | Le dice a Django que las apps existen |
| **Archivos estáticos** | `settings.py` → `STATICFILES_DIRS` | Dónde buscar el CSS |
| **Plano Maestro** | `templates/base.html` | Navbar y footer compartidos |
| **Herencia** | Cada HTML hija con `{% extends %}` | Reutiliza el diseño base |
| **URL dinámicas** | `{% url 'app:nombre' %}` en navbar | Links que no se rompen |
| **Contexto** | `views.py` → diccionario → `render()` | Envía datos de Python al HTML |
| **Ciclo** | `{% for x in lista %}` en HTML | Muestra cada elemento |
| **Condicional** | `{% if lista %}` en HTML | Evita errores con listas vacías |

---

## 🔜 Próximas etapas del proyecto

- **Base de datos real** con MySQL y el ORM de Django
- **Diseño moderno** con Tailwind CSS
- **Inteligencia Artificial** para predecir alumnos en riesgo
- **Despliegue** en PythonAnywhere para mostrarlo al mundo
