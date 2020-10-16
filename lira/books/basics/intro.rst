:tags: comentarios
:level: easy

Comentarios
-----------

Los comentarios en Python comienzan con el carácter numeral (``#``),
y se extienden hasta el final visible de la línea.
Un comentario puede aparecer al comienzo de la línea o seguido de espacios en blanco o código.

.. code:: python

   # Este es un comentario
   spam = 1  # !y este es otro!

.. test:: Escribe un comentario
   :validator: lira.validators.CommentValidator
