# HTTP logs data generation

The goal of this project is to generate semi-structured JSON data so you could use it in your data projects. To 
simulate real world behavior, you can specify the correctness of the generated dataset, either by telling how
incomplete or inconsistent with the perfect schema each record should be.

# Dataset
## Schema
For the configuration without data quality issues, the generated events wil have the following schema:


| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |


| Field name   | Field type      |  Explanation                                                                                                                                       |
|--------------|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| visit_id     | text            | The identifier for a user's visit. If a user makes multiple actions without leaving the website, this identifier remains the same for all actions. |
| event_time   | date time       | The action time, in the format year-month-dayThour:minutes:seconds+tim ezone, like for example: "2020-02-27T12:49:41+00:00"                        |
| user_id      | long            | The unique identifier of the user related to the action.                                                                                           |
| keep_private | boolean         | If true, we must to anonymize everything under the User structure field.                                                                           |
|  **page**    |  structure      |                                                                                                                                                    |
| -current     | text            | The currently visited page.                                                                                                                        |
| -previous    | text - optional | The previously visited page. May be null if it's the first user's visit.                                                                           |
| **source**   | structure       |                                                                                                                                                    |
| -site        | text            | The visited website address.                                                                                                                       |
| -api_version | text            | The API version that sent the event.                                                                                                               |
| **user**     | structure       |                                                                                                                                                    |
| -ip          | text            | The IP address of the user.                                                                                                                        |
| -latitude    | double          | The geographical latitude of the user.                                                                                                             |
| -longitude   | double          | The geographical longitude of the user.                                                                                                            |


## Data issues
### 

# Executing the generators
To execute the available generators, you can either use the scripts provided in `examples` directory or 
build Docker images like defined below.

## Building Docker images
### Apache Kafka sink
To create a dockerized environment of the generator, execute the following commands:
```
make build_kafka_runner_image
cd examples/kafka/
docker-compose down --volumes
docker-compose up
```
To change the configuration, modify `examples/kafka/configuration.yaml` file.

# Test
## PyCharm
To launch the tests on PyCharm, you need to enable pytest as the test runner for the project. You can see how to do this
on [jetbrains.com page](https://www.jetbrains.com/help/pycharm/pytest.html)

## Command line
To execute all tests from command line, you can use `make test_all` command. To check test coverage, you can execute
`make test_coverage`.

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

Check code format:
```
make lint_all
```

Reformat code:
```
make reformat_all
```
