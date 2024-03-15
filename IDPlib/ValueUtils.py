import datetime
import functools
import re
import operator
from decimal import ROUND_HALF_UP, Decimal

from fuzzywuzzy import fuzz


def replace_newline(func):
    def wrapper(*args, **kwargs):
        # first convert any None type args or kwargs to empty strings
        args = ["" if isinstance(arg, type(None)) else arg for arg in args]
        kwargs = {
            key: "" if isinstance(value, type(None)) else value
            for key, value in kwargs.items()
        }

        args = [arg.replace("\n", " ") if isinstance(arg, str) else arg for arg in args]
        kwargs = {
            key: value.replace("\n", " ") if isinstance(value, str) else value
            for key, value in kwargs.items()
        }
        return func(*args, **kwargs)

    return wrapper


class Normalise:
    @staticmethod
    def digit(value: str, pattern: str = r"[ -\$,]") -> str:
        """
        Removes spaces and dashes from a given string.
        """
        return re.sub(pattern, "", value)

    @staticmethod
    def safe_round(value: float, decimal_places: int = 2) -> float:
        # Convert the float to a Decimal object
        decimal_value = Decimal(str(value))

        # Round the Decimal object to n decimal places using proper rounding
        rounded_decimal = decimal_value.quantize(
            Decimal("1e-{}".format(decimal_places)), rounding=ROUND_HALF_UP
        )

        # Convert the rounded Decimal back to a float
        rounded_float = float(rounded_decimal)

        return rounded_float

    class Date:
        @staticmethod
        @replace_newline
        def from_string(value: str):
            """
            Converts a string date into a datetime object by trying different date formats and
            returning a default date if none of the formats work.

            :param value: a string representing a date in various formats, such as '2022-01-01', 'Jan. 1, 2022',
            '1/1/22', etc
            :return: a datetime object representing the input date string in one of the specified formats, or a
            datetime object representing the date '31/12/2999' if none of the formats match the input string.
            """
            try:
                symbols = ["-", ".", "_", " "]
                value = value.lower()

                for s in symbols:
                    value = value.replace(s, "/")

                for appendix in ["nd", "th", ","]:
                    value = value.replace(appendix, "")

                # replace all occurences of 'st' in date
                # but not in the special case of 'august'
                value = re.sub(r"(?<!augu)st", "", value)

                formats = [
                    "%Y/%m/%d",
                    "%Y/%b/%-d",
                    "%Y/%b/%d",
                    "%d/%m/%Y",
                    "%-d/%m/%Y",
                    "%d/%b/%Y",
                    "%d%B%Y",
                    "%d/%B/%Y",
                    "%d/%m/%y",
                    "%-d/%m/%y",
                    "%d/%b/%y",
                    "%d%B%y",
                    "%d/%B/%y",
                ]

                for date_format in formats:
                    try:
                        dt = datetime.datetime.strptime(value, date_format)
                        return dt
                    except ValueError:
                        pass
            except:
                pass

            return datetime.datetime.strptime("31/12/2999", "%d/%m/%Y")

        @staticmethod
        def tax_year(value):
            """
            Takes a date as either string or datetime and returns the tax year
            """
            if isinstance(value, str):
                value = Normalise.Date.from_string(value)
            if value.month >= 7:
                return value.year + 1
            else:
                return value.year


class Compare:
    @staticmethod
    def digits(value1: str, value2: str) -> bool:
        """
        The function `digits` compares two string values after normalizing
        them as digits and returns a
        boolean indicating if they are equal.

        :param value1: The function normalizes the input strings using a method
        `Normalise.digit` and then compares the normalized values to check
        if they are equal
        :type value1: str
        :type value2: str
        :return: a boolean value indicating whether the normalised versions
        of the two input values are
        equal.
        """
        normalised1 = Normalise.digit(value=value1)
        normalised2 = Normalise.digit(value=value2)
        return normalised1 == normalised2

    @staticmethod
    @functools.lru_cache(maxsize=128)
    @replace_newline
    def string_with_percent(
        value1: str, value2: str, threshold: int = 88, token_ratio: int = 89
    ):
        value = fuzz.WRatio(value1, value2)
        if value < threshold:
            value = fuzz.token_sort_ratio(value1, value2)
            if value > token_ratio:
                return True, value
            else:
                return False, value
        return True, value

    @staticmethod
    @functools.lru_cache(maxsize=128)
    @replace_newline
    def string(
        value1: str, value2: str, threshold: int = 88, token_ratio: int = 89
    ) -> bool:
        result, _ = Compare.string_with_percent(value1, value2, threshold, token_ratio)
        return result


