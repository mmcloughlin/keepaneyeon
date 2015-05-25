from setuptools import setup, find_packages

setup(name='keepaneyeon',
      version='0.1.0',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'keepaneyeon = keepaneyeon.cli:main',
              ]
          }
      )
