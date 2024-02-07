from types import FunctionType
import pickle
from skeleton import *


class PhoneNotFoundError(Exception):
    pass

class Bot:

    def __init__(self):
        self.file = 'contacts.json'
        self.book = AddressBook()
        try:
            with open(self.file, 'rb') as fh:
                contacts = pickle.load(fh)
                self.book.data = contacts
        except:
            print("Created new AddressBook")

    @staticmethod
    def input_error(func):
        def inner(*args, **kwargs):

            try:
                result = func(*args, **kwargs)
                return result
            except IndexError as err:
                return "< help ?"
            except KeyError as err:
                return "< help ?"
            except ValueError as err:
                return "< help ?"
            except PhoneNotFoundError as err:
                return "Phone is not exist in contact!"

        return inner

    @input_error
    def hello(self, command):
        return "How can I help you?"

    @input_error
    def add(self, command):
        action, name, phone_number = command.split()
        if name not in self.book.data.keys():
            record = Record(name, phone_number)
            self.book.add_record(record)
            return f"Contact {name} added successfully"
        else:
            try:
                self.book.data[name].phones.remove(phone_number)
            except ValueError:
                self.book.data[name].phones.append(Phone(phone_number))
                return f"Contact {name} updated successfully!"

    @input_error
    def change(self, command):
        action, name, old_phone, new_phone = command.split()
        if name in self.book.data.keys():   # need find upd
            try:
                self.book.data[name].phones.remove(old_phone)
            except ValueError:
                raise PhoneNotFoundError("Phone number is not found")
            self.book.data[name].phones.append(Phone(new_phone))
            return "Contact updated successfully!"
        raise ValueError("Contact not found in my base!")

    @input_error
    def phone(self, command):
        action, name = command.split()
        try:
            result = self.book.data[name]
        except:
            raise ValueError("Contact not found in my base!")
        return name + ' --> ' + str(result.phones[0])

    @input_error
    def show_all(self, command):
        if command != "show all":
            raise KeyError

        if not self.book.data:
            return "Contacts library is empty"

        return self.book

    def search(self, command):
        text = command.replace("search", "")
        text = text.strip().lower()
        result = []
        if not text:
            return result
        for record in self.book.data.values():
            if text in record.name.value.lower() + " ".join([phone.value for phone in record.phones]):
                result.append(str(record))
        return "\n".join(i for i in result)

    @input_error
    def exit(self, user_input):
        if user_input in ("good bye", "exit", "close", "."):
            with open(self.file, 'wb') as fh:
                pickle.dump(self.book.data, fh)
            return "Good bye!"
        raise KeyError

    @input_error
    def get_operation(self, user_input):
        operations = {
            "hello": self.hello,
            "add": self.add,
            "change": self.change,
            "phone": self.phone,
            "show": self.show_all,
            "search": self.search,
            "good": self.exit,
            "exit": self.exit,
            "close": self.exit,
            ".": self.exit
        }
        operation = user_input.split()[0]
        return operations[operation]

    def run(self):
        while True:

            user_input = input(" >-- ").lower().strip()
            func = self.get_operation(user_input)
            result = func(user_input)
            print(result)

            if result == 'Good bye!':
                break
