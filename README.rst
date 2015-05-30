keepaneyeon
===========

|buildstatus| |coverage|

Monitor URLs for changes

Quick Start
-----------

``keepaneyeon`` is configured with YAML. The following configuration will
download the URLs ``http://httpbin.org/html`` and
``http://httpbin.org/bytes/128``. It will store the results in S3.

.. code:: yaml

  storage:
    - &aws !storage/s3
      access_key: <...>
      secret_access_key: <...>
      path: 's3://bucket/path'

  downloaders:
    - &http !downloader/http {}

  targets:
    - !target
      name: static
      downloader: *http
      url: 'http://httpbin.org/html'
      store: *aws

    - !target
      name: dynamic
      downloader: *http
      url: 'http://httpbin.org/bytes/128'
      store: *aws

If ``config.yaml`` contains the above configuration, you can execute the
download with::

  keepaneyeon config.yaml



.. |buildstatus| image:: https://img.shields.io/travis/mmcloughlin/keepaneyeon.svg
   :target: https://travis-ci.org/mmcloughlin/keepaneyeon

.. |coverage| image:: https://img.shields.io/coveralls/mmcloughlin/keepaneyeon.svg
   :target: https://coveralls.io/r/mmcloughlin/keepaneyeon
