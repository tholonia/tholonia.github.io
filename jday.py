#!/bin/env python
from datetime import datetime


def days_from_date_to_now(year, month, day):
  # Create a datetime object for the arbitrary date
  arbitrary_date = datetime(year, month, day)

  # Get the current date
  current_date = datetime.now()

  # Calculate the difference in days
  delta = current_date - arbitrary_date

  # Extract the days from the delta
  return delta.days


# Example usage:
arbitrary_year = 2000
arbitrary_month = 1
arbitrary_day = 1

days_difference = days_from_date_to_now(arbitrary_year, arbitrary_month, arbitrary_day)
print(days_difference)
