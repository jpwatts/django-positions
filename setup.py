from setuptools import setup, find_packages
 
setup(
    name='django-positions',
    version='0.5.0',
    description='A Django field for custom model ordering.',
    author='Joel Watts',
    author_email='joel@joelwatts.com',
    url='http://github.com/jpwatts/django-positions',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)
