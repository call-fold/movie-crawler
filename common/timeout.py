#!/usr/bin/env python
# -*- coding: utf-8 -*-


from functools import wraps
import errno
import os
import signal


class TimeouError(Exception):
    pass


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def __handle_timeout(signum, frame):
            raise TimeouError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, __handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


def main():
    pass


if __name__ == '__main__':
    main()
