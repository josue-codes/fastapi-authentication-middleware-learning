import os
import logging
from typing_extensions import Literal
from datetime import datetime


def get_logger(
        logger_name: str,
        app_name: str,
        file_log_level: Literal[0, 10, 20, 30, 40, 50] = 10,
        stdout_log_level: Literal[0, 10, 20, 30, 40, 50] = 20
) -> logging.Logger:
    """Creates and configures a logger with the specified name, application name, and log level.

    Args:
        logger_name (str): The name of the logger.
        app_name (str, optional): The application name, used as a prefix for the log filename.
        file_log_level (Literal[0, 10, 20, 30, 40, 50], optional): The logging level for files (0, 10, 20, 30, 40, 50) corresponding to (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL). Defaults to 10 (DEBUG).
        stdout_log_level (Literal[0, 10, 20, 30, 40, 50], optional): The logging level for stdout (0, 10, 20, 30, 40, 50) corresponding to (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL). Defaults to 20 (INFO).

    Returns:
        logging.Logger: The configured logger instance.

    Example:
        logger = get_logger(__name__)
        logger.info("This is an info log message.")
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(min(file_log_level, stdout_log_level))

    log_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(module)s - Line: %(lineno)d - %(funcName)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File logger - Rotate log files by date
    today = datetime.today().strftime('%Y-%m-%d')
    log_filename = f'{app_name}-{today}.log'
    log_path = os.path.join(os.getcwd(), log_filename)
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(file_log_level)
    logger.addHandler(file_handler)

    # StdOut logger - Useful when running script directly
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(log_formatter)
    stdout_handler.setLevel(stdout_log_level)
    logger.addHandler(stdout_handler)

    return logger


def log_function_and_args(logger):
    """A decorator function to log the function name and its arguments. The decorated function's execution is not affected.

    Args:
        logger (logging.Logger): Logger instance used for logging function name and arguments.

    Returns:
        Callable: The decorator function.
    """
    def decorator(func):
        """The decorator function that takes the target function as an argument.

        Args:
            func (Callable): The target function to be decorated.

        Returns:
            Callable: The wrapped function that logs the function name and arguments.
        """
        def function_logger(*args, **kwargs):
            """The wrapped function that logs the function name and its arguments before executing it.

            Args:
                *args: The positional arguments passed to the target function.
                **kwargs: The keyword arguments passed to the target function.

            Returns:
                Any: The return value of the target function.
            """
            function_name = func.__name__
            args_strs = list()
            for arg in args:
                if len(repr(arg)) > 50:
                    args_strs.append(f'{repr(arg)[:50]}...')
                else:
                    args_strs.append(repr(arg))
            args_str = ', '.join(args_strs)
            kwargs_strs = list()
            for k, v in kwargs.items():
                if len(repr(v)) > 50:
                    kwargs_strs.append(f'{k}={repr(v)[:50]}...')
                else:
                    kwargs_strs.append(f'{k}={repr(v)}')
            kwargs_str = ', '.join(kwargs_strs)
            all_args = ', '.join(filter(None, [args_str, kwargs_str]))
            logger.debug(f'{function_name}({all_args})')

            return func(*args, **kwargs)
        return function_logger
    return decorator


if __name__ == '__main__':  # pragma: no cover
    pass
