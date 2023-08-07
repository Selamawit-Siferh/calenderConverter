import datetime

def _start_day_of_ethiopian(year):
    """ returns first day of that Ethiopian year

    Params:
    * year: an int """

    # magic formula gives start of year
    new_year_day = (year // 100) - (year // 400) - 4

    # if the prev Ethiopian year is a leap year, new-year occurs on 12th
    if (year - 1) % 4 == 3:
        new_year_day += 1

    return new_year_day

def gregorian_to_ethiopian(year, month, date):
    """ Ethiopian date object representation of provided Gregorian date

    Params:
    * year: an int
    * month: an int
    * date: an int """

    # prevent incorrect input
    inputs = (year, month, date)
    if 0 in inputs or [data.__class__ for data in inputs].count(int) != 3:
        raise ValueError("Malformed input can't be converted.")

    # Number of days in Gregorian months starting with January (index 1)
    # Index 0 is reserved for leap year switches.
    gregorian_months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Number of days in Ethiopian months starting with January (index 1)
    # Index 0 is reserved for leap year switches.
    ethiopian_months = [0, 30, 30, 30, 30, 30, 30, 30, 30, 30, 5, 30, 30, 30, 30]

    # if Gregorian leap year, February has 29 days.
    if  (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        gregorian_months[2] = 29

    # September sees 8-year difference
    ethiopian_year = year - 8

    # if Ethiopian leap year, Pagumain has 6 days
    if ethiopian_year % 4 == 3:
        ethiopian_months[10] = 6
    else:
        ethiopian_months[10] = 5

    # Ethiopian new year in Gregorian calendar
    new_year_day = _start_day_of_ethiopian(ethiopian_year)

    # calculate number of days up to that date
    until = 0
    for i in range(1, month):
         until += gregorian_months[i]
    until += date

    # update Tahissas (December) to match January 1st
    if ethiopian_year % 4 == 0:
        tahissas = 26
    else:
        tahissas = 25

    # take into account the 1582 change
    if year < 1582:
        ethiopian_months[1] = 0
        ethiopian_months[2] = tahissas
    elif until <= 277 and year == 1582:
        ethiopian_months[1] = 0
        ethiopian_months[2] = tahissas
    else:
        tahissas = new_year_day - 3
        ethiopian_months[1] = tahissas

    # calculate month and date incrementally
    m = 0
    for m in range(1, len(ethiopian_months)):
        if until <= ethiopian_months[m]:
            if m == 1 or ethiopian_months[m] == 0:
                ethiopian_date = until + (30 - tahissas)
            else:
                ethiopian_date = until
            break
        else:
            until -= ethiopian_months[m]

    # if m > 10, we're already on the next Ethiopian year
    if m > 10:
        ethiopian_year += 1

    # Ethiopian months ordered according to Gregorian
    order = [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4]
    ethiopian_month = order[m]

    return ethiopian_year, ethiopian_month, ethiopian_date

if __name__ == "__main__":
    print("Gregorian Date to Ethiopian Date Converter")
    print("Enter Gregorian Date:")
    year = int(input("Year: "))
    month = int(input("Month: "))
    date = int(input("Date: "))

    try:
        ethiopian_date = gregorian_to_ethiopian(year, month, date)
        print("Ethiopian Date: {}/{}/{}".format(ethiopian_date[0], ethiopian_date[1], ethiopian_date[2]))
    except ValueError as e:
        print("Error: {}".format(str(e)))
