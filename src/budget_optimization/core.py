import boto3


def main(
    bucket: str = "lee-budget-optimization",
    key: str = "OPRI_202303.zip",
    filename: str = "tmp/OPRI_202303.zip",
):
    get_opri_data(bucket, key, filename)


def get_opri_data(
    bucket: str,
    key: str,
    filename: str,
):
    s3 = boto3.client("s3")
    s3.download_file(bucket, key, filename)


if __name__ == "__main__":
    bucket: str = "lee-budget-optimization"
    key: str = "OPRI_202303.zip"
    filename: str = "tmp/OPRI_202303.zip"
    main(bucket, key, filename)
