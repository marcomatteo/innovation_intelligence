from setuptools import setup, find_packages

setup(
   name='innovation_intelligence',
   version='1.0',
   description='Modulo per test, controllo qualità di I2FVG',
   author='Marco Matteo Buzzulini',
   author_email='marco.matteo.buzzulini@areasciencepark.it',
   packages=find_packages(),
#    [
#         'file_parser',
#         'data_provider',
#         'idb',
#         'tests'
#        ], 
   install_requires=['pandas', 'numpy', 'sqlalchemy', 'xlrd', 'xlsxwriter', 'openpyxl'],
)