class Identify:
    @staticmethod
    def credit_card_number(value):
        """
        Attempts to identify if the value presented is a credit card
        Note, this isnt 100% but it is reasonably successful. If you dont like
        the outcome you are welcome to submit a patch
        """
        # Normalise the value
        try:
            cc_num = "".join(filter(str.isdigit, value))

            if len(cc_num) == 16 and cc_num.isdigit():
                digits = list(map(int, cc_num))
                doubled_digits = [
                    2 * digit if index % 2 else digit
                    for index, digit in enumerate(digits[::-1])
                ]
                summed_digits = sum(
                    digit - 9 if digit > 9 else digit for digit in doubled_digits
                )

                if summed_digits % 10 == 0:
                    return True
        except:
            pass
        finally:
            # Basic Check

            ## is Visa
            pattern = r"^4[0-9]"
            match = re.search(pattern, value)
            if match:
                return True

            ## is MasterCard
            pattern = r"^5[1-5][0-9]"
            match = re.search(pattern, value)
            if match:
                return True

            ## Is Discover
            if (
                value.startswith("6011")
                or value.startswith("644")
                or value.startswith("65")
            ):
                return True

            ## is Amex
            if value.startswith("34") or value.startswith("37"):
                return True

        return False

    @staticmethod
    def abn(value):
        """
        Checks if a given string meets the requirements of a valid abn number
        """
        abn = str(value).replace(" ", "").replace("-", "")
        if not abn.isdigit() or len(abn) != 11:
            return False

        weighting = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        modulus = 89

        temp_abn = [int(c) for c in abn if c.isdigit()]
        temp_abn[0] -= 1

        check_sum = sum(map(operator.mul, temp_abn, weighting)) % modulus
        if check_sum != 0:
            return False
        return True

    @staticmethod
    def tfn(value):
        """
        Checks if a given string meets the requirements of a valid tfn number
        """
        tfn = str(value).replace(" ", "")
        if not tfn.isdigit() or len(tfn) != 9:
            return False
        weighting = [1, 4, 3, 7, 5, 8, 6, 9, 10]
        check_sum = sum(int(tfn[i]) * weighting[i] for i in range(9))
        return check_sum % 11 == 0

    @staticmethod
    def tfn_in_string(value, max_gap=6):
        """
        Checks if a given string contains a substring which meets the requirements
        of a valid tfn number
        max gap is the maximum amount of non digit characters between digit values
        """
        pattern = r"\d{3}\s?\d{3}\s?\d{3}"
        match = re.search(pattern, value)
        if match:
            tfn = match.group(0)
            if tfn:
                return True

        def full_shift_check(string):
            """
            The function checks for valid tfn's in a given string and returns a list of valid tfn's.

            :param string: The input string that contains one or more potential tfn's to be
            checked
            :return: a list of valid tfn's found in the input string. If no valid
            tfn's are found, an empty list is returned.
            """
            pattern = r"\d+"
            digits = re.findall(pattern, string)
            stream = "".join(digits)
            if len(stream) < 9:
                return False
            groups = []
            for i in range(len(stream) - 8):
                group = stream[i : i + 9]
                if not group.startswith("0"):
                    groups.append(group)

            found_tfns = []
            for item in groups:
                if Identify.tfn(item):
                    found_tfns.append(item)
            return found_tfns

        pattern = rf"(?:(?:\ |\-){{0,{max_gap}}}(?:\d)){{8,}}"
        matches = re.findall(pattern, value)  # Search for potential TFNs
        cleansed_matches = []
        for match in matches:
            cleansed_matches.append(match.replace("-", "").replace(" ", ""))

        for match in cleansed_matches:
            if full_shift_check(match):
                return True
        return False
