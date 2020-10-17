:tags: comments
:level: easy

Comments
--------

Comments in *Python* start with the hash character (``#``),
and extend to the end of the line.
A comment may appear at the **start of the line or following whitespace or code**. 

.. code-block:: python

   # This is a comment
   spam = 1  # and this is another one!

.. Ignore me, I'm a comment

.. test-block:: Write a comment
   :validator: lira.validators.CommentValidator

.. test-block:: Write another comment
   :help: Just write another comment :)
   :validator: lira.validators.CommentValidator
