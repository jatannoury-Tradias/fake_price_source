import hashlib
import http

from app.authentication.header_param_protocol import HeaderParamProtocol
from app.config.customers import customers


def test_process_request_positive():
    protocol = HeaderParamProtocol(None, None)
    test_token = "a"
    headers = {
        "Authorization": f"{test_token}"
    }
    response = protocol.process_request("", headers)
    assert response is None

    token_hashes_dict = {customer.token_hash: customer for customer in customers}
    token_hash = hashlib.sha256(bytes(test_token, "utf-8")).hexdigest()
    assert protocol.customer == token_hashes_dict[token_hash]


def test_process_request_negative_no_header():
    protocol = HeaderParamProtocol(None, None)
    test_token = "a"
    headers = {}
    response = protocol.process_request("", headers)
    assert response == (http.HTTPStatus.UNAUTHORIZED, [], b'Invalid token\n')


def test_process_request_negative_invalid_token():
    protocol = HeaderParamProtocol(None, None)
    test_token = "INVALID!"
    headers = {
        "Authorization": f"{test_token}"
    }
    response = protocol.process_request("", headers)
    assert response == (http.HTTPStatus.UNAUTHORIZED, [], 'Unauthorized')