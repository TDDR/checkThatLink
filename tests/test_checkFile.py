import src.checkFile as checkFile
from unittest import mock
import pytest


class Args:
    pass


args = Args()
args.file = "resources/test.html"
args.secureHttp = None
args.json = None
args.all = None
args.good = None
args.bad = None
args.ignoreFile = None
args.telescope = None


def test_no_file_exception():
    args.file = "wrong/file/path"

    with pytest.raises(FileNotFoundError):
        checkFile.checkFile(args)

    args.file = "resources/test.html"


@mock.patch("src.checkFile.checkFile.headRequest")
def test_headRequest_200(mock_headRequest):

    link = "http://google.com"
    mock_headRequest.return_value = {"url": link, "status": 200, "secured": False}
    cF = checkFile.checkFile(args)

    assert cF.headRequest(link) == {
        "url": "http://google.com",
        "status": 200,
        "secured": False,
    }


@mock.patch("src.checkFile.checkFile.headRequest")
def test_headRequest_404(mock_headRequest):

    link = "http://google.cim"
    mock_headRequest.return_value = {"url": link, "status": 404, "secured": False}
    cF = checkFile.checkFile(args)

    assert cF.headRequest(link) == {
        "url": "http://google.cim",
        "status": 404,
        "secured": False,
    }


def test_parseWebAddress():

    lineToParse = "https://www.google.com/search?q=help"

    cF = checkFile.checkFile(args)

    assert cF.parseWebAddress(lineToParse) == "https://www.google.com/search?q=help"