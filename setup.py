from setuptools import setup, find_packages
setup(
    name="HTTP logs web visits data generator",
    version="0.0.1",
    description="Generates the data simulating user visits of a website",
    author="Bartosz Konieczny",
    packages=find_packages(),
    install_requires=['docutils>=0.3', 'confluent-kafka==0.11.6],
    project_urls={
        'Contact form': 'https://www.waitingforcode.com/static/contact'
    }
)
