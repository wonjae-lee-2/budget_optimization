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
def test_filelist():
    return ["OPRI_DATA_NATIONAL.csv", "OPRI_LABEL.csv"]


@pytest.fixture
def test_filename():
    return "OPRI_230221.zip"


def test_get_opri_data(test_bucket, test_filename, test_download_folder):

    filename = core.get_opri_data(test_bucket, test_download_folder)

    assert filename == test_filename
    assert Path(f"{test_download_folder}/{filename}").exists()


def test_extract_opri_data(test_filename, test_filelist, test_download_folder):

    core.extract_opri_data(test_download_folder, test_filename, test_filelist)

    for file in test_filelist:
        assert Path(f"{test_download_folder}/{file}").exists()
