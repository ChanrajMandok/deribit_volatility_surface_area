from typing import Iterator

class StoreSimpleInterface:

    def __init__(self):
        self.strings_list = []

    def add(self, string_value: str):
        if string_value not in self.strings_list:
            self.strings_list.append(string_value)

    def remove(self, string_value: str):
        if string_value in self.strings_list:
            self.strings_list.remove(string_value)
            
    def update(self, new_strings: list[str]):
        self.strings_list = list(set(new_strings))

    def get_all(self) -> list[str]:
        return self.strings_list

    def __len__(self) -> int:
        return len(self.strings_list)

    def __iter__(self) -> Iterator[str]:
        return iter(self.strings_list)