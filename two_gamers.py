import json
import random
import requests as requests
from Gamer import *


def read_file(url):
    """
    Выбирает случайное слово из списка слов для игры
    :param url: ссылка на список слов
    :return: выбранное слово для текущей игры
    """

    response = requests.get(url)
    words_list = response.json()
    random.shuffle(words_list)

    return words_list[0]


def print_results(list_):
    """
    Подведение итогов игры, вывод победителя
    :param list_: список игроков

    """
    print("Игра окончена\n======")
    print(f"Игрок 1 {list_[0].name} - {list_[0].score}\n"
          f"Игрок 2 {list_[1].name} - {list_[1].score}")

    if list_[0].score > list_[1].score:
        print(f"Победил игрок 1 - {list_[0].name}")

    elif list_[1].score > list_[0].score:
        print(f"======\nПобедил игрок 2 - {list_[1].name}")

    else:
        print("======\nПобедила дружба:)")


with open('russian.txt', 'r', encoding="windows-1251") as file:
    russian_words = file.readlines()

gamers = [Gamer(input("""Добро пожаловать в игру!
Введите имя первого игрока
""")),
          Gamer(input("Введите имя второго игрока\n"))]
print(f"{gamers[0].name.upper()} vs {gamers[1].name.upper()}, игра начинается!")

results = {"Users": {"1": gamers[0].name,
                     "2": gamers[1].name}, "Word": read_file("https://jsonkeeper.com/b/S3F0"), "Words": []}

stop_words = ["stop", "стоп"]
is_game_stopped = False

print(f"Ваше слово на эту игру:\n{results['Word'].upper()}\n")

while not is_game_stopped:
    print(f"======\nНачало раунда\n{results['Word']}")

    for gamer in gamers:
        is_word_correct = True
        check_letters_word = results['Word']  # переменная для проверки использования букв,
        # входящих в выпавшее в игре слово

        users_word = input(f"Ходит игрок {gamer.name}\n").lower()

        if users_word in stop_words:
            is_game_stopped = True
            break

        elif users_word in results["Words"]:
            print("Такое слово уже было")
            continue

        elif (users_word + "\n") not in russian_words:
            print("В русском языке нет такого слова")
            continue

        else:
            for letter in users_word.lower():
                if letter in check_letters_word.lower():
                    check_letters_word = check_letters_word.replace(letter, '*', 1)

                else:
                    print("Использованы недопустимые буквы")
                    is_word_correct = False
                    break

            if is_word_correct:
                gamer.words.append(users_word)
                results["Words"].append(users_word)
                gamer.score += len(users_word)
                print("Принято")
                continue

print_results(gamers)

file = open("winners.json", "w")
json.dump(results, file)
file.close()
print("======\nДанные записаны в файл")
