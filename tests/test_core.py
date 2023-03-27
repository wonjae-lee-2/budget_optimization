import pytest
from budget_optimization import core
from pathlib import Path


@pytest.fixture
def test_bucket():
    return "lee-budget-optimization-tests"


@pytest.fixture(scope="session")
def test_download_folder(tmp_path_factory):
    return tmp_path_factory.mktemp("tmp").as_posix()


@pytest.fixture
def test_zip_file():
    return "OPRI_230221.zip"


@pytest.fixture
def test_data_file():
    return "OPRI_DATA_NATIONAL.csv"


@pytest.fixture
def test_opri_indicators():
    return {
        "X.US.1.FSGOV": "expenditure_primary",
        "X.US.2T3.FSGOV": "expenditure_secondary",
        "20062": "enrollment_primary",
        "20082": "enrollment_secondary",
        "PRP.1": "private_primary",
        "PRP.2T3": "private_secondary",
    }


@pytest.fixture
def test_wb_indicators():
    return {
        "NY.GDP.MKTP.KD.ZG": "gdp_growth",
        "SP.POP.GROW": "population_growth",
    }


def test_get_opri_file(
    test_bucket,
    test_zip_file,
    test_download_folder,
):

    filename = core.get_opri_file(
        test_bucket,
        test_download_folder,
    )

    assert filename == test_zip_file
    assert Path(f"{test_download_folder}/{filename}").exists()


def test_extract_opri_data(
    test_zip_file,
    test_data_file,
    test_download_folder,
):

    core.extract_opri_data(
        test_download_folder,
        test_zip_file,
        test_data_file,
    )

    assert Path(f"{test_download_folder}/{test_data_file}").exists()


def test_read_opri_data(
    test_download_folder,
    test_data_file,
    test_opri_indicators,
):

    df = core.read_opri_data(
        test_download_folder,
        test_data_file,
        test_opri_indicators,
    )

    assert df.shape == (9069, 8)


def test_get_wb_data(
    test_wb_indicators,
):

    df = core.get_wb_data(
        test_wb_indicators,
    )

    assert df.shape == (5852, 5)
