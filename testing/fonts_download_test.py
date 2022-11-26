import pytest
from pathlib import Path
import matplotlib
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


def test_set_style_downloads_fonts():
    font_dir = Path(matplotlib.get_data_path()) / "fonts/ttf/"
    font_file_name = "Lobster-Regular.ttf"

    # remove the font from the previous download (locally. on remote this does nothing)
    for item in font_dir.iterdir():  # pragma: no cover
        if item.name == font_file_name:
            item.unlink()
    assert font_file_name not in [i.name for i in font_dir.iterdir()]

    # then set this to download it
    bpl.set_style(font="Lobster")
    assert font_file_name in [i.name for i in font_dir.iterdir()]
    # reset to normal style so as to not mess up other tests
    bpl.set_style()


def test_error_with_bad_font_name(make_temp_dir):
    with pytest.raises(ValueError):
        bpl.download_font("sldkfjsldkfjlskedfj", temp_dir)
    assert len([f.name for f in temp_dir.iterdir()]) == 0
