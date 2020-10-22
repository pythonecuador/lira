Development
===========

**Thanks** for the interest in contributing to lira!

Requirements:

- Git
- Python greater or equal than ``3.7``

Get the project:

.. code-block:: bash

   git clone https://github.com/pythonecuador/lira

Create a virtual environment:

.. code-block:: bash

   python -m venv ven
   source venv/bin/activate

Install the project locally with:

.. code-block:: bash

   pip install -e .

Run ``python -m lira``,
or check the docs about the :doc:`modules </modules/index>` to get familiar with the project.

.. note::

   Try to write tests for each new feature or bug fixed.
   See `tests/ <https://github.com/pythonecuador/lira/tree/master/tests>`__ for inspiration.

Install nox_ to run the tasks:

.. code-block:: bash

   python -m pip install nox

Check the available tasks with ``python -m nox -l``,
and execute the task with ``python -m nox -s <task>``.

.. _nox: https://nox.thea.codes/en/stable/

Before sending a pull request,
make sure to run the formatter,
and see if the linter, tests, and coverage are passing.

.. code-block::

   make format
   make lint
   make tests
   make coverage
