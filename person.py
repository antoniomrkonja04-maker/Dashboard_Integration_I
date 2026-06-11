import json
from PIL import Image
from datetime import date

def get_person_data():
    with open("data/person_db.json", "r", encoding="utf-8") as file:
        person_data = json.load(file)
    person_object_list = []
    for person_dict in person_data:
        person_object = Person(
            person_dict["id"],
            person_dict["date_of_birth"],
            person_dict["firstname"],
            person_dict["lastname"],
            person_dict["picture_path"],
            person_dict["ekg_tests"],
            person_dict["gender"]
        )
        person_object_list.append(person_object)
    return person_object_list


def get_person_object_by_full_name(full_name):
    persons = get_person_data()
    firstname = full_name.split(", ")[1]
    lastname = full_name.split(", ")[0]
    for person in persons:
        if person.firstname == firstname and person.lastname == lastname:
            return person


class Person:

    def __init__(self, id, date_of_birth, firstname, lastname, picture_path, ekg_tests, gender="Male"):
        self.id = id
        self.date_of_birth = date_of_birth
        self.firstname = firstname
        self.lastname = lastname
        self.picture_path = picture_path
        self.ekg_tests = ekg_tests
        self.gender = gender

    @staticmethod
    def load_by_id(person_id):
        persons = get_person_data()
        for person in persons:
            if person.id == person_id:
                return person

    def calc_age(self):
        return date.today().year - int(self.date_of_birth)

    def calc_max_heart_rate(self):
        age = self.calc_age()
        if self.gender.lower() == "female":
            return round(206 - 0.88 * age)
        return round(220 - age)

    def get_full_name(self):
        return self.lastname + ", " + self.firstname

    def get_image(self):
        return Image.open(self.picture_path)
