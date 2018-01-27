import os
import pickle

log_filename = 'simplelog.pkl'

class LogBuffer:

    def __init__(self, log_depth = 1000):
        self._buffer = []
        self._log_depth = log_depth
        self.restore_buffer()

    def add_log_message(self, message):
        if self._buffer.__len__() >= self._log_depth:
            self._buffer.remove(self._buffer[0])
        self._buffer.append(message)
        self.save_buffer()

    def dump_buffer(self, level):
        log = ''
        for message in self._buffer:
            log += message.get_message(level)
        return log

    def clear_buffer(self):
        self._buffer = []

    def save_buffer(self):
        with open(log_filename, 'wb') as f:
            pickle.dump(self._buffer, f, -1)

    def restore_buffer(self):
        if os.path.exists(log_filename):
            with open(log_filename, 'rb') as f:
                 self._buffer = pickle.load(f)