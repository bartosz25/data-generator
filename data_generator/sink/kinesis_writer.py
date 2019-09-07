import time
from collections import defaultdict

import boto3


class KinesisWriterConfiguration:
    def __init__(self, configuration):
        self.streams = []
        for stream_name, stream_configuration in configuration['topics'].items():
            self.streams.append(KinesisStreamConfiguration(stream_name, stream_configuration['shards']))
        self.kinesis_client = boto3.client('kinesis')
        self.records_to_send = defaultdict(lambda: [])

    def create_or_recreate_streams(self):
        streams_to_delete = list(map(lambda topic_spec: topic_spec.name, self.streams))
        for stream in streams_to_delete:
            print('Deleting {}'.format(stream))
            try:
                self.kinesis_client.delete_stream(StreamName=stream)
                stream_is_deleted = False
                while not stream_is_deleted:
                    stream_status = self.kinesis_client.describe_stream(StreamName=stream)
                    if stream_status['StreamDescription']:
                        time.sleep(1)
                    else:
                        stream_is_deleted = True
            except self.kinesis_client.exceptions.ResourceNotFoundException:
                # Ignore this error silently - we don't care if the stream doesn't exist anymore
                pass

        for stream in self.streams:
            print('Creating {}'.format(stream))
            self.kinesis_client.create_stream(StreamName=stream.name, ShardCount=stream.shards)
            # The stream is not created immediately, wait a little before continuing
            stream_is_ready = False
            while not stream_is_ready:
                stream_status = self.kinesis_client.describe_stream(StreamName=stream.name)
                if stream_status['StreamDescription'] \
                        and stream_status['StreamDescription']['StreamStatus'] == 'ACTIVE':
                    stream_is_ready = True
                else:
                    time.sleep(2)

    def send_messages(self, stream_name, message):
        # TODO: try more intelligent partitioning strategy (custom one)
        self.records_to_send[stream_name].append({'Data': message.encode('utf-8'), 'PartitionKey': message[0:10]})
        if len(self.records_to_send[stream_name]) > 10:
            self._send_messages_with_retry(stream_name, self.records_to_send[stream_name])
            self.records_to_send[stream_name] = []

    def _send_messages_with_retry(self, stream_name, messages):
        put_result = self.kinesis_client.put_records(StreamName=stream_name, Records=messages)
        messages_to_resend = []
        for index, result in enumerate(put_result['Records']):
            if 'ErrorCode' in result:
                messages_to_resend.append(messages[index])
        if messages_to_resend:
            self._send_messages_with_retry(stream_name, messages_to_resend)

    def __repr__(self):
        return 'KinesisWriterConfiguration (streams={})'.format(self.streams)


class KinesisStreamConfiguration:
    def __init__(self, name, shards):
        self.name = name
        self.shards = shards

    def __repr__(self):
        return 'Kinesis stream (name={}, shards={})'.format(self.name, self.shards)
