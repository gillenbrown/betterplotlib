import pytest
import os

from matplotlib import rcParams

import betterplotlib as bpl

temp_dir = "temp_font_dir"

@pytest.fixture(scope="function")
def make_temp_dir():
    os.mkdir(temp_dir)
    yield
    for item in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, item))
    os.rmdir(temp_dir)

nunito_files = ["Nunito-Black.ttf",
                "Nunito-BlackItalic.ttf",
                "Nunito-Bold.ttf",
                "Nunito-BoldItalic.ttf",
                "Nunito-ExtraBold.ttf",
                "Nunito-ExtraBoldItalic.ttf",
                "Nunito-ExtraLight.ttf",
                "Nunito-ExtraLightItalic.ttf",
                "Nunito-Italic.ttf",
                "Nunito-Light.ttf",
                "Nunito-LightItalic.ttf",
                "Nunito-Regular.ttf",
                "Nunito-SemiBold.ttf",
                "Nunito-SemiBoldItalic.ttf"]

def test_download_font_into_directory(make_temp_dir):
    bpl.download_font("Nunito", temp_dir)

    for item in nunito_files:
        assert item in os.listdir(temp_dir)

def test_download_real():
    bpl.set_style(font="Nunito")

    font_dir = os.path.join(rcParams["datapath"], "fonts/ttf/")

    for item in nunito_files:
        assert item in os.listdir(font_dir)