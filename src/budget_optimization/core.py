import boto3
import pandas as pd
import zipfile


def main(
    bucket: str,
    download_folder: str,
    filedict: dict[str, str],
    indicators: list[str],
):
    filename = get_opri_zipfile(
        bucket,
        download_folder,
    )
    extract_opri_files(
        download_folder,
        filename,
        filedict,
    )
    df_label = read_opri_label(
        download_folder,
        filedict,
        indicators,
    )
    df_data = read_opri_data(
        download_folder,
        filedict,
        indicators,
    )


def get_opri_zipfile(
    bucket: str,
    download_folder: str,
) -> str:
    s3 = boto3.resource("s3")
    filename = sorted(
        [obj.key for obj in s3.Bucket(bucket).objects.all()],
        reverse=True,
    )[0]
    download_path = f"{download_folder}/{filename}"
    s3.Bucket(bucket).download_file(filename, download_path)
    return filename


def extract_opri_files(
    download_folder: str,
    filename: str,
    filedict: dict[str, str],
):
    download_path = f"{download_folder}/{filename}"
    with zipfile.ZipFile(download_path, "r") as myzip:
        for file in filedict.values():
            if file in myzip.namelist():
                myzip.extract(file, download_folder)


def read_opri_label(
    download_folder: str,
    filedict: dict[str, str],
    indicators: list[str],
) -> pd.DataFrame:
    filepath = f"{download_folder}/{filedict['label']}"
    df = (
        pd.read_csv(filepath)
        .rename(str.lower, axis="columns")
        .loc[lambda df: df["indicator_id"].isin(indicators)]
    )
    return df


def read_opri_data(
    download_folder: str,
    filedict: dict[str, str],
    indicators: list[str],
) -> pd.DataFrame:
    filepath = f"{download_folder}/{filedict['data']}"
    df = (
        pd.read_csv(filepath)
        .rename(str.lower, axis="columns")
        .loc[lambda df: df["indicator_id"].isin(indicators)]
    )
    return df


if __name__ == "__main__":
    main(
        "lee-budget-optimization",
        "tmp",
        {
            "label": "OPRI_LABEL.csv",
            "data": "OPRI_DATA_NATIONAL.csv",
        },
        [
            "X.US.1.FSGOV",
            "X.US.2T3.FSGOV",
            "20062",
            "20082",
            "PRP.1",
            "PRP.2T3",
        ],
    )
