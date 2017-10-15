from setuptools import setup, find_packages
with open('requirements.txt') as f:
    data = f.read()
requirements = data.split()

setup(
    name='manuel',
    version='0.1.1',
    packages=find_packages(),
    url='https://github.com/Xevib/manuel',
    license='MIT',
    author='Xavier Barnada',
    author_email='xbarnada@gmail.com',
    description='Tool to generate reports',
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        manuel=manuel.cli:cli_generate_report
    ''',
)
