import gspread
import time
import json
import sys


# times: amount of retries
# timeout: pause time in seconds before retrying
# logger: if you are using loggers
def retrier(times, **kwargs):
    code_wait = [403, 429]
    timeout = kwargs.get('timeout', 0.0)
    logger = kwargs.get('logger', False)

    def attempt(func):
        def function(*fargs, **fkwargs):
            result = None
            attempts = 0
            while attempts < times:
                try:
                    result = func(*fargs, **fkwargs)
                except gspread.exceptions.APIError as err:
                    error_code = err.response.status_code
                    reason = err.response.reason
                    error_summary = "Encountered an error code '{}' due to {}".format(error_code, reason)
                    error = err.response._content.decode('utf8')
                    error_json = json.loads(error)
                    error_message = error_json['error']['message']
                    if logger:
                        logger.warning(error_summary)
                        logger.warning(error_message)
                    else:
                        sys.stdout.write("{}\n".format(error_summary))
                        sys.stdout.write("{}\n".format(error_message))
                    if error_code in code_wait:
                        attempts += 1
                        if attempts == times:
                            return error_summary
                        if logger:
                            logger.info("Sleeping for {} seconds due to {}.".format(timeout, reason))
                        else:
                            sys.stdout.write("Sleeping for {} seconds due to {}.\n".format(timeout, reason))
                        time.sleep(timeout)
                    else:
                        return error_summary
                except Exception as err:
                    return err
                if result:
                    return result
        return function
    return attempt
