import re

with open("5words_new.txt") as file:
    WORDS = file.readlines()

BAD_LETTERS = set()
GOOD_LETTERS = set()


class Words:
    def __init__(self):
        self._words = set()

    @property
    def get_words(self):
        return self._words

    def set_words(self, words: set[str]):
        self._words = words


PERHAPS_WORDS = Words()


def check_bad_letter(word: str) -> bool:
    for letter in BAD_LETTERS:
        if letter in word:
            return True
    return False


def check_good_letter(word: str) -> bool:
    _count = 0
    for letter in GOOD_LETTERS:
        if letter in word:
            _count += 1
    if _count == len(GOOD_LETTERS):
        return False
    return True


def find_word(reg_exp: str) -> set[str]:
    words = set()
    for word in PERHAPS_WORDS.get_words if len(PERHAPS_WORDS.get_words) else WORDS:
        if check_good_letter(word):
            continue
        if check_bad_letter(word):
            continue
        result = re.findall(reg_exp, word)
        if result:
            words.add(result[0])
    if len(PERHAPS_WORDS.get_words):
        PERHAPS_WORDS.set_words(PERHAPS_WORDS.get_words & words)
    else:
        PERHAPS_WORDS.set_words(words)
    return words


def update_good_and_bad_letters(result: str) -> str:
    reg_exp_index = 0
    reg_exp = "^"
    for index, char in enumerate(result):
        try:
            is_bad_letter = result[index + 1] == "!"
        except IndexError:
            is_bad_letter = False
        if is_bad_letter:
            BAD_LETTERS.add(char.lower())
        elif char == "!":
            continue
        else:
            try:
                BAD_LETTERS.remove(char.lower())
            except KeyError:
                pass
            GOOD_LETTERS.add(char.lower())
        if char.islower():
            reg_exp += f"[^{char}]" if not is_bad_letter else "\\D"
        else:
            reg_exp += f"\\{char.lower()}"
        reg_exp_index += 1
    return f"{reg_exp}$"


def main():
    # ! после буквы - такой буквы в слове нет (а!)
    # буквы в нижнем регистре - такая буква в слове есть, но стоит не на том месте (а)
    # буква в верхем регистре - такая буквы есть и стоит на своем месте (А)
    # "о!п!е!р!а!" - в слове нет таких букв как О, П, Е, Р, А
    # "мИд!Ия!" - в слове нету букв Д и Я. Буква М стоит не на своем месте. Буквы И стоят на своем месте
    for result in ["опе!р!а!", "ПиЛот!"]:
        reg_exp = update_good_and_bad_letters(result)
        words = find_word(reg_exp)
    print(f"Подходит {len(words)} слов(а):")
    print(*words, sep="\n")


if __name__ == "__main__":
    main()
