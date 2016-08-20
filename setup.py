from setuptools import setup, find_packages

# Customize
package_name = 'HboMovieData'
version = '0.1.0'
description = 'Creates a file with movie data for all current HBO GO movies'
install_requires = [
    'requests',
]


setup(
    name=package_name,
    version=version,
    description=description,
    url='https://github.com/dlomelin/%s' % (package_name),
    author='David Lomelin',
    author_email='david.lomelin@gmail.com',
    packages=find_packages(),
    install_requires=install_requires,
)
