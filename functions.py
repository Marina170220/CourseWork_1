from Gamer import *
import requests
import random


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

    winners_number = 0
    max_score = 0

    print("Игра окончена\n======")

    if len(list_) == 1:
        print(f"Игрок {list_[0].name}, Вы набрали {list_[0].score}")

    elif len(list_) > 1:

        for g in list_:
            print(f"Игрок {list_.index(g) + 1} {g.name} - {g.score}")

            if g.score > max_score:
                max_score = g.score
                winner = g
                winners_number = list_.index(g) + 1

        print(f"======\nПобедил игрок {winners_number} {winner.name}")
    else:
        print("Победителя нет")


def get_gamers_list(num, dict_, list_=[]):
    """
    Формирует список с заданным количеством участников игры
    :param num: количество игроков, введённое пользователем
    :param dict_: словарь с результатами игры
    :param list_: пустой список игроков
    :return: список игроков
    """
    if num > 0:
        if num == 1:
            list_.append(Gamer(input(f"Введите имя игрока\n")))
        else:
            for i in range(num):
                list_.append(Gamer(input(f"Введите имя {i + 1}-го игрока\n")))
                dict_["Users"][i] = list_[i].name
    else:
        get_gamers_list(int(input("Введите корректное число\n")), dict_)
    return list_


def check_word(list_, dict_, rus, stop=False):
    """
    Проверяет составленные игроками слова, заносит результаты в словарь с итогами игры
    :param rus: список русских слов
    :param list_: список игроков
    :param dict_: словарь с результатами игры
    :param stop: флаг прерывания игры участником
    """
    stop_words = ["stop", "стоп"]

    while not stop:
        print(f"======\nНачало раунда\n{dict_['Word']}")

        for gamer in list_:
            is_word_correct = True
            check_letters_word = dict_['Word']  # переменная для проверки использования букв,
            # входящих в выпавшее в игре слово

            users_word = input(f"Ходит игрок {gamer.name}\n").lower()

            if users_word in stop_words:
                stop = True
                break

            elif users_word in dict_["Words"]:
                print("Такое слово уже было")
                continue

            elif (users_word + "\n") not in rus:
                print("В русском языке нет такого слова")
                continue

            else:
                for letter in users_word:
                    if letter in check_letters_word.lower():
                        check_letters_word = check_letters_word.replace(letter, '*', 1)

                    else:
                        print("Использованы недопустимые буквы")
                        is_word_correct = False
                        break

                if is_word_correct:
                    gamer.words.append(users_word)
                    dict_["Words"].append(users_word)
                    gamer.score += len(users_word)
                    print("Принято")
                    continue
