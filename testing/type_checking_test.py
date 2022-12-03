import pytest
from pytest import approx
from betterplotlib.type_checking import *


# ------------------------------------------------------------------------------
#
# testing numeric list type checking
#
# ------------------------------------------------------------------------------
def test_numeric_list_scalar_value():
    assert numeric_list_1d(3.4) == approx(3.4)


def test_numeric_list_scalar_type():
    assert type(numeric_list_1d(3.4)) == np.ndarray


def test_numeric_list_scalar_length():
    assert len(numeric_list_1d(3.4)) == 1


def test_numeric_list_list():
    original_list = [1.0, 2.0, 3.0]
    assert approx(numeric_list_1d(original_list)) == np.array(original_list)


def test_numeric_list_empty_list():
    assert len(numeric_list_1d([])) == 0


def test_numeric_list_list_multiple_dimensions():
    original_list = [[1.0, 2.0, 3.0], [4, 5, 6]]
    with pytest.raises(ValueError) as err_msg:
        numeric_list_1d(original_list)
    assert str(err_msg.value) == "This item cannot be cast to a float array."


def test_numeric_list_string():
    with pytest.raises(TypeError) as err_msg:
        numeric_list_1d("abc")
    assert str(err_msg.value) == "This item cannot be cast to a float array."


def test_numeric_list_empty_string():
    with pytest.raises(TypeError) as err_msg:
        numeric_list_1d("")
    assert str(err_msg.value) == "This item cannot be cast to a float array."


def test_numeric_list_string_array():
    with pytest.raises(TypeError) as err_msg:
        numeric_list_1d(["a", "b", "c"])
    assert str(err_msg.value) == "This item cannot be cast to a float array."


def test_numeric_list_string_float_value():
    assert numeric_list_1d("3.4") == approx(3.4)


def test_numeric_list_string_float_type():
    assert type(numeric_list_1d("3.4")) == np.ndarray


def test_numeric_list_string_float_length():
    assert len(numeric_list_1d("3.4")) == 1


def test_numeric_list_string_array_float_value():
    data = ["3.4", "4.5", "7.6"]
    assert approx(numeric_list_1d(data)) == [float(item) for item in data]


def test_numeric_list_string_array_float_type():
    assert type(numeric_list_1d(["3.4", "4.5", "7.6"])) == np.ndarray


def test_numeric_list_string_array_float_length():
    assert len(numeric_list_1d(["3.4", "4.5", "7.6"])) == 3


def test_numeric_list_float_string_array():
    with pytest.raises(TypeError) as err_msg:
        numeric_list_1d(["a", "b", "c"])
    assert str(err_msg.value) == "This item cannot be cast to a float array."


def test_numeric_list_dict_with_int_keys():
    """Integer keys can mess up some things, since they act like indices."""
    test_dict = {0: "a", 1: "b", 2: "c"}
    with pytest.raises(TypeError) as err_msg:
        numeric_list_1d(test_dict)
    assert str(err_msg.value) == "This item cannot be cast to a float array."


def test_numeric_list_message_default():
    with pytest.raises(TypeError) as err_msg:
        numeric_list_1d("a")  # default value
    assert str(err_msg.value) == "This item cannot be cast to a float array."


def test_numeric_list_message_user():
    user_msg = "This is bad and you should feel bad."
    with pytest.raises(TypeError) as err_msg:
        numeric_list_1d("a", user_msg)  # default value
    assert str(err_msg.value) == user_msg


# ------------------------------------------------------------------------------
#
# testing numeric scalar type checking
#
# ------------------------------------------------------------------------------
def test_numeric_scalar_regular_floats():
    assert numeric_scalar(1.7) == approx(1.7)


def test_numeric_scalar_float_type():
    assert type(numeric_scalar(1.87)) == float


def test_numeric_scalar_regular_int():
    assert numeric_scalar(1) == approx(1)


def test_numeric_scalar_int_type():
    assert type(numeric_scalar(1)) == float


def test_numeric_scalar_regular_float_string():
    assert numeric_scalar("6.45") == approx(6.45)


