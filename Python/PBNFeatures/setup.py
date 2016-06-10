from setuptools import setup

setup(name='PBNFeatures',
        version='0.1',
        description='Generate features from images',
        url='http://github.com/majorgowan/painterByNumbers_5thFloor',
        author='Mark Fruman',
        author_email='majorgowan@yahoo.com',
        license='MIT',
        packages=['paletteTools', 'cylindrical', 'textureTools']
        install_requires=['Pillow'],
        zip_safe=False)
