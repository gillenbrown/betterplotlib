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

tinos_files = [
    "Tinos-Bold.ttf",
    "Tinos-BoldItalic.ttf",
    "Tinos-Italic.ttf",
    "Tinos-Regular.ttf",
]

opensans_files = [
    "OpenSans[wdth,wght].ttf",
    "OpenSans-Italic[wdth,wght].ttf",
]

inconsolata_files = [
    "Inconsolata-Black.ttf",
    "Inconsolata-Bold.ttf",
    "Inconsolata-ExtraBold.ttf",
    "Inconsolata-ExtraLight.ttf",
    "Inconsolata-Light.ttf",
    "Inconsolata-Medium.ttf",
    "Inconsolata-Regular.ttf",
    "Inconsolata-SemiBold.ttf",
]


def test_download_lato_into_directory(make_temp_dir):
    bpl.download_font("Lato", temp_dir)
    assert sorted(lato_files) == sorted([i.name for i in temp_dir.iterdir()])


def test_download_font_into_directory(make_temp_dir):
    bpl.download_font("Tinos", temp_dir)
    assert sorted(tinos_files) == sorted([i.name for i in temp_dir.iterdir()])


def test_download_variable_font_into_directory(make_temp_dir):
    bpl.download_font("OpenSans", temp_dir)
    assert sorted(opensans_files) == sorted([i.name for i in temp_dir.iterdir()])


def test_download_variable_font_static_into_directory(make_temp_dir):
    bpl.download_font("Inconsolata", temp_dir)
    assert sorted(inconsolata_files) == sorted([i.name for i in temp_dir.iterdir()])


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
