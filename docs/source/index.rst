==========================
FAIR Data Point API Client
==========================
.. contents::
    :depth: 3

.. meta::
   :description: A collection of tutorials and guides for fairdatapoint-client package.
   :keywords: fairdatapoint, metadata, guide, tutorial, doc

fairdatapoint-client is a simple and elegant library to interact with
`FAIR Data Point <https://github.com/fair-data/fairdatapoint>`_ resources from
Python, e.g. read and write catalogs, datasets and distributions in an FDP server.

The supported APIs are listed below:

.. list-table::
   :widths: 20 30 40
   :header-rows: 1

   * - FDP Layers
     - Path Endpoint
     - Specific Resource Endpoint
   * - fdp
     - [baseURL] or [baseURL]/fdp
     -
   * - catalog
     - [baseURL]/catalog
     - [baseURL]/catalog/[catalogID]
   * - dataset
     - [baseURL]/dataset
     - [baseURL]/dataset/[datasetID]
   * - distribution
     - [baseURL]/distribution
     - [baseURL]/distribution/[distributionID]

Quick Start
-----------

Using Client

.. code-block:: python

    from fdpclient.client import Client

    # create a client with base URL
    client = Client('http://example.org')

    # create metadata
    with open('catalog01.ttl') as f:
        data = f.read()
    client.create_catalog(data)

    # let's assume the catalogID was assigned as 'catalog01'
    # read metadata, return a RDF graph
    r = client.read_catalog('catalog01')
    print(r.serialize(format="turtle").decode("utf-8"))

    # update metadata
    with open('catalog01_update.ttl') as f:
        data_update = f.read()
    client.update_catalog('catalog01', data_update)

    # delete metadata
    client.delete_catalog('catalog01')

Using operation functions

.. code-block:: python


    from fdpclient import operations

    # create metadata
    with open('catalog01.ttl') as f:
    data = f.read()
    operations.create('http://example.org/catalog', data)

    # read metadata, return a RDF graph
    r = operations.read('http://example.org/catalog/catalog01')
    print(r.serialize(format="turtle").decode("utf-8"))

    # update metadata
    with open('catalog01_update.ttl') as f:
        data_update = f.read()
    operations.update('http://example.org/catalog/catalog01', data_update)

    # delete metadata
    operations.delete('http://example.org/catalog/catalog01')


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