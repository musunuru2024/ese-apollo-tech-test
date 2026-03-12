"""Simple S3 reader utilities.

Provides helper functions to read an S3 object as bytes or text and a small
CLI for quick use. Uses boto3 and respects environment credentials or an
optional AWS profile.

Usage examples:
  python s3_reader.py --bucket my-bucket --key path/to/file.txt
  python s3_reader.py --bucket my-bucket --key path/to/file.txt --output out.txt

Notes:
  - Credentials are loaded from environment, instance/role metadata, or an
    AWS profile if --profile is provided.
  - For large objects consider streaming directly to disk instead of loading
    into memory.
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def _s3_client(region: Optional[str] = None, profile: Optional[str] = None):
    """Create a boto3 S3 client using an optional profile and region.

    If profile is provided a Session will be created with that profile. If not,
    the default session/credentials chain is used.
    """
    if profile:
        session = boto3.Session(profile_name=profile)
        return session.client("s3", region_name=region)
    return boto3.client("s3", region_name=region)


def read_s3_bytes(bucket: str, key: str, region: Optional[str] = None, profile: Optional[str] = None) -> bytes:
    """Download an S3 object and return its content as bytes.

    Raises ClientError or BotoCoreError on failure.
    """
    client = _s3_client(region=region, profile=profile)
    try:
        resp = client.get_object(Bucket=bucket, Key=key)
        body = resp["Body"].read()
        return body
    except ClientError:
        # propagate ClientError (e.g. NoSuchKey, NoSuchBucket, AccessDenied)
        raise
    except BotoCoreError:
        # network/credentials/other botocore errors
        raise


def read_s3_text(bucket: str, key: str, encoding: str = "utf-8", region: Optional[str] = None, profile: Optional[str] = None) -> str:
    """Download an S3 object and return its content decoded as text.

    This simply calls read_s3_bytes() and decodes using the provided
    encoding. It will raise the same exceptions as read_s3_bytes.
    """
    data = read_s3_bytes(bucket=bucket, key=key, region=region, profile=profile)
    return data.decode(encoding)


def _parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Read an S3 object and print or save it")
    p.add_argument("--bucket", required=True, help="S3 bucket name")
    p.add_argument("--key", required=True, help="Object key in the bucket")
    p.add_argument("--profile", help="AWS profile name to use (optional)")
    p.add_argument("--region", help="AWS region to use for the client (optional)")
    p.add_argument("--output", help="Write the object to this local file instead of stdout")
    p.add_argument("--binary", action="store_true", help="Treat object as binary (don't decode)")
    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = _parse_args(argv)
    try:
        if args.binary:
            data = read_s3_bytes(args.bucket, args.key, region=args.region, profile=args.profile)
            if args.output:
                with open(args.output, "wb") as f:
                    f.write(data)
                print(f"Wrote {len(data)} bytes to {args.output}")
            else:
                # Write bytes to stdout buffer
                sys.stdout.buffer.write(data)
        else:
            text = read_s3_text(args.bucket, args.key, region=args.region, profile=args.profile)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"Wrote {len(text)} characters to {args.output}")
            else:
                print(text)
        return 0
    except ClientError as e:
        print(f"S3 client error: {e}", file=sys.stderr)
        return 2
    except BotoCoreError as e:
        print(f"BotoCore error: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
