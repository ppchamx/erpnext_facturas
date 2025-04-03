from setuptools import setup, find_packages

setup(
    name='facturas_cfdi',
    version='0.0.1',
    description='Módulo para administrar e importar facturas CFDI en ERPNext',
    author='Jose Chavez',
    author_email='ventas@tiendamax.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[],
)
