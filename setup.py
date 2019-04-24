from setuptools import setup, find_packages
setup(
    name="Data engineer course data generator",
    version="0.0.1",
    description="Generates the data used in the 'Become a data engineer course'",
    author="Bartosz Konieczny",
    packages=find_packages(),
    install_requires=['docutils>=0.3', 'kafka-python>=1.4.4'],
    project_urls={
        'Contact form': 'https://www.waitingforcode.com/static/contact'
    }
)
