from collections import UserDict
from datetime import datetime
from pickle import dump, load

class Field:
    def __init__(self, value=None):
        self.__value = None
        self.value = value

class Name(Field):
    pass

class Phone(Field):

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if len(value) in [10, 12, 13]:
            self.__value = value
        else:
            raise ValueError

class Birthday(Field):

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if not value or len(value) == 10:
            self.__value = value
        else:
            raise ValueError

class Record:
    def __init__(self, name, phone, birthday):
        self.name = name
        self.phones = [phone]
        self.birthday = birthday
    
    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def change_phone(self, phone):
        self.phones.pop()
        self.phones.append(phone)

    def days_to_birthday(self):
        if self.birthday:
            current_datetime = datetime.now().date()
            d, m, y = self.birthday.value.split(".")
            birthday_date = datetime(year=int(y), month=int(m), day=int(d))
            new_datetime = birthday_date.replace(year=current_datetime.year).date()
            difference = new_datetime - current_datetime
            return difference

class AddressBook(UserDict):
    def __init__(self, n):
        super().__init__()
        self.n = n
        
    def add_record(self, record):
        self.data.update({record.name.value: record})

    def iterator(self):
        for i, record in enumerate(self.data.values()):
            print(record.name.value, [x.value for x in record.phones])
            if i and (i+1) % self.n == 0:
                yield ""   
    
def main():
    def input_error(func):
        def inner(string):
            try:
                func(string)
            except IndexError:
                print("Give me name and phone please")
            except (KeyError, ValueError):
                print("Enter user name")
        return inner
    
    @input_error
    def handler_add(string):
        parser = string.split(" ")
        name = Name(parser[1].capitalize())

        try:
            phone = Phone(parser[2])
        except ValueError:
            print("Uncorrect number")

        try:
            birthday = Birthday(parser[3])
        except ValueError:
            print("Uncorrect birthday")
        except IndexError:
            birthday = Birthday()

        try:
            if name.value not in ab.data:
                rec = Record(name, phone, birthday)
                ab.add_record(rec)
            else:
                ab[name.value].add_phone(phone)
        except UnboundLocalError:
            pass

    @input_error
    def handler_remove(string):
        parser = string.split(" ")
        name = parser[1].capitalize()
        for phone in ab[name].phones:
            if phone.value == parser[2]:
                ab[name].remove_phone(phone)
            
    @input_error
    def handler_change(string):
        parser = string.split(" ")
        name = parser[1].capitalize()
        phone = Phone(parser[2])
        ab[name].change_phone(phone)
    
    @input_error
    def handler_phone(string):
        parser = string.split(" ")
        name = parser[1].capitalize()
        print([x.value for x in ab[name].phones]) 

    @input_error
    def handler_birthday(string):
        parser = string.split(" ")
        name = parser[1].capitalize()
        days_to_birthday = str(ab[name].days_to_birthday()).split(",")
        print(f"{days_to_birthday[0]} to {name}'s birthday")

    @input_error
    def handler_search(string):
        parser = string.split(" ")
        search = parser[1]
        for v in ab.data.values():
            if search in v.name.value.lower():
                print(v.name.value, [x.value for x in v.phones])
            else:
                for ch in [x.value for x in v.phones]:
                    if search in ch:
                        print(v.name.value, [x.value for x in v.phones])
                
    def handler_show_all():
        for ch in ab.iterator():
            print(ch)

    try:
        with open("data.bin", "rb") as fh:
            ab = load(fh)
    except FileNotFoundError:
        ab = AddressBook(5)

    while True:
        string = input().lower()
        if string in ["good bye", "close", "exit"]:
            print("Good bye!")
            with open("data.bin", "wb") as fh:
                dump(ab, fh)
            break
        elif string == "hello":
            print("How can I help you?")
        elif string == "show all":
            handler_show_all()
        elif string.startswith("add"):
            handler_add(string)
        elif string.startswith("delete"):
            handler_remove(string)
        elif string.startswith("change"):
            handler_change(string)
        elif string.startswith("phone"):
            handler_phone(string)
        elif string.startswith("birthday"):
            handler_birthday(string)
        elif string.startswith("search"):
            handler_search(string)

if __name__ == "__main__":
    main()