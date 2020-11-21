:level: easy
:tags: showcase book

An Informal Introduction to Python
----------------------------------

Comments in Python start with the hash character, #, 
and extend to the end of the physical line. 

A hash character within a string literal is just a hash character. 

Since comments are to clarify code and are not interpreted by Python, 
they may be omitted when typing in examples.

Some examples:

.. code-block:: python

  # this is the first comment
  spam = 1  # and this is the second comment
          # ... and now a third!
  text = "# This is not a comment because it's inside quotes."


Numbers
-------

The interpreter acts as a simple calculator: 
you can type an expression at it and it will write the value. 

For example:

.. code-block:: python

  >>> 2 + 2
  4
  >>> 50 - 5*6
  20
  >>> (50 - 5*6) / 4
  5.0
  >>> 8 / 5  # division always returns a floating point number
  1.6


