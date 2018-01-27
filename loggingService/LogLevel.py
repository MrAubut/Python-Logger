
class LogLevel(object):
    INFO = 0
    WARNING = 1
    ERROR = 2

    @staticmethod
    def get_level_string(level):
        if level == LogLevel.INFO:
            return 'INFO'
        elif level == LogLevel.WARNING:
            return 'WARNING'
        elif level == LogLevel.ERROR:
            return 'ERROR'