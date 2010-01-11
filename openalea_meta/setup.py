import os, sys
pj = os.path.join

from setuptools import setup, find_packages

from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in zip(metadata.keys(), metadata.values()):
    exec("%s = '%s'" % (key, value))


platform = sys.platform
external_dependencies = [
'numpy',
'scipy',
'matplotlib>=0.99',
]

if platform != 'darwin':
    external_dependencies.append('PIL<=1.1.6')

alea_dependencies = [
'openalea.deploy >= 0.7.0.dev',
'openalea.deploygui >= 0.7.0.dev',
'openalea.core >= 0.7.0.dev',
'openalea.visualea >= 0.7.0.dev',
'openalea.stdlib >= 0.7.0.dev',
'openalea.sconsx >=0.7.0.dev',
'openalea.misc >=0.7.0.dev',
'openalea.scheduler >=0.7.0.dev',
#'openalea.container >=2.0.1.dev',
#'openalea.mtg >=0.7.0.dev',
]

install_requires = alea_dependencies

# Add dependencies on Windows and Mac OS X platforms
if 'win' in platform:
    install_requires += external_dependencies 

setup(
    name = name,
    version = version,
    description = description,
    long_description = long_description,
    author = authors,
    author_email = authors_email,
    url = url,
    license = license,


    create_namespaces=False,
    zip_safe=False,

    packages=find_packages('src'),

    package_dir={"":"src" },

    # Add package platform libraries if any
    include_package_data=True,
    package_data = {'' : ['*.png']},
    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = install_requires,
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points = {"wralea": ['openalea = openalea']},
    )


