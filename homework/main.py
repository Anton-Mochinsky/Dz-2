from pprint import pprint
import csv
import re
from collections import OrderedDict


with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def create_dict(phonebook):
    list_phonebook = []
    for person in phonebook:
        dict_person = OrderedDict(dict(zip(phonebook[0], person)))
        list_phonebook.append(dict_person)
    return list_phonebook


def ordered_fio(phonebook):
    for person in phonebook:
        person_fio = str(person['lastname'] + ' ' + person['firstname'] + ' ' + person['surname'])
        person_fio = person_fio.split(' ')
        person_fio = [x for x in person_fio if x != '']
        try:
            person['lastname'] = person_fio[0]
            person['firstname'] = person_fio[1]
            person['surname'] = person_fio[2]
        except:
            pass
    return phonebook


def ordered_phone_numbers(phonebook):
    for person in phonebook:
        phone_number = person['phone']
        phone_number = re.sub(r'(\+7|8)\s?\(?(\d{3})\)?\s?\-?(\d{3})\-?(\d{2})\-?(\d{2})',
                              '+7(\\2)\\3-\\4-\\5', phone_number)
        phone_number = re.sub(r'\s*\(?\s*(\доб.)\s?(\d+)\)?',
                              ' \\1\\2', phone_number)
        person['phone'] = phone_number
    return phonebook


def search_for_matches(phonebook):
    for person in phonebook:
        for contact_for_comparison in phonebook:
            if person != contact_for_comparison and person['lastname'] == contact_for_comparison['lastname'] \
                    and person['firstname'] == contact_for_comparison['firstname']:
                for x, y in person.items():
                    if y == '':
                        person[x] = contact_for_comparison[x]
                phonebook.remove(contact_for_comparison)
    return phonebook


def create_list(phonebook):
    correct_list_phonebook = []
    for person in phonebook:
        person = list(person.values())
        correct_list_phonebook.append(person)
    return correct_list_phonebook


if __name__ == '__main__':
    created_dict = create_dict(contacts_list)
    ordered_fio = ordered_fio(created_dict)
    ordered_phone_numbers = ordered_phone_numbers(ordered_fio)
    searching_for_matches = search_for_matches(ordered_phone_numbers)
    correct_list = create_list(searching_for_matches)
    pprint(correct_list)

with open("phonebook.csv", "w", encoding='utf-8') as f:
    data_writer = csv.writer(f, delimiter=',')
    data_writer.writerows(correct_list)
