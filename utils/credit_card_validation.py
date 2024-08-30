import re
from datetime import date
""" make some validation over the credit card of the user """

def validate_credit_card_num(credit_card_num):
    """ check if the credit card number is valid or not """
    try:
        if credit_card_num == '' or credit_card_num is None:
            return 'Input is invalid'


        if ' ' in credit_card_num:
            credit_card_num = credit_card_num.replace(' ', '')

        length = len(credit_card_num)
        if length <= 19 and length > 13:
            sum = 0
            index = length
            idx = 1
            while index > 0:
                num = int(credit_card_num[index - 1])
                if idx % 2 == 0:
                    num = num * 2
                    if num > 9:
                        num = num - 9
                index -= 1
                idx += 1
                sum += num
            if sum % 10 == 0:
                return "Vaild number"

    except Exception as e:
        print(e)
    return "Invalid number"


def get_card_type(card_number, cvv):
    """ check the type of the card and the cvv """
    card_number = card_number.replace(' ', '')
    cvv = cvv.strip()
    credit_type = "Unknown type"

    card_types = {
        "Visa": r"^4[0-9]{12}(?:[0-9]{3})?$",
        "MasterCard": r"^5[1-5][0-9]{14}$",
        "American Express": r"^3[47][0-9]{13}$",
        "Discover": r"^6(?:011|5[0-9]{2})[0-9]{12}$",
        "JCB": r"^(?:2131|1800|35\d{3})\d{11}$",
        "Diners Club": r"^3(?:0[0-5]|[68][0-9])[0-9]{11}$"
    }

    for card_type, pattern in card_types.items():
        if re.match(pattern, card_number):
            result = False
            credit_type = card_type

    if credit_type == "American Express":
        result = re.match('^\d{4}$', cvv)
    else:
        result = re.match('^\d{3}$', cvv)

    if result is None:
        return "Invalid cvv"

    return credit_type


def verify_date(month, year):
    """ check the date of the card """
    if month[0] == 0:
        month = month[1]

    month = int(month)
    year = int(year)
    today = str(date.today()).split('-')
    current_year = int(today[0])
    current_month = int(today[1])

    if (year == current_year and month < current_month) or (year < current_year):
        return "Invalid date"

    return "Valid date"


def main():
    number = input("Enter you credit_card_num: ")
    cvv = input("Enter cvv of your card: ")
    month, year = input("Enter the date of your credit: ").split(" ")
    print(validate_credit_card_num(number))
    print(get_card_type(number, cvv))
    print(verify_date(month, year))
main()
