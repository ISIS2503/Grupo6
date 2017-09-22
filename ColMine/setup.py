from setuptools import setup, find_packages
from colmine import __version__

setup(
    name='ColMine',
    version=__version__,

    url='http://host/',
    author='suavized',
    author_email='',

    packages=find_packages(),
    include_package_data=True,
    scripts=['scripts/manage.py'],

    install_requires=(
        'django<1.7',
    )
)

