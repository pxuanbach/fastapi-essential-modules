from os import path


def read_file_line_by_line(file_path):
    if not path.exists(file_path):
        return []
    try:
        with open(file_path, "r") as f:
            return [line.rstrip() for line in f]
    except:
        pass
    return []
