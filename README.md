# ese-apollo-tech-test

A tiny sample project that provides a helper to read files from Amazon S3.

This repository contains a small Python utility, `s3_reader.py`, which exposes
convenient functions and a CLI for downloading S3 objects as text or bytes.

Why this exists
- Quick helper for demos, scripts, or small tools that need to fetch objects
	from S3 without pulling in a large codebase.

What is included
- `s3_reader.py` — functions and a small CLI to read an S3 object:
	- read_s3_bytes(bucket, key, region=None, profile=None) -> bytes
	- read_s3_text(bucket, key, encoding='utf-8', region=None, profile=None) -> str
	- CLI with flags: `--bucket`, `--key`, `--output`, `--binary`, `--profile`, `--region`

Requirements
- Python 3.8+
- boto3

Install

Install the runtime dependency (recommended into a virtualenv):

```bash
python -m pip install --user boto3
```

Usage examples

Print a text file from S3 to stdout:

```bash
python s3_reader.py --bucket my-bucket --key path/to/file.txt
```

Save a text object to disk:

```bash
python s3_reader.py --bucket my-bucket --key path/to/file.txt --output out.txt
```

Download a binary object and write raw bytes:

```bash
python s3_reader.py --bucket my-bucket --key path/to/image.png --binary --output image.png
```

Use a specific AWS profile or region:

```bash
python s3_reader.py --bucket my-bucket --key path/to/file.txt --profile myprofile --region us-east-1
```

Notes
- Authentication uses boto3's standard credential chain (environment,
	shared credentials file/profile, or instance role). For large objects,
	consider streaming to disk instead of loading into memory.

Contributing
- Small, non-sensitive changes can be proposed via pull requests. If you add
	new functionality, please include tests where practical.

License
- Please add a license if you intend to make this repo public.
# ese-apollo-tech-test
