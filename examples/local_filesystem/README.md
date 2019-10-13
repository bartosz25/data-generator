# Local file system sink example

An example of generator writing data to a local file system directory.

# How to run?
Before executing these steps, activate your virtualenv as stated in [README.md](../../README.md#development) under Development section.
Execute all commands from the main directory of the project (data-generator)
1. Start generation script: `python examples/local_filesystem/write_sessions_to_local_filesystem.py`

# How to configure
By default the script generates the data partitioned by `event_time` column. The generation starts 
3 days ago. The files will contain 200000 entries which should generate files of ~100MB. The data will
be written into `/tmp/sessions/input`. You can configure all these properties in the 
`write_sessions_to_local_filesystem.py`.

#Tips
1. If you want to generate data across different partitions, play with:
- Dataset's: `duration_min_seconds` and `duration_max_minutes` properties and for instance set them respectively to
`120` and `10` - the generator will generate activities for the time range between 2 and 10 minutes, so it will
generate the data for the next partition sooner
- `get_random_duration_in_seconds` method and for instance set the range to `random.randint(60, 180)`
2. To generate dataset across different partitions, you can also change the timer's timeshifting to fit into
40th or 50th minute of the hour.