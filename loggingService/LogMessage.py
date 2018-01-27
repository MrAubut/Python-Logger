import time
import LogLevel

class LogMessage():

    def __init__(self, identity, level, message):
        self._timestamp = time.time()
        self._identity = identity
        self._level = self.get_level(level)
        self._message = message

    def get_message(self, level):
        if  self._level >= self.get_level(level):
            return '{} {} -> {}: {}\n'.format(self._timestamp, self._identity,
                                        LogLevel.LogLevel.get_level_string(self._level), self._message)
        return ''

    def get_level(self, level):
        if level.startswith('e') or level.startswith('E'):
            return LogLevel.LogLevel.ERROR
        elif level.startswith('w') or level.startswith('W'):
            return LogLevel.LogLevel.WARNING
        else:
            return LogLevel.LogLevel.INFO
