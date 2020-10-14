# Formato de los tutoriales

Los tutoriales son encapsulados en un directorio,
contienen la siguiente estructura:

```
tutorial
├── __init__.py
├── intro.rst
├── bucles.rst
├── tutorial.yaml
├── prompts.py
└── validators.py
```

Los archivos de python deben ser importables,
y estos son usados para ejecutar los tests presentados al usuario.

Los tutoriales estarán redactados en reStructuredText
con una sintaxis reducida (documentar qué no más soportamos).
El tutorial debe tener un par de metadatos locales (lista de definición).
Algo así:


```rst
:created: 01/10/2020
:updated: 02/10/2020
:tags: python, comentarios
:level: easy

Comentarios
-----------

En Python usamos ``#`` para escribir comentarios.

.. code:: python

   # this is the first comment
   spam = 1 # and this is the second comment


.. test:: Escribe un comentario!
   :help: Escribe un comentario
   :validator: pylearn.basic.validators.Comment

.. prompt:: Escribe tu nombre
   :default: Python
   :runner: pylearn.basic.runner.GetName

Bucles
------

...

```

El directorio también debe contener un archivo ``tutoril.yaml`` con
metadatos globales del tutorial:

```yaml
authors:
  - Santos Gallegos
contents:
  Intro: tutorial-example.rst
  Condicionales: condicionales.rst
  Bucles: bucles.rst
```

Existen un par de directivas especiales para pedir información al usuario o mostrar los tests.

## test

Argumento: Título del test
Opciones:
- help: ayuda adicional sobre el test (default al valor del argumento) (optional)
- validator: Módulo a una clase de Python que implemente los métodos
  `validate(self, data, options) -> bool` y `hints(self, data, option) -> list[str]`.

## prompt

Argumento: Título del prompt
Opciones:
- help: ayuda adicional sobre el prompt (default al valor del argumento) (optional)
- validator: Módulo a una clase de Python que implemente los métodos
  `run(self, data, options) -> str` (optional)
- default: valor por defecto si el usuario no ingresa nada? (optional)
- name: Nombre con la que se va a guardar la opción (required)
