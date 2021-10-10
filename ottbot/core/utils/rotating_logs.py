try:
    import codecs
except ImportError:
    codecs = None
import logging.handlers
import time
import os


class LoggingFilter(logging.Filter):
    """Custom filter to get rid of repetitive messages"""

    FILTER_MESSAGES = ["Commiting database"]

    def filter(self, record: logging.LogRecord) -> bool:
        return all([msg in record.getMessage() for msg in self.FILTER_MESSAGES])


class BetterTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """Rotating file handler that updates the filename on rotation"""

    def __init__(self, path):
        self.path = path
        filename = os.path.join(self.path, f"{time.strftime('%m-%d-%Y')}.log")

        logging.handlers.TimedRotatingFileHandler.__init__(
            self, filename, when="D", interval=1, backupCount=0, encoding=None
        )
        # `when` kwarg
        # Calculate the real rollover interval, which is just the number of
        # seconds between rollovers.  Also set the filename suffix used when
        # a rollover occurs.  Current 'when' events supported:
        # S - Seconds
        # M - Minutes
        # H - Hours
        # D - Days
        # midnight - roll over at midnight
        # W{0-6} - roll over on a certain day; 0 - Monday
        #
        # Case of the 'when' specifier is not important; lower or upper case
        # will work.

    def doRollover(self):
        """
        TimedRotatingFileHandler remix - rotates logs on daily basis, and filename of current logfile is time.strftime("%m-%d-%Y").log
        """
        self.stream.close()
        # get the time that this sequence started at and make it a TimeTuple
        t = self.rollover_at - self.interval
        time_tuple = time.localtime(t)
        self.base_filename = os.path.join(self.path, f"{time.strftime('%m-%d-%Y')}.log")
        if self.encoding:
            self.stream = codecs.open(self.base_Filename, "w", self.encoding)
        else:
            self.stream = open(self.base_filename, "w")
        self.rollover_at = self.rollover_at + self.interval


if __name__ == "__main__":
    trfh = BetterTimedRotatingFileHandler(
        os.path.join(".", "logs")
    )  # set logging dir to "./logs"
    ff = logging.Formatter(
        f"[%(asctime)s] %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    trfh.setFormatter(ff)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(trfh)
