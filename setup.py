from setuptools import setup
import re

pkg_init_file = open('keepaneyeon/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__\s*=\s*'([^']+)'", pkg_init_file))

setup(name='keepaneyeon',
      version=metadata['version'],
      description='Monitor URLs for changes',
      url='https://github.com/mmcloughlin/keepaneyeon',
      author='Michael McLoughlin',
      license='MIT',
      packages=['keepaneyeon'],
      entry_points={
          'console_scripts': [
              'keepaneyeon = keepaneyeon.cli:main',
              ]
          },
      install_requires=[
          'requests[security]',
          'boto',
          'PyYAML',
          ],
      test_suite='nose.collector',
      tests_require=[
          'nose',
          'coverage',
          'mock',
          'responses',
          'moto',
          ],
      )
