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

Running tests
--------------

When you add a new file or update code, run the test suite locally before pushing.
Use a virtual environment or install the test dependencies into your user site-packages:

```bash
python3 -m pip install --user -r requirements.txt
```

Run the full test suite:

```bash
python3 -m pytest
```

Run quietly (short output):

```bash
python3 -m pytest -q
```

Run tests for a single test file (useful after adding a new test file):

```bash
python3 -m pytest tests/test_newfile.py
```

Run a single test by node id:

```bash
python3 -m pytest tests/test_newfile.py::test_specific_behavior
```

Run tests matching a keyword expression (quick local selection):

```bash
python3 -m pytest -k "keyword"
```

Continuous Integration
----------------------

This repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that
runs the test suite on push and pull requests against Python 3.8–3.11. After pushing
your changes, the CI will run automatically. Check the Actions tab in GitHub for results.

Tips
- Prefer working inside a virtualenv: `python3 -m venv .venv && source .venv/bin/activate`
- Add tests for new behavior and run them locally before pushing.
# ese-apollo-tech-test
