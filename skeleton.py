from collections import UserDict
from datetime import datetime, date


class Field:
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError
        self.__value = value

    def __eq__(self, other):
        return self.__value == other

    def __ne__(self, other):
        return self.__value != other

    def __str__(self):
        return str(self.value)

    def is_valid(self, value):
        return True


class Name(Field):
    pass


class Phone(Field):

    def is_valid(self, value):
        value = str(value)
        return value.isdigit() and len(value) == 10


class Birthday(Field):

    def is_valid(self, value):
        try:
            date(*[int(x) for x in value.split()])
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, phone=None, birthday=None):  # input only str
        self.name = Name(name)
        self.phones = []
        if phone:
            self.phones.append(Phone(phone))
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if self.birthday:
            bday = date(*[int(x) for x in str(self.birthday.value).split()])
            current_date = datetime.now()
            next_birthday = datetime(current_date.year, bday.month, bday.day)
            if current_date > next_birthday:
                next_birthday = datetime(current_date.year + 1, bday.month, bday.day)
            delta = next_birthday - current_date
            return delta.days
        return None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def edit_phone(self, phone, new_phone):  # debug
        phone = Phone(phone)
        if phone in self.phones:
            new_phone = Phone(new_phone)
            self.phones[self.phones.index(phone)] = new_phone
        else:
            raise ValueError

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.pop(self.phones.index(phone))
        else:
            raise ValueError

    def find_phone(self, item):
        if item in self.phones:
            return Phone(item)
        else:
            return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record):
        if record.name.value in self.data:
            return self.data[record.name.value]
        self.data[record.name.value] = record
        return Record(record)

    def find(self, name):
        try:
            return self.data[name]
        except KeyError:
            return None

    def delete(self, name):
        if name in self.data.keys():
            self.data.pop(name)
        else:
            return None

    def iterator(self, n=3):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i: i+n]

    def __str__(self):
        return "\n".join(str(p) for p in self.data.values())
