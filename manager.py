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
