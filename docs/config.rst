Configuration
=============

The configuration file is located at ``~/.config/lira/config.yaml`` on UNIX-like systems,
and at ``~/AppData/Local/config.yaml`` on Windows systems.
This is how it looks like

.. code-block:: yaml

   books:
     - lira.books.intro
     - example/

.. note::

   Lira follows the XDG_ base directory specification.

   .. _XDG: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html


All supported settings are document below.

books
-----

List of books, each book can be a dotted path to the module of the book,
or a local path to the directory of the book
(it can be a relative path to the config file).

.. code-block:: yaml
   books:
      # A dotted path to a module
      - lira.books.intro

      # An absolute local path
      - ~/local/path/to/book/

      # A relative path to the config file
      - relative/path

Defaults to:

.. code-block:: yaml

   books:
     - lira.books.intro
