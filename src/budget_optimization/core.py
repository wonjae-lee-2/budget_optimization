import boto3
import zipfile


def main(
    bucket: str,
    download_folder: str,
    filelist: list[str],
):
    filename = get_opri_data(bucket, download_folder)
    extract_opri_data(download_folder, filename, filelist)


def get_opri_data(
    bucket: str,
    download_folder: str,
) -> str:
    s3 = boto3.resource("s3")
    filename = sorted(
        [obj.key for obj in s3.Bucket(bucket).objects.all()], reverse=True
    )[0]
    download_path = f"{download_folder}/{filename}"
    s3.Bucket(bucket).download_file(filename, download_path)
    return filename


def extract_opri_data(
    download_folder: str,
    filename: str,
    filelist: list[str],
):
    download_path = f"{download_folder}/{filename}"
    with zipfile.ZipFile(download_path, "r") as myzip:
        for file in filelist:
            if file in myzip.namelist():
                myzip.extract(file, download_folder)


if __name__ == "__main__":
    main("lee-budget-optimization", "tmp", ["OPRI_DATA_NATIONAL.csv", "OPRI_LABEL.csv"])
