:level: easy
:tags: showcase book

Inline text
-----------

This is a paragraph with *some* nodes.
I'm a ``literal`` node, and I'm **strong**.

Code blocks
-----------

This is a ``Python`` code block:

.. code-block:: python

   print("Hello world!")

This is a ``JavaScript`` code block:

.. code-block:: js

   console.log("Hello world!")

Test blocks
-----------

.. test-block:: This is a test block
   :validator: lira.validators.Validator

   Write your guess here.

.. test-block:: Invalid answer
   :validator: lira.validators.Validator
   :state: invalid

   This is how a test block looks like 
   if you don't answer correctly :(

.. test-block:: Valid answer
   :validator: lira.validators.Validator
   :language: python
   :state: valid

   # This is how a test block looks like when you pass the test!
   # Test blocks also support highlighting.

   print("You did it!")
