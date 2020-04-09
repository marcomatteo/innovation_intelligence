from setuptools import setup

setup(
   name='innovation_intelligence',
   version='1.0',
   description='Modulo per test, controllo qualità di I2FVG',
   author='Marco Matteo Buzzulini',
   author_email='marco.matteo.buzzulini@areasciencepark.it',
   packages=[
        'file_parser',
        'data_provider',
        'idb'
       ], 
   install_requires=['pandas', 'numpy', 'sqlalchemy'],
   scripts=[
        'preprocessing_infocamere'
        ]
)