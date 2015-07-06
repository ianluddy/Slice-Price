from setuptools import setup

setup(
    name='Slice Scanner',
    version='1.0',
    long_description=__doc__,
    packages=['pizza'],
    url='ianluddy@gmail.com',
    author_email='ianluddy@gmail.com',
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'pizza = pizza:run',
        ]
    }
)