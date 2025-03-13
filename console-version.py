import os
import random

def clear_console():
    print("\n" * 100)

def display_rules():
    while True:
        clear_console()
        print("Zasady gry:")
        print("1. Gra rozpoczyna się od pustej sekwencji liter.")
        print("2. W każdej turze gracz dodaje jedną literę na początek lub koniec sekwencji.")
        print("3. Celem jest uformowanie słowa znajdującego się w słowniku.")
        print("4. Jeśli sekwencja nie może być częścią żadnego słowa, gracz przegrywa.")
        print("5. Drugi gracz może rzucić wyzwanie, jeśli uważa, że sekwencja nie prowadzi do poprawnego słowa.")
        print("6. Gra kończy się, gdy ktoś uformuje słowo lub popełni błąd.")
        print("\n1. Powrót do menu")

        choice = input("Wybierz opcję (1): ").strip()
        if choice == "1":
            break
        else:
            print("Nieprawidłowy wybór, spróbuj ponownie.")

def computer_turn(sequence, dictionary):
    potential_moves = []
    for letter in "abcdefghijklmnopqrstuvwxyz":
        for new_seq in [letter + sequence, sequence + letter]:
            if any(word.startswith(new_seq) or word.endswith(new_seq) for word in dictionary):
                potential_moves.append((new_seq, letter))

    if potential_moves:
        chosen_move = random.choice(potential_moves)
        print(f"Komputer dodał literę '{chosen_move[1]}'.")
        return chosen_move[0]
    else:
        print("Komputer nie może dodać litery i przegrywa!")
        return None

def word_game(dictionary, vs_computer=False):
    player1 = input("Podaj imię Gracza 1: ").strip()
    player2 = "Komputer" if vs_computer else input("Podaj imię Gracza 2: ").strip()
    players = [player1, player2]
    clear_console()

    current_player = random.randint(0, 1)
    print(f"Losowanie: Grę rozpoczyna {players[current_player]}!")

    while True:
        current_sequence = ""

        while True:
            print(f"\nAktualna sekwencja: '{current_sequence}'")
            print(f"Tura {players[current_player]}:")

            if vs_computer and players[current_player] == "Komputer":
                current_sequence = computer_turn(current_sequence, dictionary)
                if current_sequence is None:
                    print(f"{players[current_player]} przegrywa!")
                    break
            else:
                move = input("Dodaj literę na początek lub koniec sekwencji (np. 'a', 'b', ...): ").strip()
                if len(move) != 1 or not move.isalpha():
                    print("Należy wprowadzić tylko jedną literę!")
                    continue

                print("1. Dodaj na początek")
                print("2. Dodaj na koniec")
                while True:
                    position = input("Wybierz opcję (1 lub 2): ").strip()
                    if position == "1":
                        current_sequence = move + current_sequence
                        break
                    elif position == "2":
                        current_sequence = current_sequence + move
                        break
                    else:
                        print("Nieprawidłowy wybór, wybierz 1 lub 2!")

            if current_sequence in dictionary:
                print(f"{players[current_player]} tworzy słowo '{current_sequence}' i wygrywa!")
                break

            valid_prefix = any(word.startswith(current_sequence) for word in dictionary)
            valid_suffix = any(word.endswith(current_sequence) for word in dictionary)

            if not valid_prefix and not valid_suffix:
                print(f"Sekwencja '{current_sequence}' nie może być częścią żadnego słowa!")
                print(f"{players[current_player]} przegrywa!")
                break

            if not (vs_computer and players[1 - current_player] == "Komputer"):
                while True:
                    challenge = input(f"Czy {players[1 - current_player]} chce sprawdzić sekwencję? (1 = tak, 2 = nie): ").strip()
                    if challenge == "1":
                        possible_words = [word for word in dictionary if current_sequence in word]
                        if possible_words:
                            print(f"Sekwencja '{current_sequence}' występuje w słowach: {', '.join(possible_words)}. Gra trwa dalej.")
                        else:
                            print(f"Sekwencja '{current_sequence}' nie występuje w żadnym słowie!")
                            print(f"{players[current_player]} przegrywa!")
                            break
                        break
                    elif challenge == "2":
                        break
                    else:
                        print("Nieprawidłowy wybór, wybierz 1 lub 2!")

            current_player = 1 - current_player

        while True:
            choice = input("Czy chcesz zagrać jeszcze raz? ('1 = tak' lub '2 = nie'): ").strip().lower()
            if choice == "1":
                clear_console()
                break
            elif choice == "2":
                print("Dziękujemy za grę! Do zobaczenia!")
                clear_console()
                return
            else:
                print("Nieprawidłowy wybór, wpisz 'tak' lub 'nie'.")

def main():
    while True:
        clear_console()
        print("\nMenu:")
        print("1. Start")
        print("2. Zasady")
        print("3. Wyjście")

        choice = input("Wybierz opcję (1, 2, 3): ").strip()

        if choice == "1":
            with open("slownik.txt", "r", encoding="utf-8") as file:
                dictionary = set(line.strip() for line in file if line.strip())

            clear_console()
            print("1. Gra z innym graczem")
            print("2. Gra z komputerem")
            while True:
                mode = input("Wybierz tryb (1 lub 2): ").strip()
                if mode == "1":
                    word_game(dictionary, vs_computer=False)
                    break
                elif mode == "2":
                    word_game(dictionary, vs_computer=True)
                    break
                else:
                    print("Nieprawidłowy wybór, wybierz 1 lub 2!")
        elif choice == "2":
            display_rules()
        elif choice == "3":
            clear_console()
            print("Do zobaczenia!")
            break
        else:
            print("Nieprawidłowy wybór, spróbuj ponownie.")

if __name__ == "__main__":
    main()
