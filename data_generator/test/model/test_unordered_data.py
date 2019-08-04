from assertpy import assert_that

from data_generator.model.unordered_data import UnorderedDataContainer


def should_wrap_an_action_and_buffer_it_as_late_event():
    unordered_data_container = UnorderedDataContainer(lambda: True)

    unordered_data_container.wrap_action('action1', None)
    unordered_data_container.wrap_action('action2', None)

    assert_that(unordered_data_container.all_buffered_actions).is_length(2).contains_only('action1', 'action2')


def should_wrap_an_action_and_not_buffer_it_as_late_event():
    wrapped_data = []
    unordered_data_container = UnorderedDataContainer(lambda: False)

    unordered_data_container.wrap_action('action1', lambda action: wrapped_data.append(action))
    unordered_data_container.wrap_action('action2', lambda action: wrapped_data.append(action))

    assert_that(unordered_data_container.all_buffered_actions).is_empty()
    assert_that(wrapped_data).is_length(2).contains_only('action1', 'action2')


def should_send_unordered_actions():
    wrapped_data = []
    unordered_data_container = UnorderedDataContainer(lambda: True)
    unordered_data_container.wrap_action('action1', None)
    unordered_data_container.wrap_action('action2', None)

    unordered_data_container.send_buffered_actions(lambda action: wrapped_data.append(action))

    assert_that(unordered_data_container.all_buffered_actions).is_empty()
    assert_that(wrapped_data).is_length(2).contains_only('action1', 'action2')
