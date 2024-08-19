import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='django-richmin',
    url='https://github.com/mymy47/django-richmin',
    version='0.1.18',
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,
    description='Customized lte-bootstrap django admin theme with some useful tools',
    long_description=README,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=[
        'django>4,<5',
    ],
    author='my47',
    author_email='mymy47@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ],
)