def test_numeric_scalar_float_string_type():
    assert type(numeric_scalar("6.45")) == float


def test_numeric_scalar_empty_list():
    with pytest.raises(TypeError) as err_msg:
        numeric_scalar([])
    assert str(err_msg.value) == "This item cannot be cast to a scalar float."


def test_numeric_scalar_empty_array():
    with pytest.raises(TypeError) as err_msg:
        numeric_scalar(np.array([]))
    assert str(err_msg.value) == "This item cannot be cast to a scalar float."


def test_numeric_scalar_list_many_items():
    with pytest.raises(TypeError) as err_msg:
        numeric_scalar([1, 2, 3])
    assert str(err_msg.value) == "This item cannot be cast to a scalar float."


def test_numeric_scalar_array_many_items():
    with pytest.raises(TypeError) as err_msg:
        numeric_scalar(np.array([1, 2, 3]))
    assert str(err_msg.value) == "This item cannot be cast to a scalar float."


def test_numeric_scalar_single_item_list_allowed_type():
    assert type(numeric_scalar([1])) == float


def test_numeric_scalar_single_item_list_allowed_value():
    assert numeric_scalar([1.5]) == approx(1.5)


def test_numeric_scalar_single_item_array_allowed_type():
    assert type(numeric_scalar(np.array([1]))) == float


def test_numeric_scalar_single_item_array_allowed_value():
    assert numeric_scalar(np.array([1.7])) == approx(1.7)


def test_numeric_scalar_no_length_array_allowed_type():
    assert type(numeric_scalar(np.array(1.7))) == float


def test_numeric_scalar_no_length_array_allowed_value():
    assert numeric_scalar(np.array(1.7)) == approx(1.7)


def test_numeric_scalar_regular_float_string_array():
    assert numeric_scalar(["6.45"]) == approx(6.45)


def test_numeric_scalar_float_string_array_type():
    assert type(numeric_scalar(["6.45"])) == float


def test_numeric_scalar_empty_string():
    with pytest.raises(TypeError) as err_msg:
        numeric_scalar("")
    assert str(err_msg.value) == "This item cannot be cast to a scalar float."


def test_numeric_scalar_single_char_string():
    with pytest.raises(TypeError) as err_msg:
        numeric_scalar("a")
    assert str(err_msg.value) == "This item cannot be cast to a scalar float."


def test_numeric_scalar_multiple_char_string():
    with pytest.raises(TypeError) as err_msg:
        numeric_scalar("abc")
    assert str(err_msg.value) == "This item cannot be cast to a scalar float."


def test_numeric_scalar_dict():
    test_dict = {0: 0}
    with pytest.raises(TypeError) as err_msg:
        numeric_scalar(test_dict)
    assert str(err_msg.value) == "This item cannot be cast to a scalar float."


def test_numeric_scalar_message_default_empty_list():
    with pytest.raises(TypeError) as err_msg:
        numeric_scalar([])
    assert str(err_msg.value) == "This item cannot be cast to a scalar float."


def test_numeric_scalar_message_default_list():
    with pytest.raises(TypeError) as err_msg:
        numeric_scalar([1, 2, 3])
    assert str(err_msg.value) == "This item cannot be cast to a scalar float."


def test_numeric_scalar_message_default_string():
    with pytest.raises(TypeError) as err_msg:
        numeric_scalar("a")
    assert str(err_msg.value) == "This item cannot be cast to a scalar float."


def test_numeric_scalar_message_user():
    user_msg = "This is bad and you should feel bad."
    with pytest.raises(TypeError) as err_msg:
        numeric_scalar([], user_msg)
    assert str(err_msg.value) == user_msg


def test_numeric_scalar_message_user_list():
    user_msg = "This is bad and you should feel bad."
    with pytest.raises(TypeError) as err_msg:
        numeric_scalar([1, 2, 3], user_msg)
    assert str(err_msg.value) == user_msg


def test_numeric_scalar_message_user_empty_list():
    user_msg = "This is bad and you should feel bad."
    with pytest.raises(TypeError) as err_msg:
        numeric_scalar([], user_msg)
    assert str(err_msg.value) == user_msg
