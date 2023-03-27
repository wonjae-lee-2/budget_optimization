import boto3
import pandas as pd
import requests
import zipfile


def main(
    bucket: str,
    download_folder: str,
    data_file: str,
    opri_indicators: dict[str, str],
    wb_indicators: dict[str, str],
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
    df_opri = read_opri_data(
        download_folder,
        data_file,
        opri_indicators,
    )
    df_wb = get_wb_data(
        wb_indicators,
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
        .drop(columns=["magnitude", "qualifier"])
        .loc[lambda df: df["indicator_id"].isin(indicators.keys())]
        .assign(indicator_desc=lambda df: df["indicator_id"].map(indicators))
        .drop(columns="indicator_id")
        .pivot(
            values="value",
            index=["country_id", "year"],
            columns="indicator_desc",
        )
        .rename_axis(None, axis="columns")
        .reset_index()
        .assign(expenditure_primary=lambda df: df["expenditure_primary"] * 1000000)
        .assign(expenditure_secondary=lambda df: df["expenditure_secondary"] * 1000000)
        .assign(private_primary=lambda df: df["private_primary"] / 100)
        .assign(private_secondary=lambda df: df["private_secondary"] / 100)
    )
    return df


def get_wb_data(indicators: dict[str, str]) -> pd.DataFrame:
    dict = {
        key: []
        for key in [
            "country",
            "country_id",
            "year",
            "value",
            "indicator_desc",
        ]
    }
    for key in indicators.keys():
        r = requests.get(
            f"http://api.worldbank.org/v2/country/all/indicator/{key}?date=2000:2023&format=json&per_page=30000"
        )
        for x in r.json()[1]:
            dict["country"].append(x["country"]["value"])
            dict["country_id"].append(x["countryiso3code"])
            dict["year"].append(x["date"])
            dict["value"].append(x["value"])
            dict["indicator_desc"].append(indicators[key])
    df = (
        pd.DataFrame(dict)
        .pivot(
            values="value",
            index=["country", "country_id", "year"],
            columns="indicator_desc",
        )
        .rename_axis(None, axis="columns")
        .reset_index()
        .assign(gdp_growth=lambda df: df["gdp_growth"] / 100)
        .assign(population_growth=lambda df: df["population_growth"] / 100)
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
        {
            "NY.GDP.MKTP.KD.ZG": "gdp_growth",
            "SP.POP.GROW": "population_growth",
        },
    )
