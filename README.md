# HTTP logs data generation

The goal of this project is to generate semi-structured JSON data so you could use it in your data projects. To 
simulate real world behavior, you can specify the correctness of the generated dataset, either by telling how
incomplete or inconsistent with the perfect schema each record should be.

# Dataset characteristics

# Sinks
## Apache Kafka


# Test
## PyCharm
To launch the tests on PyCharm, you need to enable pytest as the test runner for the project. You can see how to do this
on [jetbrains.com page](https://www.jetbrains.com/help/pycharm/pytest.html)

## Command line
To execute all tests from command line, you can use `make test_all` command.

# Development
## virtualenv
Setup a virtualenv environment:
```
virtualenv -p python3 .venv/
```

Activate the installed environment:
```
source .venv/bin/activate
```

Install dependencies (venv activated):
``` 
pip3 install -r requirements.txt
```

Desactivate the virtualenv:
```
deactivate
```