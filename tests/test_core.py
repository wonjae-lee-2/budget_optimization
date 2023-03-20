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
def test_filedict():
    return {
        "label": "OPRI_LABEL.csv",
        "data": "OPRI_DATA_NATIONAL.csv",
    }


@pytest.fixture
def test_filename():
    return "OPRI_230221.zip"


@pytest.fixture
def test_indicators():
    return [
        "X.US.1.FSGOV",
        "X.US.2T3.FSGOV",
        "20062",
        "20082",
        "PRP.1",
        "PRP.2T3",
    ]


def test_get_opri_zipfile(
    test_bucket,
    test_filename,
    test_download_folder,
):

    filename = core.get_opri_zipfile(
        test_bucket,
        test_download_folder,
    )

    assert filename == test_filename
    assert Path(f"{test_download_folder}/{filename}").exists()


def test_extract_opri_files(
    test_filename,
    test_filedict,
    test_download_folder,
):

    core.extract_opri_files(
        test_download_folder,
        test_filename,
        test_filedict,
    )

    for file in test_filedict.values():
        assert Path(f"{test_download_folder}/{file}").exists()


def test_read_opri_label(
    test_download_folder,
    test_filedict,
    test_indicators,
):

    df = core.read_opri_label(
        test_download_folder,
        test_filedict,
        test_indicators,
    )

    assert df.shape == (6, 2)


def test_read_opri_data(
    test_download_folder,
    test_filedict,
    test_indicators,
):

    df = core.read_opri_data(
        test_download_folder,
        test_filedict,
        test_indicators,
    )

    assert df.shape == (31812, 6)
