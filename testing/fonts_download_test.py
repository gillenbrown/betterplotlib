import pytest
from pathlib import Path

import betterplotlib as bpl

temp_dir = Path(__file__).parent / "temp_font_dir"


@pytest.fixture(scope="function")
def make_temp_dir():
    temp_dir.mkdir(exist_ok=False)
    yield
    for item in temp_dir.iterdir():
        item.unlink()
    temp_dir.rmdir()


lato_files = [
    "Lato-Black.ttf",
    "Lato-BlackItalic.ttf",
    "Lato-Bold.ttf",
    "Lato-BoldItalic.ttf",
    "Lato-ExtraBold.ttf",
    "Lato-ExtraBoldItalic.ttf",
    "Lato-ExtraLight.ttf",
    "Lato-ExtraLightItalic.ttf",
    "Lato-Italic.ttf",
    "Lato-Light.ttf",
    "Lato-LightItalic.ttf",
    "Lato-Medium.ttf",
    "Lato-MediumItalic.ttf",
    "Lato-Regular.ttf",
    "Lato-SemiBold.ttf",
    "Lato-SemiBoldItalic.ttf",
    "Lato-Thin.ttf",
    "Lato-ThinItalic.ttf",
]

opensans_files = [
    "OpenSans[wdth,wght].ttf",
    "OpenSans-Italic[wdth,wght].ttf",
]

roboto_files = [
    "Roboto-Light.ttf",
    "Roboto-Regular.ttf",
    "Roboto-Medium.ttf",
    "Roboto-MediumItalic.ttf",
    "Roboto-ThinItalic.ttf",
    "Roboto-BoldItalic.ttf",
    "Roboto-LightItalic.ttf",
    "Roboto-Italic.ttf",
    "Roboto-BlackItalic.ttf",
    "Roboto-Bold.ttf",
    "Roboto-Thin.ttf",
    "Roboto-Black.ttf",
]


def test_download_font_into_directory(make_temp_dir):
    bpl.download_font("Lato", temp_dir)
    assert sorted(lato_files) == sorted([i.name for i in temp_dir.iterdir()])


def test_download_variable_font_into_directory(make_temp_dir):
    bpl.download_font("OpenSans", temp_dir)
    assert sorted(opensans_files) == sorted([i.name for i in temp_dir.iterdir()])


def test_download_variable_font_static_into_directory(make_temp_dir):
    bpl.download_font("Roboto", temp_dir)
    assert sorted(roboto_files) == sorted([i.name for i in temp_dir.iterdir()])
