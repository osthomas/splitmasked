import pytest
import pkg_resources

from splitmasked import io, split


@pytest.fixture
def input1_stream():
    return io.stream(pkg_resources.resource_filename("tests.resources", "input1.fastq"))


def _test_with_parameters(
        infile,
        expected_out_masked,
        expected_out_unmasked,
        parameters,
        tmp_path):
    infile = pkg_resources.resource_filename("tests.resources", infile)
    with open(pkg_resources.resource_filename("tests.resources", expected_out_masked), "r") as f:
        expect_masked = f.read()
    with open(pkg_resources.resource_filename("tests.resources", expected_out_unmasked), "r") as f:
        expect_unmasked = f.read()

    out_unmasked = tmp_path / "out_unmasked"
    out_masked = tmp_path / "out_masked"
    with open(out_unmasked, "w") as fh_unmasked, open(out_masked, "w") as fh_masked:
        split.split_masked(infile, fh_unmasked, fh_masked, **parameters)
    with open(out_unmasked, "r") as fh_unmasked, open(out_masked, "r") as fh_masked:
        result_unmasked = fh_unmasked.read()
        result_masked = fh_masked.read()
    assert expect_unmasked == result_unmasked
    assert expect_masked == result_masked


def test_nofilter(tmp_path):
    infile = "input1.fastq"
    expected_out_unmasked = "output1_unmasked.fastq"
    expected_out_masked = "output1_masked.fastq"
    parameters = {
        "maskchar": "lowercase",
        "minlength_masked": 0,
        "minlength_unmasked": 0,
        "revert_lowercase": False,
    }
    _test_with_parameters(infile, expected_out_masked, expected_out_unmasked, parameters, tmp_path)


def test_revert_lowercase(tmp_path):
    infile = "input1.fastq"
    expected_out_unmasked = "output1_unmasked_revert.fastq"
    expected_out_masked = "output1_masked_revert.fastq"
    parameters = {
        "maskchar": "lowercase",
        "minlength_masked": 0,
        "minlength_unmasked": 0,
        "revert_lowercase": True,
    }
    _test_with_parameters(infile, expected_out_masked, expected_out_unmasked, parameters, tmp_path)


def test_minlength(tmp_path):
    infile = "input1.fastq"
    expected_out_unmasked = "output1_unmasked_minlength.fastq"
    expected_out_masked = "output1_masked_minlength.fastq"
    parameters = {
        "maskchar": "lowercase",
        "minlength_masked": 5,
        "minlength_unmasked": 7,
        "revert_lowercase": False,
    }
    _test_with_parameters(infile, expected_out_masked, expected_out_unmasked, parameters, tmp_path)
