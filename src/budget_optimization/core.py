import boto3
import pandas as pd
import zipfile


def main(
    bucket: str,
    download_folder: str,
    data_file: str,
    indicators: dict[str, str],
):
    downloaded_file = get_opri_file(
        bucket,
        download_folder,
    )
    extract_opri_data(
        download_folder,
        downloaded_file,
        data_file,
    )
    df_data = read_opri_data(
        download_folder,
        data_file,
        indicators,
    )


def get_opri_file(
    bucket: str,
    download_folder: str,
) -> str:
    s3 = boto3.resource("s3")
    file_to_download = sorted(
        [obj.key for obj in s3.Bucket(bucket).objects.all()],
        reverse=True,
    )[0]
    download_path = f"{download_folder}/{file_to_download}"
    s3.Bucket(bucket).download_file(file_to_download, download_path)
    return file_to_download


def extract_opri_data(
    download_folder: str,
    downloaded_file: str,
    file_to_extract: str,
):
    download_path = f"{download_folder}/{downloaded_file}"
    with zipfile.ZipFile(download_path, "r") as myzip:
        myzip.extract(file_to_extract, download_folder)


def read_opri_data(
    download_folder: str,
    extracted_file: str,
    indicators: dict[str, str],
) -> pd.DataFrame:
    filepath = f"{download_folder}/{extracted_file}"
    df = (
        pd.read_csv(filepath)
        .rename(str.lower, axis="columns")
        .loc[lambda df: df["indicator_id"].isin(indicators.keys())]
    )
    return df


if __name__ == "__main__":
    main(
        "lee-budget-optimization",
        "tmp",
        "OPRI_DATA_NATIONAL.csv",
        {
            "X.US.1.FSGOV": "expenditure_primary",
            "X.US.2T3.FSGOV": "expenditure_secondary",
            "20062": "enrollment_primary",
            "20082": "enrollment_secondary",
            "PRP.1": "private_primary",
            "PRP.2T3": "private_secondary",
        },
    )
