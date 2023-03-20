from budget_optimization import core
from pathlib import Path


def test_get_opri_data():
    bucket: str = "lee-budget-optimization"
    key: str = "OPRI_202303.zip"
    filename: str = "tmp/OPRI_202303.zip"

    core.get_opri_data(bucket, key, filename)

    assert Path(filename).exists()

    Path(filename).unlink()
