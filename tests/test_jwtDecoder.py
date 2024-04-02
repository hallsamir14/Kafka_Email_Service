import pytest
from unittest.mock import patch, MagicMock
from app.jwt_decoder.decoder import readUser

# Test for markdown to HTML conversion
def test_readUser():
    decoded_token = readUser('app/jwt_decoder/token.txt') 

    #expected output for sample token
    expected_decoded_token = {'token': {'test-data': 'auth0-flow-https://auth0.com/blog/adding-custom-claims-to-id-token-with-auth0-actions/', 'nickname': 'bzs6+testacct', 'name': 'bzs6+testacct@njit.edu', 'picture': 'https://s.gravatar.com/avatar/ddfb6d7752bedb5e2bd297d94f0bdd07?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fbz.png', 'updated_at': '2024-02-24T00:30:28.987Z', 'email': 'bzs6+testacct@njit.edu', 'email_verified': True, 'iss': 'https://is373-dev.us.auth0.com/', 'aud': 'OGylLwgho8mHKBg6cE9i293QDIAEuG1Y', 'iat': 1708734630, 'exp': 1708770630, 'sub': 'auth0|65c6755d5a130b87df96f200', 'sid': 'gOe1xZy8K99P90DZaULH39Thx9o91O-2', 'nonce': 's_majaXr-N3-6pHEp2riAVD9yv2gFRVi8vDpnLQS2wA'}}  
    assert decoded_token == expected_decoded_token


if __name__ == "__main__":
    pytest.main()
