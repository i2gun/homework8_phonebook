# Создать телефонный справочник с возможностью импорта и экспорта
# данных в формате .txt. Фамилия, имя, отчество, номер телефона - 
# данные, которые должны находиться в файле.
# 1. Программа должна выводить данные
# 2. Программа должна сохранять данные в текстовом файле
# 3. Пользователь может ввести одну из характеристик для поиска определенной записи(Например имя или фамилию человека)
# 4. Использование функций. Ваша программа не должна быть линейной

# Дополнить справочник возможностью копирования данных из одного
# файла в другой. Пользователь вводит номер строки, которую
# необходимо перенести из одного файла в другой.

#=================================================================
#
#

from os.path import exists
from csv import DictReader, DictWriter, reader

#===========   Используемые классы  ==============================
#
#

class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


class LenNameError(Exception):
    def __init__(self, txt):
        self.txt = txt

#===========   Используемые функции  ==============================
#
#

#----- check_criteria(), get_valid_data() - проверка валидности ---

def check_criteria(data, criteria):
    if criteria == "имя" or criteria == "фамилию":
        return len(data) < 2
    elif criteria == "номер телефона":
        return len(str(data)) != 11


def get_valid_data(msg: str, exception_type: Exception) -> str:
    while True:
        try:
            data = input("Введите " + msg + ": ")
            if check_criteria(data, msg):
                raise exception_type
            else:
                return data
        except exception_type.__class__ as err:
            print(err)
            continue

#------------  Ниже функции реализующие команды  ----------------------

def get_info() -> list:
    first_name = get_valid_data("имя", LenNameError("Имя слишком короткое"))
    last_name = get_valid_data("фамилию", LenNameError("Фамилия слишком короткая"))
    phone_number = get_valid_data("номер телефона", LenNumberError("Неверная длина номера телефона"))

    return [first_name, last_name, phone_number]


def create_file(file_name):
    with open(file_name, "w", encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()


def read_file(file_name):
    with open(file_name, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_file(file_name, lst):
    res = read_file(file_name)
    obj = {"Имя": lst[0], "Фамилия": lst[1], "Телефон": lst[2]}
    res.append(obj)

    file_is_empty = False
    with open(file_name, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        if len(list(f_reader)) == 0:
            file_is_empty = True

    if file_is_empty:
        with open(file_name, "w", encoding='utf-8', newline='') as data:
            f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
            f_writer.writeheader()
    else:
        for el in res:
            if el["Телефон"] == str(lst[2]):
                print("Такой телефон уже есть")
                return

    with open(file_name, "w", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)


def search_in_file(file_name):
    while True:
        print("      ----------------")
        print("      | Выберите критерий поиска:")
        print("      | 1 - по имени")
        print("      | 2 - по фамилии")
        print("      | 3 - по номеру телефона")
        criteria = input("      | Критерий поиска: ")
        print("      ----------------")
        match criteria:
            case "1":
                field_name = "Имя"
                searching_item = get_valid_data("имя", LenNameError("Имя слишком короткое"))
                break
            case "2":
                field_name = "Фамилия"
                searching_item = get_valid_data("фамилию", LenNameError("Фамилия слишком короткая"))
                break
            case "3":
                field_name = "Телефон"
                searching_item = get_valid_data("номер телефона", LenNumberError("Неверная длина номера телефона"))
                break
            case _:
                print("Выбран неверный критерий")

    data_dictionary = read_file(file_name)
    res_list = list()

    # поиск всех вхождений искомого значения
    #  (например, несколько записей с одинаковыми именами)
    for el in data_dictionary:
        for key, value in el.items():
            if key == field_name and value == searching_item:
                res_list.append(el)
    return res_list


def copy_file(file_name):
    new_file_name = input("Введите имя файла принимающего строку: ")
    while True:
        try:
            line_number = int(input("Введите номер строки: "))
            break
        except Exception:
            print("Введен неверный номер строки")

    with open(file_name, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        gen = (row for idx, row in enumerate(f_reader) if idx == line_number)
        one_line = dict(*gen)

    if not exists(new_file_name):
        with open(new_file_name, "w", encoding='utf-8') as data:
            f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
            f_writer.writeheader()

    file_is_empty = False
    with open(new_file_name, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        if len(list(f_reader)) == 0:
            file_is_empty = True

    if file_is_empty:
        with open(new_file_name, "w", encoding='utf-8', newline='') as data:
            f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
            f_writer.writeheader()
    else:
        with open(new_file_name, "r", encoding='utf-8') as data:
            f_reader = DictReader(data)
            if one_line in f_reader:
                print("Такие данные уже есть в файле " + new_file_name)
                return

    with open(new_file_name, "a", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writerow(one_line)
        print(one_line)

#===========   Основная программа  =============================
#
#

phonebook = './phonebook.py'

while True:
    print()
    print("      -----------------------------")
    print("      | Доступные команды: q - выход, w - запись, r - чтение, s - поиск, c - копирование")
    command = input("      | Введите команду: ")
    print("      -----------------------------")
    print()
    match (command):
        case "q":
            break

        case "w":
            if not exists(phonebook):
                create_file(phonebook)
            write_file(phonebook, get_info())
            
        case "r":
            if not exists(phonebook):
                print("Нет файла для чтения. Создайте файл справочника")
                continue
            output = read_file(phonebook)
            for i in range(len(output)):
                print(output[i])
        
        case "s":
            if not exists(phonebook):
                print("Поиск отменен. Отсутствует файл. Создайте файл справочника")
                continue
            output = search_in_file(phonebook)
            print()
            for i in range(len(output)):
                print(output[i])

        case "c":
            if not exists(phonebook):
                print("Копирование невозможно. Файл отсутствует. Создайте файл справочника")
                continue
            copy_file(phonebook)
        
        case _:
            print("Введена неверная команда")