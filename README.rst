Docker Hosts
--------

To use (with caution), simply do::

    >>> import dockerhosts
    >>> print dockerhosts.run()
    or docker-hosts
    or with args: docker-hosts -c /etc/hosts -s unix://var/run/docker.sock
