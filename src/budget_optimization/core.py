import boto3


def get_opri_data(
    bucket: str = "lee-budget-optimization",
    key: str = "OPRI_202303.zip",
    filename: str = "tmp/OPRI_202303.zip",
):
    s3 = boto3.client("s3")
    s3.download_file(bucket, key, filename)


if __name__ == "__main__":
    get_opri_data("lee-budget-optimization", "OPRI_202303.zip", "tmp/OPRI_202303.zip")
