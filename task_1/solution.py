import csv


class CountryDict:

    def __init__(self):
        self.count: int = 0
        self.people: list[str] = []

    @property
    def values(self) -> dict[str, list | int]:
        return {'people': self.people, 'count': self.count}

    # @values.setter
    def add_value(self, person_name: str):
        self.people.append(person_name)
        self.count += 1


class Agregator:

    def __init__(self):
        self.result_dict: dict[str, CountryDict] = {}

    def update(self, person_country: dict[str, str]) -> None:
        country = person_country['country']
        person = person_country['person']

        country_dict = self.result_dict.setdefault(country, CountryDict())
        country_dict.add_value(person)

    @property
    def result(self) -> dict[str, dict[str, list | int]]:
        return {country_name: country_dict.values for country_name, country_dict in self.result_dict.items()}


def main(file_path: str) -> None:
    agregator = Agregator()

    with open(file_path, 'r', encoding='utf8') as csv_data_file:
        file_reader = csv.DictReader(csv_data_file, delimiter=',')

        for row in file_reader:
            agregator.update(row)

    agregatoin_result = agregator.result
    print(agregatoin_result)


if __name__ == '__main__':
    FilePath = 'data.csv'
    main(FilePath)

