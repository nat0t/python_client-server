import pytest
from . import server
from . import client
import pickle
from time import time


@pytest.fixture(scope='function')
def resource_setup():
    request = {
        'action': 'presence',
        'time': time(),
        'type': 'status',
        'user': {
            'account_name': 'user',
            'status': 'status'
        }
    }
    pickled_request = pickle.dumps(request)
    response = {'response': 200, 'time': time(), 'alert': 'OK'}
    pickled_response = pickle.dumps(response)
    return request, pickled_request, response, pickled_response


def test_server_get_request_presence(resource_setup):
    assert server.get_request(resource_setup[1]) == resource_setup[0]


def test_server_get_request_error():
    assert server.get_request(None) == {}


def test_server_prepare_response_200(resource_setup):
    assert server.prepare_response(200) == resource_setup[2]


def test_server_prepare_response_incorrect_code():
    assert server.prepare_response(500) is None


def test_server_set_response_with_dict(resource_setup):
    assert server.set_response(resource_setup[0]) == resource_setup[3]


def test_server_set_response_incorrect_arg():
    assert server.set_response(None) == b''


def test_client_set_request_presence(resource_setup):
    assert client.set_request('presence', 'user', 'status') == \
           resource_setup[1]


def test_client_get_response_with_dict(resource_setup):
    assert client.get_response(resource_setup[3]) == resource_setup[2]


def test_client_get_response_incorrect_arg():
    assert client.get_response(None) == {}
