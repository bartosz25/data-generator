class UnorderedDataContainer:
    """
    :param must_buffer_data: A function that should return True if the verified action should be buffered.
    """
    def __init__(self, must_buffer_data):
        self.__buffered_actions = []
        self.__must_buffer_data = must_buffer_data

    def wrap_action(self, generated_action, send_method):
        if self.__must_buffer_data():
            self.__buffered_actions.append(generated_action)
        else:
            send_method(generated_action)

    def send_buffered_actions(self, send_method):
        if self.__buffered_actions:
            print('Sending late events {}'.format(self.__buffered_actions))
        for late_action in self.__buffered_actions:
            send_method(late_action)

        self.__buffered_actions = []

    @property
    def all_buffered_actions(self):
        return self.__buffered_actions