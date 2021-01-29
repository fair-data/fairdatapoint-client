import logging
from fdpclient import operations

logger = logging.getLogger(__name__)

class Client:
    def __init__(self, host, host_as_fdp=False):
        """The Client object to connect to a FAIR Data Point server.

        FAIR Data Point server contains 4 types of metadata as described in the
        `specification`_:

        ============  ======================
        type          path
        ============  ======================
        fdp           <host>/fdp or <host>
        catalog       <host>/catalog
        dataset       <host>/dataset
        distribution  <host>/distribution
        ============  ======================

        A server may use the host URL to store the 'fdp' metadata, and then
        the 'fdp' path is the same as the host.

        .. _`specification`: https://github.com/FAIRDataTeam/FAIRDataPoint-Spec/blob/master/spec.md

        Args:
            host(str): the host URL
            host_as_fdp(bool): the host is also the fdp, i.e. the host stores
                the fdp metadata, and the host and fdp share the same URL.
                Otherwise, the fdp URL should be ``<host>/fdp``.
                Defaults to False.

        Examples:
            >>> client = Client('http://fdp.fairdatapoint.nl`)
            >>> fdp_metadata = client.read_fdp()
            >>> catalog_metadata = client.read_catalog('catalog01')
            >>> print(fdp_metadata, catalog_metadata)
        """
        self.host = host.rstrip('/')
        self.host_as_fdp = host_as_fdp

    # Create metadata
    def create_fdp(self, data, format='turtle', **kwargs):
        """Create fdp metadata.

        Args:
            data(str, bytes or file-like object):
                the content of metadata to send in the request body.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``content-type``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        if self.host_as_fdp:
            r = self._request('create', '', data=data, format=format, **kwargs)
        else:
            r = self._request('create', 'fdp', data=data, format=format, **kwargs)
        return r

    def create_catalog(self, data, format='turtle', **kwargs):
        """Create a new catalog metadata."""
        return self._request('create', 'catalog', data=data, format=format, **kwargs)

    def create_dataset(self, data, format='turtle', **kwargs):
        """Create a new dataset metadata."""
        return self._request('create', 'dataset', data=data, format=format, **kwargs)

    def create_distribution(self, data, format='turtle', **kwargs):
        """Create a new distribution metadata."""
        return self._request('create', 'distribution', data=data, format=format, **kwargs)

    # Read metadata
    def read_fdp(self, format='turtle', **kwargs):
        """Read the fdp metadata."""
        if self.host_as_fdp:
            r = self._request('read', '', id='', format=format, **kwargs)
        else:
            r = self._request('read', 'fdp', id='', format=format, **kwargs)
        return r

    def read_catalog(self, id, format='turtle', **kwargs):
        """Read a catalog metadata.

        Args:
            id(str): the identifier of the metadata.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``accept``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        return self._request('read', 'catalog', id=id, format=format, **kwargs)

    def read_dataset(self, id, format='turtle', **kwargs):
        """Read a dataset metadata."""
        return self._request('read', 'dataset', id=id, format=format, **kwargs)

    def read_distribution(self, id, format='turtle', **kwargs):
        """Read a distribution metadata."""
        return self._request('read', 'distribution', id=id, format=format, **kwargs)

    # Update metadata
    def update_fdp(self, data, format = 'turtle', **kwargs):
        """Update the fdp metadata."""
        if self.host_as_fdp:
            r = self._request('update', '', id='', data=data, format=format, **kwargs)
        else:
            r = self._request('update', 'fdp', id='', data=data, format=format, **kwargs)
        return r

    def update_catalog(self, id, data, format='turtle', **kwargs):
        """Update a catalog metadata."""
        return self._request('update', 'catalog', id=id, data=data, format=format, **kwargs)

    def update_dataset(self, id, data, format='turtle', **kwargs):
        """Update a dataset metadata."""
        return self._request('update', 'dataset', id=id, data=data, format=format, **kwargs)

    def update_distribution(self, id, data, format='turtle', **kwargs):
        """Update a distribution metadata."""
        return self._request('update', 'distribution', id=id, data=data, format=format, **kwargs)

    # Delete metadata
    def delete_catalog(self, id, **kwargs):
        """Delete a catalog metadata."""
        return self._request('delete', 'catalog', id=id, **kwargs)

    def delete_dataset(self, id, **kwargs):
        """Delete a dataset metadata."""
        return self._request('delete', 'dataset', id=id, **kwargs)

    def delete_distribution(self, id, **kwargs):
        """Delete a distribution metadata."""
        return self._request('delete', 'distribution', id=id, **kwargs)

    # Private methods
    def _request(self, operation, type, id=None, data=None, format='turtle', **kwargs):
        """Private request method.

        Args:
            operation(str): the request operation.
                Available options: 'read', 'write', 'update' and 'delete'.
                See :class:`fdpclient.operations`.
            type(str): the type of metadata.
                Available types: 'fdp', 'catalog', 'dataset' and 'distribution'.
                When ``host_as_fdp`` is True, the 'fdp' type should be specified
                as empty string, i.e. ``''``.
            id(str): the identifier of the metadata.
                Defaults to None.
            data(str, bytes or file-like object):
                the content of metadata to send in the request body.
                Defaults to None.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``content-type`` or
                ``accept``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                See :const:`fdpclient.config.DATA_FORMATS`.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """

        request_methods = ('create', 'read', 'update', 'delete')

        if operation not in request_methods:
            raise ValueError(f'Invalid request method: {operation}')

        if operation in ('read', 'delete', 'update') and id is None:
            raise ValueError(f'Metadata "id" must be given for request method {operation}')

        if operation in ('create', 'update') and data is None:
            raise ValueError(f'Metadata "data" must be given for request method {operation}')

        if id is not None:
            url = '/'.join([self.host, type, id])
        else:
            url = '/'.join([self.host, type])
        url = url.rstrip('/')

        logger.debug(f'Request: {operation} metadata on {url}')
        request = getattr(operations, operation)
        if operation == 'delete':
            r = request(url=url, data=data, **kwargs)
        else:
            r = request(url=url, data=data, format=format, **kwargs)
        return r