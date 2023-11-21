from setuptools import setup

setup(
    name='Clean_folder',
    version='1.0',
    description='clean folder script',
    url='git',
    author='Prus Valerii',
    author_email='prusvalerii@gmail.com',
    license='MIT',
    packages=['clean_folder'],
    install_requires=[],
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:start']}
)