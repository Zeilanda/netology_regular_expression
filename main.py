import re

# читаем адресную книгу в формате CSV в список contacts_list
import csv


def get_lists_of_data():
    with open("phonebook_raw.csv", encoding='utf-8', newline='') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    result = []
    for i, parts in enumerate(contacts_list):
        if i == 0:
            result.append(parts)
        else:
            line_parts = []
            lastname, firstname, surname = get_all_name(*parts[0:3])
            line_parts += lastname, firstname, surname, parts[3], parts[4]
            if parts[5] == '':
                line_parts.append(parts[5])
            else:
                phone = regular_phone(parts[5])
                line_parts.append(phone)
            line_parts.append(parts[6])
            result.append(line_parts)
    return result


def get_all_name(lastname: str, firstname: str, surname: str) -> tuple[str, str, str]:
    """
    Possible inputs:
    "ФИО", "", ""
    "Ф", "ИО", ""
    "Ф", "И", "О"
    Result:
    "Ф", "И", "О"
    :param lastname:
    :param firstname:
    :param surname:
    :return:
    """
    if lastname and firstname and surname:
        return lastname, firstname, surname
    elif lastname and firstname and not surname:
        firstname, surname = firstname.split()
        return lastname, firstname, surname
    else:
        name_data = lastname.split()
        if len(name_data) == 3:
            lastname, firstname, surname = name_data
            return lastname, firstname, surname
        else:
            lastname = name_data[0]
            firstname = name_data[1]
            surname = ''
            return lastname, firstname, surname


def regular_phone(phone: str) -> str:
    re_match = re.search(r'\+?(?:7|8) ?\(?(\d{3})\)? ?-?(\d{3})-?(\d{2})-?(\d{2})(?: ?\(?доб\. (\d{4})\)?)?', phone)
    if re_match.group(5):
        additional = f'доб. {re_match.group(5)}'
        result = f'+7({re_match.group(1)}){re_match.group(2)}-{re_match.group(3)}-{re_match.group(4)} {additional}'
        return result
    result = f'+7({re_match.group(1)}){re_match.group(2)}-{re_match.group(3)}-{re_match.group(4)}'
    return result


def compare_values(x, y):
    if x == y:
        return True
    else:
        return False


def get_double_strings_index(phone_list: list[list[str]]) -> list[tuple[int, int]]:
    result_list = []
    for i, data_first in enumerate(phone_list):
        for j, data_second in enumerate(phone_list):
            if i > j:
                result = list(map(compare_values, data_first, data_second))
                if result[0] and result[1]:
                    result_list.append((i, j))
    return result_list


def concatenate_strings(string_1: str, string_2: str) -> str:
    if string_1 == '' and string_2:
        return string_2
    elif string_2 == '' and string_1:
        return string_1
    else:
        return string_1


def merge_strings(first_string: list[str], second_string: list[str]) -> list[str]:
    result = list(map(concatenate_strings, first_string, second_string))
    return result


def merge_duplicated_strings(strings: list[list[str]]):
    double_strings_index = get_double_strings_index(strings)
    result = []
    for i, str_ in enumerate(strings):
        for index_pair in double_strings_index:
            if i == index_pair[0]:
                str_ = merge_strings(strings[index_pair[0]], strings[index_pair[1]])
            elif i == index_pair[1]:
                str_ = ""
        if str_:
            result.append(str_)

    return result


def export_csv(data_list):
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(data_list)


if __name__ == "__main__":
    list_data = get_lists_of_data()
    # pprint(list_data)
    fixed_data = [list_data[0]] + merge_duplicated_strings(list_data[1:])
    export_csv(fixed_data)
