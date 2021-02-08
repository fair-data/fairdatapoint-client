==========================
FAIR Data Point API Client
==========================

.. meta::
   :description: A collection of tutorials and guides for fairdatapoint-client package.
   :keywords: fairdatapoint, metadata, guide, tutorial, doc

fairdatapoint-client is a simple and elegant Python package to work with REST
APIs of FAIR Data Point.

-----------------------------------------------------------------------------

**The power of fairdatapoint-client:**

.. ipython:: python

    from fdpclient import operations
    r = operations.read('http://145.100.57.30/catalog/catalog02')
    print(r.serialize(format="turtle").decode("utf-8"))


.. ipython:: python

    from fdpclient.client import Client
    client = Client('http://145.100.57.30')
    r = client.read_catalog('catalog02')
    print(r.serialize(format="turtle").decode("utf-8"))

User Guide
----------
.. toctree::
    :maxdepth: 3

    Quick Start <tutorial>
    APIs <api>


List of Methods/Functions
-------------------------

Client methods
::::::::::::::
.. currentmodule:: fdpclient.client.Client

You can use :class:`fdpclient.client.Client` class and its methods to process FDP metadata.

.. autosummary::

    create_fdp
    create_catalog
    create_dataset
    create_distribution

.. autosummary::

    read_fdp
    read_catalog
    read_dataset
    read_distribution

.. autosummary::

    update_fdp
    update_catalog
    update_dataset
    update_distribution

.. autosummary::

    delete_catalog
    delete_dataset
    delete_distribution

Operation functions
:::::::::::::::::::

You can also use :mod:`fdpclient.operations` functions to process FDP metadata.

.. currentmodule:: fdpclient.operations

.. autosummary::

    create
    read
    update
    delete


Indices and tables
------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`