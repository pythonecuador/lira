Development
===========

Contributing
------------

**Thanks** for the interest in contributing to Lira!

Requirements:

- Git
- Python greater or equal than ``3.7``

Get the project:

.. code-block:: bash

   git clone https://github.com/pythonecuador/lira
   cd lira

Create a virtual environment:

.. code-block:: bash

   python -m venv ven
   source venv/bin/activate

Install the project locally with:

.. code-block:: bash

   pip install -e .

Run ``python -m lira``,
or check the docs about the :doc:`modules </modules/index>` to become familiar with the project.

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

If you want help or have any questions, please join our telegram group `Python Ecuador <https://t.me/pythonecuador>`__.

Documentation
-------------

If you are contributing to the documentation,
try ``make serve-docs`` to see it locally and with hot-reloading.

Debugging
---------

If you are having problems,
you can check the logs at ``~/.local/share/lira/log/lira.log``,
or at ``~/AppData/Local/lira-data/log/lira.log`` if you are using Windows.

Roadmap
-------

Goals
~~~~~

- Command line tutorial (100% text)
- Multi platform
- Easy to install
- Content for all levels
- Autocomplete (program arguments)
- Easy to add new tutorials
- Multi-languages (i18n)
- Edit the code with your favorite editor
- Save your advance

Non-Goals
~~~~~~~~~

- It is not a web tutorial
- No mobile support
- It does not have multi-user support
- It is not an editor or IDE for Python
- Does not support other languages
- Not a replacement for Jupyter Notebook
- It is not a reference document or book

Random ideas for the future
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Multiple themes support
- Plugins
- Share your score
- Expand to other types of tutorials (physics, math, statistics)
- Against the clock mode
- Quiz mode
