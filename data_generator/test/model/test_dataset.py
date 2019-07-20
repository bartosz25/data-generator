from assertpy import assert_that

from data_generator.model.dataset import Dataset


def should_generate_pages_map():
    page_map = Dataset.create_page_map()

    expected_map = {'category 17': [
        'category 1', 'category 2', 'category 3', 'category 4', 'category 5', 'category 6',
        'category 7', 'category 8', 'category 9', 'category 10', 'category 11', 'category 12',
        'category 13', 'category 14', 'category 15', 'category 16', 'category 17', 'category 18',
        'category 19', 'category 20', 'category 21', 'category 22', 'category 23', 'category 24',
        'category 25', 'index', 'about', 'my-account', 'article category 17-1', 'article category 17-2',
        'article category 17-3', 'article category 17-4', 'article category 17-5',
        'article category 17-6', 'article category 17-7', 'article category 17-8',
        'article category 17-9', 'article category 17-10', 'article category 17-11',
        'article category 17-12', 'article category 17-13', 'article category 17-14',
        'article category 17-15', 'article category 17-16', 'article category 17-17', 'article category 17-18',
        'article category 17-19', 'article category 17-20', 'article category 17-21', 'article category 17-22',
        'article category 17-23', 'article category 17-24', 'article category 17-25'
    ], 'article category 25-17': [
        'category 1', 'category 2', 'category 3', 'category 4', 'category 5', 'category 6', 'category 7',
        'category 8', 'category 9', 'category 10', 'category 11', 'category 12', 'category 13', 'category 14',
        'category 15', 'category 16', 'category 17', 'category 18', 'category 19', 'category 20', 'category 21',
        'category 22', 'category 23', 'category 24', 'category 25', 'index', 'about', 'my-account'
    ], 'about': [
        'index', 'about', 'my-account', 'category 1', 'category 2', 'category 3', 'category 4', 'category 5',
        'category 6', 'category 7', 'category 8', 'category 9', 'category 10', 'category 11', 'category 12',
        'category 13', 'category 14', 'category 15', 'category 16', 'category 17', 'category 18', 'category 19',
        'category 20', 'category 21', 'category 22', 'category 23', 'category 24', 'category 25'
    ]}

    for page_name, linked_pages in expected_map.items():
        assert_that(page_map[page_name]).contains_sequence(*linked_pages)


def should_create_correct_apps_distribution():
    versions_distribution = Dataset.create_versions_distribution(50, 10, 10, 80)

    versions_count = {'v1': 0, 'v2': 0, 'v3': 0}
    for version in versions_distribution:
        versions_count[version] += 1

    assert_that(versions_count['v1']).is_equal_to(5)
    assert_that(versions_count['v2']).is_equal_to(5)
    assert_that(versions_count['v3']).is_equal_to(40)
