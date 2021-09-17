import charset_normalizer

import dgloss


def decode_bytes(bytes, filename=None):
    charset_data = charset_normalizer.from_bytes(bytes).best()
    return get_str(charset_data, filename)


def decode_file(filename):
    filename = str(filename)
    charset_data = charset_normalizer.from_path(filename).best()
    return get_str(charset_data)


def get_str(charset_data, filename=None):
    err_msg = "Unable to decode character data"
    if not charset_data:
        if filename:
            err_msg += f": {filename}"
        raise dgloss.EncodingError(err_msg)
    text = str(charset_data)
    return text
