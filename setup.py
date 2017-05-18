from setuptools import setup, find_packages

import pynnmap_arcgis_post_process

setup(
    name='pynnmap_arcgis_post_process',
    version=pynnmap_arcgis_post_process.__version__,
    url='http://github.com/lemma-osu/pynnmap-arcgis-post-process/',
    author='LEMMA group @ Oregon State University',
    author_email='matt.gregory@oregonstate.edu',
    packages=find_packages(),
    description='Post-process pynnmap prediction rasters to ArcGIS format',
    install_requires=[
        # 'arcpy',
        'click',
        'matplotlib',
        'six'
    ],
    entry_points='''
        [pynnmap.cli_commands]
        post-process=pynnmap_arcgis_post_process.cli.post_process:post_process
    ''',
)
