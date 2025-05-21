# GCS Signed URLs Generator using HMAC

This project provides a script to generate signed URLs for Google Cloud Storage (GCS) using HMAC (Hash-based Message
Authentication Code) for authentication. Signed URLs allow you to grant temporary access to private objects in your GCS
buckets.

## Features

- Generate signed URLs for GET, POST, PUT, DELETE, etc.
- Support for different HTTP methods
- Configurable expiration time for signed URLs

## Requirements

- Python 3.6 or later
- Google Cloud Storage library
- Google Auth library

## Installation

1. Clone the repository to your local machine:
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Set the environment variables `ACCESS_KEY` and `SECRET_KEY` with your GCS credentials.
2. Run the `generate_signed_urls_hmac.py` script with the required arguments:
   ```
   python signed_urls/generate_signed_urls_hmac.py <request_method> <region> <bucket_name> <object_name> [expiration]
   ```
    - `request_method`: HTTP method for the signed URL (e.g., GET, POST)
    - `region`: Your Cloud Storage region name
    - `bucket_name`: Your Cloud Storage bucket name
    - `object_name`: Your Cloud Storage object name
    - `expiration`: Expiration time in seconds for the signed URL (max 604800 seconds or 7 days)

3. The script will output the signed URL, which you can use to access the private object in your GCS bucket.

## Example

To generate a signed URL for a GET request to an object named `example.txt` in the `my-bucket` bucket with an expiration
time of 3600 seconds (1 hour):

```
python signed_urls/generate_signed_urls_hmac.py GET us-central1 my-bucket example.txt 3600
```

## Testing

To run the tests for this project, install the testing dependencies:

```
pip install -r requirements-test.txt
```

Then execute the tests using `pytest`:

```
pytest
```

## Contributing

Feel free to submit pull requests or open issues to contribute to this project.

## License

This project is licensed under the Apache 2.0 License. See the `LICENSE` file for details.
