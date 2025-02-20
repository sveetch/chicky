import json
from freezegun import freeze_time

from chicky.cli.entrypoint import main


def test_cli_source_required(capsys, settings):
    """
    Positional argument 'source' is required.
    """
    try:
        main([])
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert captured.out == ""
    msg = "error: the following arguments are required: DIRECTORY_PATH"
    assert msg in captured.err


@freeze_time("2012-10-15 10:00:00")
def test_cli_basic(capsys, settings):
    """
    With only the 'source' positional argument all files are collected and checksummed.
    """
    sample_structure = settings.fixtures_path / "sample_structure"

    try:
        main(["", str(sample_structure)])
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert captured.err == ""
    assert len(captured.out) > 0
    assert json.loads(captured.out) == {
        "created": "2012-10-15T10:00:00",
        "basedir": str(sample_structure),
        "extensions": None,
        "files": {
            "empty.txt": "3345524abf6bbe1809449224b5972c41790b6cf2",
            "images/logo.png": "af9d9cee847018416da2bc5eb2011a04a1945bd7",
            "images/furo-adjustments.css": "abac58d43616bc9360d3c08524650f050a3fe616",
            "images/favicon.ico": "da000da74d8613672fa817b07cdad21b1dc9913f",
            "images/lotus/logo.png": "4011d3757eeb983b286c6560ee5880d52d70181a",
            "images/lotus/favicon.ico": "45e82276182efeb2aa2ebc388910ff48f2d9a3e1",
            "images/atoum/logo.png": "e372449fc103593878b40fd467c48353fd7d4f5a",
            "images/atoum/favicon.ico": "76a711c735bcf7403dc15c9c762af08182e0e623",
            "css/bootstrap.css": "b5b31416eb16e75e8d35469467229af5954d7ebf",
            "css/vendor/bootstrap-icons.css": (
                "6e3587086a462623cb250321b4cbb37208827f96"
            ),
            "css/parts/bootstrap-reboot.css": (
                "c14bf2282a74232929071e7c8711bf501cdfa02e"
            ),
            "css/parts/bootstrap-grid.css": "8a4e912ae22125866fa6c8a99ea41bace29b6af4"
        }
    }


@freeze_time("2012-10-15 10:00:00")
def test_cli_filters(capsys, settings, tmp_path):
    """
    Given filter arguments should be respected during collection of files.
    """
    sample_structure = settings.fixtures_path / "sample_structure"

    try:
        main([
            "",
            str(sample_structure),
            "--ext=css",
            "--ignore-dir-lead=images",
            "--ignore-dir-lead=css/vendor",
            "--ignore-file-lead=bootstrap-",
            "--ignore-file-lead=logo.p",
        ])
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert captured.err == ""
    assert len(captured.out) > 0
    assert json.loads(captured.out) == {
        "created": "2012-10-15T10:00:00",
        "basedir": str(sample_structure),
        "extensions": ["css"],
        "files": {
            "css/bootstrap.css": "b5b31416eb16e75e8d35469467229af5954d7ebf",
        }
    }


@freeze_time("2012-10-15 10:00:00")
def test_cli_format_text(capsys, settings, tmp_path):
    """
    Given format name should be used to serialize data output.
    """
    sample_structure = settings.fixtures_path / "sample_structure"

    try:
        main([
            "",
            str(sample_structure),
            "--format=text",
        ])
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == (
        "empty.txt\t3345524abf6bbe1809449224b5972c41790b6cf2\n"
        "images/logo.png\taf9d9cee847018416da2bc5eb2011a04a1945bd7\n"
        "images/furo-adjustments.css\tabac58d43616bc9360d3c08524650f050a3fe616\n"
        "images/favicon.ico\tda000da74d8613672fa817b07cdad21b1dc9913f\n"
        "images/lotus/logo.png\t4011d3757eeb983b286c6560ee5880d52d70181a\n"
        "images/lotus/favicon.ico\t45e82276182efeb2aa2ebc388910ff48f2d9a3e1\n"
        "images/atoum/logo.png\te372449fc103593878b40fd467c48353fd7d4f5a\n"
        "images/atoum/favicon.ico\t76a711c735bcf7403dc15c9c762af08182e0e623\n"
        "css/bootstrap.css\tb5b31416eb16e75e8d35469467229af5954d7ebf\n"
        "css/vendor/bootstrap-icons.css\t6e3587086a462623cb250321b4cbb37208827f96\n"
        "css/parts/bootstrap-reboot.css\tc14bf2282a74232929071e7c8711bf501cdfa02e\n"
        "css/parts/bootstrap-grid.css\t8a4e912ae22125866fa6c8a99ea41bace29b6af4\n"
    )


@freeze_time("2012-10-15 10:00:00")
def test_cli_destination(capsys, settings, tmp_path):
    """
    Output should be written to given destination path.
    """
    sample_structure = settings.fixtures_path / "sample_structure"
    destination = tmp_path / "sample.json"

    try:
        main([
            "",
            str(sample_structure),
            "--destination={}".format(destination),
        ])
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "Written output to: {}\n".format(destination)
    assert destination.exists() is True

    assert json.loads(destination.read_text()) == {
        "created": "2012-10-15T10:00:00",
        "basedir": str(sample_structure),
        "extensions": None,
        "files": {
            "empty.txt": "3345524abf6bbe1809449224b5972c41790b6cf2",
            "images/logo.png": "af9d9cee847018416da2bc5eb2011a04a1945bd7",
            "images/furo-adjustments.css": "abac58d43616bc9360d3c08524650f050a3fe616",
            "images/favicon.ico": "da000da74d8613672fa817b07cdad21b1dc9913f",
            "images/lotus/logo.png": "4011d3757eeb983b286c6560ee5880d52d70181a",
            "images/lotus/favicon.ico": "45e82276182efeb2aa2ebc388910ff48f2d9a3e1",
            "images/atoum/logo.png": "e372449fc103593878b40fd467c48353fd7d4f5a",
            "images/atoum/favicon.ico": "76a711c735bcf7403dc15c9c762af08182e0e623",
            "css/bootstrap.css": "b5b31416eb16e75e8d35469467229af5954d7ebf",
            "css/vendor/bootstrap-icons.css": (
                "6e3587086a462623cb250321b4cbb37208827f96"
            ),
            "css/parts/bootstrap-reboot.css": (
                "c14bf2282a74232929071e7c8711bf501cdfa02e"
            ),
            "css/parts/bootstrap-grid.css": "8a4e912ae22125866fa6c8a99ea41bace29b6af4"
        }
    }
