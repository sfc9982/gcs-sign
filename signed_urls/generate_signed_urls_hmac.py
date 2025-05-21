import argparse
import datetime
import hashlib
import hmac
import os
import sys
from urllib.parse import quote

import six

algorithm = 'GOOG4-HMAC-SHA256'
http_method = 'GET'
signed_headers = 'host'

ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
service = 'storage'
request_type = 'goog4_request'

datetime_now = datetime.datetime.now(tz=datetime.timezone.utc)
request_timestamp = datetime_now.strftime('%Y%m%dT%H%M%SZ')
datestamp = datetime_now.strftime('%Y%m%d')

expiration = '30'  # seconds


def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def get_signature_key(key, datestamp, regionName, serviceName):
    key_date = sign(('GOOG4' + key).encode('utf-8'), datestamp)
    key_region = sign(key_date, regionName)
    key_service = sign(key_region, serviceName)
    signing_key = sign(key_service, 'goog4_request')
    return signing_key


def generate_signed_url(
        region,
        bucket_name,
        object_name,
        expiration=600,
        http_method='GET',
        query_parameters=None,
        headers=None,
):
    if expiration > 604800:
        print('Expiration Time can\'t be longer than 604800 seconds (7 days).')
        sys.exit(1)

    escaped_object_name = quote(six.ensure_binary(object_name), safe=b'/~')
    host = f'{bucket_name}.storage.googleapis.com'
    canonical_uri = f'/{escaped_object_name}'
    credential_scope = f'{datestamp}/{region}/{service}/{request_type}'

    canonical_headers = (
        f'X-Goog-Algorithm={algorithm}'
        f'&X-Goog-Credential={quote(ACCESS_KEY + '/' + credential_scope, safe='')}'
        f'&X-Goog-Date={request_timestamp}'
        f'&X-Goog-Expires={expiration}'
        f'&X-Goog-SignedHeaders={signed_headers}\n'
        f'host:{host}'
    )
    canonical_request = (
        f'{http_method}\n'
        f'{canonical_uri}\n'
        f'{canonical_headers}\n\n'
        f'{signed_headers}\n'
        f'UNSIGNED-PAYLOAD'
    )
    string_to_sign = (
        f'{algorithm}\n'
        f'{request_timestamp}\n'
        f'{credential_scope}\n'
        f'{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}'
    )

    signing_key = get_signature_key(SECRET_KEY, datestamp, region, service)

    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

    scheme_and_host = '{}://{}'.format('https', host)
    signed_url = (
        f'{scheme_and_host}'
        f'{canonical_uri}'
        f'?X-Goog-Algorithm={algorithm}'
        f'&X-Goog-Credential={ACCESS_KEY}/{credential_scope}'
        f'&X-Goog-Date={request_timestamp}'
        f'&X-Goog-Expires={expiration}'
        f'&X-Goog-SignedHeaders={signed_headers}'
        f'&X-Goog-Signature={signature}'
    )

    return signed_url


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('request_method', help='A request method, e.g GET, POST.')
    parser.add_argument('region', help='Your Cloud Storage region name.')
    parser.add_argument('bucket_name', help='Your Cloud Storage bucket name.')
    parser.add_argument('object_name', help='Your Cloud Storage object name.')
    parser.add_argument('expiration', type=int, help='Expiration time.')

    args = parser.parse_args()

    signed_url = generate_signed_url(
        region=args.region,
        http_method=args.request_method,
        bucket_name=args.bucket_name,
        object_name=args.object_name,
        expiration=int(args.expiration),
    )

    print(signed_url)
