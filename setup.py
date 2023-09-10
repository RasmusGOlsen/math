from setuptools import setup, find_packages

setup(
    name='math',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    package_data={
        'mathtables.resources.fonts': ['*'],
        'mathtables.resources.images': ['*'],
        'mathtables.resources.sounds': ['*'],
    },
    include_package_data=True,
    install_requires=[
        'pygame',
    ],
    entry_points={
        'console_scripts': ['math=mathtables.__main__:main'],
    },
)
