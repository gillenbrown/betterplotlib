import numpy as np


def numeric_list_1d(item, message=""):
    """
    Return a numpy array of float values. Serves as error checking too.

    Lists will be returned as numpy array objects with `dtype="float64"`.
    Scalar floats or ints will be returned as a one item numpy array with the
    same data type. Other data objects that cannot be parsed into a numpy array
    with this data type will raise a TypeError.

    :param item: Any python object that you want to check whether it can be
                 parsed into a numpy array of floats.
    :param message: Optional parameter that will be the error message if `item`
                    cannot be parsed into this format. Will have a default error
                    message if this is not passed in.
    :return: Array of float values.
    :rtype: np.ndarray
    :raises: TypeError if data cannot be parsed into a float array.
    """
    if message == "":
        message = "This item cannot be cast to a float array."
    # need to turn item into an iterable so it has a length if it is made
    # into a numpy array. This is useful for scalars.
    try:
        len(item)
    except TypeError:  # is a scalar
        item = [item]
    # also check for scalar strings
    if isinstance(item, str):
        item = [item]

    # see if it is compatible with the numpy float array.
    try:
        array = np.array(item, dtype="float64")
    except ValueError:  # wrong data type.
        raise TypeError(message)
    except TypeError:
        raise TypeError(message)

    # then check that it isn't multi-dimensional
    if len(array.shape) > 1:
        raise ValueError(message)

    return array


def numeric_scalar(item, message=""):
    """
    Turn an item into a single float value. Performs error checking too.

    :param item: Item to check for numerical scalar-ness.
    :param message: Message to be passed to the user via the error message if
                    `item` is not compatible with a float. Will raise a default
                    error message if this is empty.
    :return:
    """
    if message == "":
        message = "This item cannot be cast to a scalar float."
    # check for dictionaries, where their access can behave like indexing if
    # the appropriate keys are present.
    if isinstance(item, dict):
        raise TypeError(message)

    # check for iterability
    try:
        if len(item) != 1:
            raise TypeError(message)
        item = item[0]
    except TypeError:  # scalars have no length, dictionaries key
        pass

    try:
        return float(item)
    except (ValueError, TypeError):  # bad conversion to float
        raise TypeError(message)
