# HTTP logs data generation

The goal of this project is to generate semi-structured JSON data so you could use it in your data projects. To 
simulate real world behavior, you can specify the correctness of the generated dataset, either by telling how
incomplete or inconsistent with the perfect schema each record should be.

# Dataset
## Schema
For the configuration without data quality issues, the generated events wil have the following schema:

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
| -api_version | text            | The API version that sent the event. Can be: v1, v2 or v3.                                                                                                              |
| **user**     | structure       |                                                                                                                                                    |
| -ip          | text            | The IP address of the user.                                                                                                                        |
| -latitude    | double          | The geographical latitude of the user.                                                                                                             |
| -longitude   | double          | The geographical longitude of the user.                                                                                                              |
| **technical**     | structure       |                                                                                                                                                    |
| -browser          | text            | The browser name.                                                                                                                        |
| -os    | text          | The operating system of the user.                                                                                                         |
| -lang   | text          | The browser language of the user.                                                                                                            |
| -network | text | The network type, can be one of: adsl, fiber_optic, 3g, 4g
| **-device**   | structure          |                                                                                                           |
| --type   | text          | The browser language of the user.                                                                                                            |
| --version   | text          | The browser language of the user.                                                                                                            |
| --lang   | text          | The browser language of the user.                                                                                                            |

## Data issues
To configure data issues, you have to define these properties:
```yaml
dataset:
  # ...
  composition_percentage:
    incomplete: 2
    inconsistent: 2
    fully_valid: 96
```

What's the difference between them? 

An **incomplete** event misses one or more of the following fields: 
(`device`, `network`, `technical.browser`, `source`, `visit_id`, `user_id`). All the fields except `user_id` 
are missing. `user_id` is set to 0.

An **inconsistent** event has the following data issues:
* `device`
    * can be defined as `{"type": {"name": "string"}, "version": string"}}`
* `network`
    * can be defined as `{"short_name": "string", "long_name": "string"}`
* `browser`
    * can be defined as `{"name": "string", "language": "string"}` and in that case, the `technical.lang` is missing
* `source`
    * can be defined as `www.name of the website` whereas the expected format doesn't include `www`

## Users without consent
With `users_no_data_consent_percentage` you can define the percentage of the users who would like to keep
their data private. For them, the `keep_private` field will be set to true. In the snippet below, 2% of 10
users will have this flag set to true:
```yaml
dataset:
  all_users: 10
  # ...
  users_no_data_consent_percentage: 2
```

## Late data
Late data can be simulated with `data_generator.model.unordered_data.UnorderedDataContainer` class. You have to
create the instance with a method controlling whether an event should be buffered or sent directly to the sink. All
buffered events are then considered as late and, therefore, unordered events.

You can find an example of its use in `examples/kafka/generated_dataset_to_kafka.py`:
```python
# create the container from the main configuration file 
# generation > late_data_percentage will be used to determine whether the action should be sent directly or not
unordered_data_container = UnorderedDataContainer.from_yaml_with_random_distribution(configuration)

# Method to control if the late data should be delivered
def should_send_late_data_to_kafka():
    flags = [0] * 90 + [1] * 10
    return choice(flags)

while True:
    # usual events generation
    action = visit.generate_new_action(dataset.pages, get_random_duration_in_seconds(), is_valid_log())
    unordered_data_container.wrap_action((visit.visit_id, action),
                                         lambda generated_action: configuration.send_message(
                                             output_topic_name,
                                             generated_action[0],
                                             generated_action[1]
                                         ))
    
    if should_send_late_data_to_kafka():
        unordered_data_container.send_buffered_actions(
            lambda late_action: configuration.send_message(output_topic_name, late_action[0], late_action[1]))
```

## App versions
As for this writing, the `versions_percentage` part doesn't introduce any differences and it's here just to simulate some
variability in case of app version analytics axis. 

# Executing the generators
To execute the available generators, you can either use the scripts provided in `examples` directory or 
build Docker images like defined below.

## Building Docker images
### Apache Kafka sink
To create a dockerized environment of the generator, execute the following commands:
```
make build_kafka_runner_image
cd examples/kafka-docker
docker-compose down --volumes
docker-compose up
```
To change the configuration, modify `examples/kafka-docker/configuration.yaml` file.

The broker will be available at `localhost:29092`.

## Running Python scripts
### Apache Kafka sink
To start Apache Kafka sink from the script, execute the following commands:
* start the broker
```
cd examples/kafka
docker-compose down --volumes
docker-compose up
```
The broker will be available at `localhost:29092`.

* start the generator
```
python examples/kafka/generate_dataset_to_kafka.py
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
## Code checks
Check code format:
```
make lint_all
```

Reformat code:
```
make reformat_all
```

## Pre-commit hook setup
The hook will execute the code formatting before the commit and the unit tests before the push. To install
it, please use [Pre-commit plugin](https://pre-commit.com/) and `pre-commit install` command.