import logging
import requests
import rdflib
from fdpclient import DATA_FORMATS

logger = logging.getLogger(__name__)

def create(url, data, format='turtle', **kwargs):
    """Send a create request.

    Args:
        url(str): URL for creating a metadata.
        data(str, bytes or file-like object):
            the content of metadata to send in the request body.
        format (str, optional): the format of the metadata.
            This argument overwrites the request header ``content-type``.
            Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
            Defaults to 'turtle'.
        **kwargs: Optional arguments that :func:`requests.request` takes.
    """
    logger.debug(f'Create metadata on {url} with the content: \n{data}')
    if 'content-type' in kwargs:
        kwargs['headers']['content-type'] = DATA_FORMATS[format]
    try:
        r = requests.post(url, data, **kwargs)
    except Exception as error:
        print(f'Unexpected error when connecting to {url}\n')
        raise error
    else:
        if r.status_code >= 300:
            print(f'HTTP error: {r.status_code} {r.reason} for {url}',
                  f'\nResponse message: {r.text}')
            raise

def read(url, format='turtle', **kwargs):
    """Send a read request.

    Args:
        url(str): URL for reading a metadata.
        format (str, optional): the format of the metadata.
            This argument overwrites the request header ``accept``.
            Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
            Defaults to 'turtle'.
        **kwargs: Optional arguments that :func:`requests.request` takes.

    Returns:
        :class:`requests.Response`: response of the read request.
    """
    logger.debug(f'Read metadata: {url}')
    if 'headers' in kwargs:
        kwargs['headers']['accept'] = DATA_FORMATS[format]
    try:
        r = requests.get(url, **kwargs)
    except Exception as error:
        print(f'Unexpected error when connecting to {url}\n')
        raise error
    else:
        if r.status_code != 200:
            print(f'HTTP error: {r.status_code} {r.reason} for {url}',
                  f'\nResponse message: {r.text}')
            raise

    g = rdflib.Graph()
    g.parse(data=r.text, format=format)
    return g


def update(url, data, format='turtle', **kwargs):
    """Send an update request.

    Args:
        url(str): URL for updating a metadata.
        data(str, bytes or file-like object):
            the content of metadata to send in the request body.
        format (str, optional): the format of the metadata.
            This argument overwrites the request header ``content-type``.
            Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
            Defaults to 'turtle'.
        **kwargs: Optional arguments that :func:`requests.request` takes.
    """
    logger.debug(f'Update metadata on {url} with the content: \n{data}')
    if 'content-type' in kwargs:
        kwargs['headers']['content-type'] = DATA_FORMATS[format]
    try:
        r = requests.put(url, data, **kwargs)
    except Exception as error:
        print(f'Unexpected error when connecting to {url}\n')
        raise error
    else:
        if r.status_code >= 300:
            print(f'HTTP error: {r.status_code} {r.reason} for {url}',
                  f'\nResponse message: {r.text}')
            raise

def delete(url, **kwargs):
    """Send a delete request.

    Args:
        url(str): URL for deleting a metadata.
        **kwargs: Optional arguments that :func:`requests.request` takes.
    """
    logger.debug(f'Delete metadata: {url}')
    try:
        r = requests.delete(url, **kwargs)
    except Exception as error:
        print(f'Unexpected error when connecting to {url}\n')
        raise error
    else:
        if r.status_code >= 300:
            print(f'HTTP error: {r.status_code} {r.reason} for {url}',
                  f'\nResponse message: {r.text}')
            raise