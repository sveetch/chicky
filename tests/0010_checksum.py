from chicky.core import checksum


def test_checksum_basic(settings):
    """
    Checksum on a basic text file works as expected and 'digest_size' argument is
    respected when used.
    """
    sample_structure = settings.fixtures_path / "sample_structure"
    result = checksum(sample_structure / "css/bootstrap.css")
    assert isinstance(result, str) is True
    assert len(result) == 40
    assert result == "b5b31416eb16e75e8d35469467229af5954d7ebf"


def test_checksum_binary(settings):
    """
    Checksum on a binary file works as expected.
    """
    sample_structure = settings.fixtures_path / "sample_structure"
    result = checksum(sample_structure / "images/logo.png")
    assert isinstance(result, str) is True
    assert len(result) == 40
    assert result == "af9d9cee847018416da2bc5eb2011a04a1945bd7"


def test_checksum_digest_size(settings):
    """
    The 'digest_size' argument is respected when used.
    """
    sample_structure = settings.fixtures_path / "sample_structure"
    result = checksum(sample_structure / "css/bootstrap.css", digest_size=10)
    assert isinstance(result, str) is True
    assert len(result) == 20
    assert result == "de5cf0ac7ea0856f1d5a"
