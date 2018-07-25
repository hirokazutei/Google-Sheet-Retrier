# Google-Sheet-Retrier
Waits and Retries Request When You Hit API Limit

## How to use:
1. Import it:
~~~
import retrier
~~~

2. Use it as a decorator:
~~~
@retrier(3, timeout=10, logger=logger)
def write_on_google_sheet_function():
~~~
* The first variable indicates the amount of times you want to retry before giving up.
* `timeout` indicates the amount of time in seconds you would like to wait before retrying.
* `logger` allows you to set a logger so the error messages can be logged.

## Deals With:
Currently, it pauses only for `403` and `429` errors since they are time-dependent.

## Contribution:
Please let me know if there are other API errors that can be dealt with in a perferred way, I will make adjustments.
