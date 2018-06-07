import pytest
import logging

logging.basicConfig(level=logging.DEBUG)

# Modules under test
import isd_api_server

# Modules from which to load exceptions
import requests.exceptions

# Data used for tests

isd_payload = {'name': 'Ben West',
           'email': 'ben.west.500@gmail.com',
           'subject': 'Hello',
           'message': 'Hello, Im interested in comming for try dive'}


# Helper functions
def send_test_isd_message_payload(host='localhost', port=5000):
    url = "http://{}:{}/api/message".format(host, port)
    referer = "https://{}/contact".format(host)
    req = requests.request(method='POST', url=url,
                           headers={'Referer': referer},
                           data=isd_payload, allow_redirects=False)
    return req.status_code


# BEGIN TESTS
def test_send_test_isd_message_payload_badhost():
    with pytest.raises(requests.exceptions.ConnectionError):
        send_test_isd_message_payload('nothing')


def test_send_test_isd_message_payload_good_302_response():
    assert send_test_isd_message_payload() == 302


def test_write_to_sns_topic():
    assert isd_api_server.write_to_sns_topic(isd_payload['name'],
                                             isd_payload['email'],
                                             isd_payload['subject'],
                                             isd_payload['message']) is True


def test_write_to_sns_topic_odd_chars_in_message():
    custom_messages = \
        [""""!"£%$^(&*)&(*%^}{}{:}).,./.,QWedfgopeqFEGWROJ321%!"$!¬`¬""",
         """;-hEloo2!fa"$"""]
    for test in custom_messages:
        assert isd_api_server.write_to_sns_topic(isd_payload['name'],
                                                 isd_payload['email'],
                                                 isd_payload['subject'],
                                                 test) is False


def test_write_to_sns_topic_newlines_in_message():
    custom_messages = \
        [""""Hello\nWith\nUnix\nnewlines...""",
         """Hello\r\nwith\r\nmsdos\r\nnewlines"""]
    for test in custom_messages:
        assert isd_api_server.write_to_sns_topic(isd_payload['name'],
                                                 isd_payload['email'],
                                                 isd_payload['subject'],
                                                 test) is True


def test_write_to_sns_topic_missing_email():
    assert isd_api_server.write_to_sns_topic(isd_payload['name'],
                                             "",
                                             isd_payload['subject'],
                                             isd_payload['message']) is False


def test_write_to_sns_topic_missing_message():
    assert isd_api_server.write_to_sns_topic(isd_payload['name'],
                                             isd_payload['email'],
                                             isd_payload['subject'],
                                             "") is False



