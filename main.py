import tkinter as tk
from tkinter import messagebox
import random

class WordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Gra Słowna")

        self.dictionary = set()
        self.load_dictionary()

        self.players = []
        self.current_player = 0
        self.current_sequence = ""
        self.vs_computer = False
        self.game_over = False

        self.setup_menu()

    def load_dictionary(self):
        try:
            with open("slownik.txt", "r", encoding="utf-8") as file:
                self.dictionary = set(line.strip().lower() for line in file if line.strip())
        except FileNotFoundError:
            messagebox.showerror("Błąd", "Nie znaleziono pliku 'slownik.txt'.")
            self.root.destroy()

    def setup_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Menu Główne", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Start", command=self.setup_game_mode, width=20).pack(pady=5)
        tk.Button(self.root, text="Zasady", command=self.show_rules, width=20).pack(pady=5)
        tk.Button(self.root, text="Wyjście", command=self.root.destroy, width=20).pack(pady=5)

    def show_rules(self):
        self.clear_window()

        rules_text = (
            "Zasady gry:\n"
            "1. Gra rozpoczyna się od pustej sekwencji liter.\n"
            "2. W każdej turze gracz dodaje jedną literę na początek lub koniec sekwencji.\n"
            "3. Celem jest uformowanie słowa znajdującego się w słowniku.\n"
            "4. Jeśli sekwencja nie może być częścią żadnego słowa, gracz przegrywa.\n"
            "5. Drugi gracz może rzucić wyzwanie, jeśli uważa, że sekwencja nie prowadzi do poprawnego słowa.\n"
            "6. Gra kończy się, gdy ktoś uformuje słowo lub popełni błąd.\n"
        )

        tk.Label(self.root, text="Zasady Gry", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=rules_text, font=("Arial", 12), justify="left").pack(padx=10, pady=10)

        tk.Button(self.root, text="Powrót", command=self.setup_menu, width=20).pack(pady=10)

    def setup_game_mode(self):
        self.clear_window()

        tk.Label(self.root, text="Wybierz tryb gry", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Gra z graczem", command=lambda: self.setup_player_names(False), width=20).pack(pady=5)
        tk.Button(self.root, text="Gra z komputerem", command=lambda: self.setup_player_names(True), width=20).pack(pady=5)
        tk.Button(self.root, text="Powrót", command=self.setup_menu, width=20).pack(pady=5)

    def setup_player_names(self, vs_computer):
        self.clear_window()

        self.vs_computer = vs_computer
        tk.Label(self.root, text="Podaj imiona graczy", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Gracz 1:").pack()
        self.player1_entry = tk.Entry(self.root)
        self.player1_entry.pack(pady=5)

        if not vs_computer:
            tk.Label(self.root, text="Gracz 2:").pack()
            self.player2_entry = tk.Entry(self.root)
            self.player2_entry.pack(pady=5)

        tk.Button(self.root, text="Start", command=self.start_game, width=20).pack(pady=10)
        tk.Button(self.root, text="Powrót", command=self.setup_game_mode, width=20).pack(pady=5)

    def start_game(self):
        player1 = self.player1_entry.get().strip()
        player2 = "Komputer" if self.vs_computer else self.player2_entry.get().strip()

        if len(player1) > 12 or len(player2) > 12:
            messagebox.showwarning("Błąd", "Imiona nie mogą mieć więcej niż 12 znaków!")
            return

        if not player1 or (not self.vs_computer and not player2):
            messagebox.showwarning("Błąd", "Wprowadź imiona wszystkich graczy!")
            return

        self.players = [player1, player2]
        self.current_player = random.randint(0, 1)
        self.current_sequence = ""
        self.game_over = False

        self.setup_game_interface()

        if self.vs_computer and self.players[self.current_player] == "Komputer":
            self.root.after(1000, self.computer_turn)

    def setup_game_interface(self):
        self.clear_window()

        tk.Label(self.root, text=f"Gra Słowna", font=("Arial", 16)).pack(pady=10)

        self.player_turn_label = tk.Label(self.root, text=f"Teraz gra {self.players[self.current_player]}", font=("Arial", 12))
        self.player_turn_label.pack(pady=5)

        self.sequence_label = tk.Label(self.root, text=f"Aktualna sekwencja: '{self.current_sequence}'", font=("Arial", 12))
        self.sequence_label.pack(pady=5)

        tk.Label(self.root, text="Dodaj literę:").pack()
        self.move_entry = tk.Entry(self.root)
        self.move_entry.pack(pady=5)

        tk.Button(self.root, text="Dodaj na Początek", command=lambda: self.player_turn("1"), width=20).pack(pady=5)
        tk.Button(self.root, text="Dodaj na Koniec", command=lambda: self.player_turn("2"), width=20).pack(pady=5)

        tk.Button(self.root, text="Sprawdź sekwencję", command=self.check_sequence, width=20).pack(pady=5)
        tk.Button(self.root, text="Powrót do menu", command=self.setup_menu, width=20).pack(pady=10)

    def player_turn(self, position):
        if self.game_over:
            return

        move = self.move_entry.get().strip().lower()
        if len(move) != 1 or not move.isalpha():
            messagebox.showwarning("Błąd", "Wprowadź dokładnie jedną literę!")
            return

        if position == "1":
            self.current_sequence = move + self.current_sequence
        elif position == "2":
            self.current_sequence = self.current_sequence + move

        self.sequence_label.config(text=f"Aktualna sekwencja: '{self.current_sequence}'")
        self.move_entry.delete(0, tk.END)

        if self.current_sequence in self.dictionary:
            self.end_game(f"{self.players[self.current_player]} tworzy słowo '{self.current_sequence}' i wygrywa!")
            return

        valid_prefix = any(word.startswith(self.current_sequence) for word in self.dictionary)
        valid_suffix = any(word.endswith(self.current_sequence) for word in self.dictionary)

        if not valid_prefix and not valid_suffix:
            self.end_game(f"{self.players[self.current_player]} tworzy niepoprawną sekwencję '{self.current_sequence}' i przegrywa!")
            return

        self.current_player = 1 - self.current_player
        self.player_turn_label.config(text=f"Teraz gra {self.players[self.current_player]}")

        if self.vs_computer and self.players[self.current_player] == "Komputer":
            self.root.after(1000, self.computer_turn)

    def computer_turn(self):
        if self.game_over:
            return

        potential_moves = []
        for letter in "abcdefghijklmnopqrstuvwxyz":
            for new_seq in [letter + self.current_sequence, self.current_sequence + letter]:
                valid_prefix = any(word.startswith(new_seq) for word in self.dictionary)
                valid_suffix = any(word.endswith(new_seq) for word in self.dictionary)
                if valid_prefix or valid_suffix:
                    potential_moves.append((new_seq, letter))

        if potential_moves:
            safe_moves = [move for move in potential_moves if move[0] not in self.dictionary]
            if safe_moves:
                chosen_move = random.choice(safe_moves)
            else:
                chosen_move = random.choice(potential_moves)

            self.current_sequence = chosen_move[0]
            self.sequence_label.config(text=f"Aktualna sekwencja: '{self.current_sequence}'")

            messagebox.showinfo("Ruch Komputera", f"Komputer dodał literę: '{chosen_move[1]}'")

            if self.current_sequence in self.dictionary:
                self.end_game(f"Komputer tworzy słowo '{self.current_sequence}' i wygrywa!")
                return
        else:
            self.end_game("Komputer nie może dodać litery i przegrywa!")
            return

        self.current_player = 1 - self.current_player
        self.player_turn_label.config(text=f"Teraz gra {self.players[self.current_player]}")

    def check_sequence(self):
        if not self.current_sequence:
            messagebox.showwarning("Błąd", "Musisz dodać przynajmniej jedną literę, aby sprawdzić sekwencję.")
            return

        possible_words = [word for word in self.dictionary if self.current_sequence in word]
        if possible_words:
            messagebox.showinfo("Sekwencja", f"Sekwencja '{self.current_sequence}' występuje w słowach: {', '.join(possible_words)}.")
        else:
            messagebox.showinfo("Sekwencja", f"Sekwencja '{self.current_sequence}' nie występuje w żadnym słowie.")

    def end_game(self, message):
        self.game_over = True
        self.clear_window()
        messagebox.showinfo("Koniec gry", message)

        tk.Button(self.root, text="Powrót do menu", command=self.setup_menu, width=20).pack(pady=5)
        tk.Button(self.root, text="Nowa gra", command=self.setup_game_mode, width=20).pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = WordGame(root)
    root.mainloop()
