from setuptools import setup

setup(
    name='slice_scanner',
    version='1.0',
    long_description=__doc__,
    packages=['slice_scanner'],
    url='ianluddy@gmail.com',
    author_email='ianluddy@gmail.com',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "flask_autodoc",
        "flask_pymongo"
    ],
    entry_points={
        'console_scripts': [
            'slice = slice_scanner:run',
        ]
    }
)