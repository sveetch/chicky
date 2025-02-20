from chicky.core import collect_files


def test_collect_checksum(settings):
    """
    When collecting a path, the basedir is removed from leading of paths and they
    all have a checksum.
    """
    sample_structure = settings.fixtures_path / "sample_structure"
    result = collect_files(sample_structure / "css")

    store = [[str(v[0]), v[1]] for v in result]
    assert store == [
        ["bootstrap.css", "b5b31416eb16e75e8d35469467229af5954d7ebf"],
        ["vendor/bootstrap-icons.css", "6e3587086a462623cb250321b4cbb37208827f96"],
        ["parts/bootstrap-reboot.css", "c14bf2282a74232929071e7c8711bf501cdfa02e"],
        ["parts/bootstrap-grid.css", "8a4e912ae22125866fa6c8a99ea41bace29b6af4"],
    ]


def test_collect_all_files(settings):
    """
    Just collecting the whole structure.
    """
    sample_structure = settings.fixtures_path / "sample_structure"
    result = collect_files(sample_structure)

    # We just care of paths
    store = [str(v[0]) for v in result]
    assert store == [
        "empty.txt",
        "images/logo.png",
        "images/furo-adjustments.css",
        "images/favicon.ico",
        "images/lotus/logo.png",
        "images/lotus/favicon.ico",
        "images/atoum/logo.png",
        "images/atoum/favicon.ico",
        "css/bootstrap.css",
        "css/vendor/bootstrap-icons.css",
        "css/parts/bootstrap-reboot.css",
        "css/parts/bootstrap-grid.css"
    ]


def test_collect_filter_extensions(settings):
    """
    Collecting should respect allowed file extensions if given.
    """
    sample_structure = settings.fixtures_path / "sample_structure"
    result = collect_files(sample_structure, extensions=["css", "txt"])
    # We just care of paths
    store = [str(v[0]) for v in result]

    assert store == [
        "empty.txt",
        "images/furo-adjustments.css",
        "css/bootstrap.css",
        "css/vendor/bootstrap-icons.css",
        "css/parts/bootstrap-reboot.css",
        "css/parts/bootstrap-grid.css"
    ]


def test_collect_filter_ignore_dir_leads(settings):
    """
    Collecting should ignore files with given pattern director leadings.
    """
    sample_structure = settings.fixtures_path / "sample_structure"

    dir_leads = ["images", "css/vendor", "parts"]

    result = collect_files(sample_structure, dir_leads=dir_leads)

    # We just care of paths
    store = [str(v[0]) for v in result]
    assert store == [
        "empty.txt",
        "css/bootstrap.css",
        "css/parts/bootstrap-reboot.css",
        "css/parts/bootstrap-grid.css"
    ]


def test_collect_filter_ignore_filename_leads(settings):
    """
    Collecting should ignore files with given pattern filename leadings.
    """
    sample_structure = settings.fixtures_path / "sample_structure"

    filename_leads = ["bootstrap-", "logo.p", "images"]

    result = collect_files(sample_structure, filename_leads=filename_leads)

    # We just care of paths
    store = [str(v[0]) for v in result]
    assert store == [
        "empty.txt",
        "images/furo-adjustments.css",
        "images/favicon.ico",
        "images/lotus/favicon.ico",
        "images/atoum/favicon.ico",
        "css/bootstrap.css",
    ]


def test_collect_filter_mix(settings):
    sample_structure = settings.fixtures_path / "sample_structure"

    dir_leads = ["images", "css/vendor"]
    filename_leads = ["bootstrap-", "logo.p"]

    result = collect_files(
        sample_structure,
        extensions=["css"],
        dir_leads=dir_leads,
        filename_leads=filename_leads,
    )

    # We just care of paths
    store = [str(v[0]) for v in result]
    assert store == [
        "css/bootstrap.css",
    ]
