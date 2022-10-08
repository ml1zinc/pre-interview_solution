import csv

from dataclasses import dataclass, field

PersonCountry = dict[str, list | int]
AggregatoinResult = dict[str, PersonCountry]


@dataclass
class CountryDict:
    count: int = 0
    people: list[str] = field(default_factory=list)


    @property
    def values(self) -> PersonCountry:
        return {'people': self.people, 'count': self.count}

    def add_value(self, person_name: str):
        self.people.append(person_name)
        self.count += 1


class Aggregator:

    def __init__(self) -> None:
        self.result_dict: dict[str, CountryDict] = {}

    def update(self, person_country: dict[str, str]) -> None:
        country = person_country['country']
        person = person_country['person']

        country_dict = self.result_dict.setdefault(country, CountryDict())
        country_dict.add_value(person)

    @property
    def result(self) -> AggregatoinResult:
        return {country_name: country_dict.values for country_name, country_dict in self.result_dict.items()}


def main(file_path: str) -> None:
    aggregator = Aggregator()

    with open(file_path, 'r', encoding='utf8') as csv_data_file:
        file_reader = csv.DictReader(csv_data_file, delimiter=',')

        for row in file_reader:
            aggregator.update(row)

    agregatoin_result = aggregator.result
    print(agregatoin_result)


if __name__ == '__main__':
    FilePath = 'data.csv'
    main(FilePath)

