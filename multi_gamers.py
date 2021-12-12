import json
from functions import *


with open('russian.txt', 'r', encoding="windows-1251") as file:
    russian_words = file.readlines()

results = {"Users": {}, "Word": read_file("https://jsonkeeper.com/b/S3F0"), "Words": []}

gamers = get_gamers_list(int(input("Добро пожаловать в игру!\nВведите количество игроков\n")), results)

print(f"Игра начинается!\nВаше слово на эту игру:\n{results['Word'].upper()}\n")

check_word(gamers, results, russian_words)
print_results(gamers)

file = open("winners.json", "w")
json.dump(results, file)
file.close()
print("======\nДанные записаны в файл")
