from setuptools import setup, find_packages

setup(name='keepaneyeon',
      version='0.1.0',
      description='Monitor URLs for changes',
      url='https://github.com/mmcloughlin/keepaneyeon',
      author='Michael McLoughlin',
      license='MIT',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'keepaneyeon = keepaneyeon.cli:main',
              ]
          },
      test_suite='nose.collector',
      tests_require=[
          'nose',
          'coverage',
          'responses',
          ],
      )
