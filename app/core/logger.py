import datetime
import logging
import os

# Define default logfile format.
file_name_format = "{year:04d}{month:02d}{day:02d}.log"

# Define the default logging message formats.
file_msg_format = "%(asctime)s %(levelname)-8s: %(message)s"
console_msg_format = "%(levelname)s: %(message)s"

# Define the log rotation criteria.
max_bytes = 1024**2   # ~ 1MB
backup_count = 100


class ColoredFormatter(logging.Formatter):
    COLOR_CODES = {
        'DEBUG': '\033[94m',  # blue
        'INFO': '\033[92m',   # green
        'WARNING': '\033[93m',  # yellow
        'ERROR': '\033[91m',  # red
        'CRITICAL': '\033[41m\033[97m'  # red background color and white text
    }
    RESET_CODE = '\033[0m'  # called to return to standard terminal text color

    def format(self, record):
        # Get the color corresponding to the log level
        color = self.COLOR_CODES.get(record.levelname, '')
        # Add color to log messages and reset color at the end
        formatted_message = f"{color}{super().format(record)}{self.RESET_CODE}"
        return formatted_message


def setup(dir = "log", file_level=logging.DEBUG, stream_level=logging.INFO):
    # Create the root logger.
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Validate the given directory.
    dir = os.path.normpath(dir)
    
    # Create a folder for the logfiles.
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Construct the name of the logfile.
    t = datetime.datetime.now()
    file_name = file_name_format.format(
        year=t.year,
        month=t.month,
        day=t.day,
    )
    file_name = os.path.join(dir, file_name)

    # Set up logging to the logfile.
    file_handler = logging.handlers.RotatingFileHandler(
        filename=file_name, maxBytes=max_bytes, backupCount=backup_count
    )
    file_handler.setLevel(file_level)
    file_formatter = logging.Formatter(file_msg_format)
    file_handler.setFormatter(file_formatter)

    # Set up logging to the console.
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(stream_level)
    stream_formatter = ColoredFormatter(console_msg_format)
    stream_handler.setFormatter(stream_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return
