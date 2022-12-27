import http
import websockets
import hashlib

from app.config.customers import customers
token_hashes_dict = {customer.token_hash: customer for customer in customers}


class HeaderParamProtocol(websockets.WebSocketServerProtocol):
    def process_request(self, path, headers):
        """
        Interceptor to authenticate the user.

        Will add the attribute <customer> to the object in case of successful authentication.
        Will raise an Unauthorized error, if the authentication fails.

        Args:
            path: passed from websocket instance
            headers: passed from websocket instance

        Returns: None

        """
        token = headers['Authorization'] if 'Authorization' in headers else None
        if token is None:
            return http.HTTPStatus.UNAUTHORIZED, [], b'Invalid token\n'
        try:
            token_hash = hashlib.sha256(bytes(token, "utf-8")).hexdigest()
            assert token_hash in token_hashes_dict.keys()
            self.customer = token_hashes_dict[token_hash]
            return None
        except Exception as error:
            return http.HTTPStatus.UNAUTHORIZED, [], 'Unauthorized'