from setuptools import setup, find_packages
 
setup(
    name='django-positions',
    version='0.5.3',
    description='(Django Positions needs a new maintainer) A Django field for custom model ordering',
    author='Joel Watts',
    author_email='joel@joelwatts.com',
    url='http://github.com/jpwatts/django-positions',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django',
        'setuptools'
    ],
)
