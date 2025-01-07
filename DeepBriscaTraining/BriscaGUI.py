import os
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Pillow library for better image handling
from briscola_gym.card import Card
from briscola_gym.game import BriscolaCustomEnemyPlayer, BriscolaRandomPlayer
from briscola_gym.game_rules import select_winner
from briscola_gym.player.human_player import HumanPlayer
from briscola_gym.player.model_player import ModelPlayer
from briscola_gym.player.random_player import PseudoRandomPlayer
from briscola_gym.seed import Seed


class BriscolaGUI:
    def __init__(self, root, game_env, image_path="cards/", dev_mode=False):
        self.root = root
        self.env = game_env
        self.state, _ = self.env.reset()
        self.image_path = image_path
        self.dev_mode = dev_mode

        # Load card images
        self.card_images = self.load_card_images()
        self.reverse_card_image = self.load_reverse_card_image()

        # Set up GUI elements
        self.root.title("Briscola Game")

        # Frames
        self.deck_frame = tk.Frame(root)
        self.deck_frame.pack(side=tk.LEFT, padx=20)
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(pady=20)
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(pady=20)
        self.hand_frame = tk.Frame(root)
        self.hand_frame.pack(pady=20)
        self.opponent_frame = tk.Frame(root)
        self.opponent_frame.pack(pady=20)

        # Info labels
        self.score_label = tk.Label(self.info_frame, text="Your Score: 0 | Opponent Score: 0\n"
                                                          "Brisca Card:", font=("Helvetica", 16))
        self.score_label.pack()

        self.briscola_label = tk.Label(self.info_frame, text="Briscola:", font=("Helvetica", 16))
        self.briscola_label.pack()

        # Table cards
        self.table_label = tk.Label(self.table_frame, text="Table:", font=("Helvetica", 16))
        self.table_label.pack()

        self.table_cards = tk.Label(self.table_frame, text="[No cards on table]", font=("Helvetica", 16))
        self.table_cards.pack()

        # Player hand
        self.hand_label = tk.Label(self.hand_frame, text="Your Hand:", font=("Helvetica", 16))
        self.hand_label.pack()

        self.hand_buttons = []

        # Deck information
        self.deck_label = tk.Label(self.deck_frame, text=f"Deck Length: {len(self.env.deck.cards)}", font=("Helvetica", 16))
        self.deck_label.pack()

        self.deck_image_label = tk.Label(self.deck_frame, image=self.reverse_card_image)
        self.deck_image_label.pack()

        # Opponent hand
        self.opponent_label = tk.Label(self.opponent_frame, text="Opponent's Hand:", font=("Helvetica", 16))
        self.opponent_label.pack()

        self.opponent_hand_labels = []

        # Initialize game
        self.update_briscola()
        self.update_hand()
        self.update_table()
        self.update_deck_length()
        self.update_opponent_hand()

    def load_card_images(self):
        """Load all card images into a dictionary for quick access."""
        images = {}
        for filename in os.listdir(self.image_path):
            if filename.endswith(".png"):
                card_name = filename.split(".")[0]
                filepath = os.path.join(self.image_path, filename)
                image = Image.open(filepath).resize((120, 180))  # Increase card size
                images[card_name] = ImageTk.PhotoImage(image)
        return images

    def load_reverse_card_image(self):
        """Load the reverse card image."""
        reverse_image = Image.open(os.path.join(self.image_path, "reverse_card.png")).resize((120, 180))
        return ImageTk.PhotoImage(reverse_image)

    def get_card_image(self, card):
        """Get the image for a specific card."""
        mapped_value = card.value
        if card.value == 8:
            mapped_value = 10
        elif card.value == 9:
            mapped_value = 11
        elif card.value == 10:
            mapped_value = 12

        # Generate card name based on mapped value and seed name
        card_name = f"{mapped_value}_of_{Seed.get_name_seed(card.seed)}"
        return self.card_images.get(card_name, None)

    def update_briscola(self):
        briscola = self.env.briscola
        if briscola:
            briscola_img = self.get_card_image(briscola)
            if briscola_img:
                self.briscola_label.config(image=briscola_img)
                self.briscola_label.image = briscola_img

    def update_hand(self):
        for btn in self.hand_buttons:
            btn.destroy()

        self.hand_buttons = []

        for idx, card in enumerate(self.env.my_player.hand):
            card_img = self.get_card_image(card)
            if card_img:
                btn = tk.Button(self.hand_frame, image=card_img, command=lambda i=idx: self.play_card(i))
                btn.image = card_img
                btn.pack(side=tk.LEFT, padx=10)  # Increase padding
                self.hand_buttons.append(btn)

    def update_table(self):
        if len(self.env.table) == 0:
            self.table_cards.config(image="", text="[No cards on table]")
            self.table_cards.image = None
        else:
            table_imgs = [self.get_card_image(card) for card in self.env.table]
            if table_imgs and table_imgs[-1]:
                self.table_cards.config(image=table_imgs[-1], text="")  # Display the latest card
                self.table_cards.image = table_imgs[-1]

    def update_scores(self):
        self.score_label.config(text=f"Your Score: {self.env.my_points} | Opponent Score: {self.env.other_points} \n "
                                     f"Brisca Card:")

    def update_deck_length(self):
        self.deck_label.config(text=f"Deck Length: {len(self.env.deck.cards)}")

    def update_opponent_hand(self):
        for label in self.opponent_hand_labels:
            label.destroy()

        self.opponent_hand_labels = []

        for card in self.env.other_player.hand:
            if self.dev_mode:
                # Show actual opponent cards if in dev mode
                card_img = self.get_card_image(card)
            else:
                # Show reverse card image otherwise
                card_img = self.reverse_card_image

            label = tk.Label(self.opponent_frame, image=card_img)
            label.image = card_img
            label.pack(side=tk.LEFT, padx=5)  # Increase padding
            self.opponent_hand_labels.append(label)

    def play_card(self, card_idx):
        try:
            if self.env.turn_my_player == 0:
                show_card = True
            else:
                show_card = False
            state, reward, done, _, _ = self.env.step(card_idx)

            if show_card:
                opponent_card = self.env.discarded_cards[-1]
                opponent_card_img = self.get_card_image(opponent_card)

                if opponent_card_img:
                    self.table_cards.config(image=opponent_card_img)
                    self.table_cards.image = opponent_card_img

                    # Pause for a moment to show the opponent's card
                    self.root.update()
                    time.sleep(1)

            self.update_table()
            self.update_hand()
            self.update_scores()
            self.update_deck_length()
            self.update_opponent_hand()

            if done:
                self.end_game()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def end_game(self):
        if self.env.my_points > self.env.other_points:
            messagebox.showinfo("Game Over", "You win!")
        elif self.env.my_points < self.env.other_points:
            messagebox.showinfo("Game Over", "You lose!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")

        self.root.quit()


if __name__ == "__main__":
    trained_model_path = "models3/dqn_greedy-100_000-800KMem-1e_4LR-128BS-NNv2.pth"
    game_env = BriscolaCustomEnemyPlayer(ModelPlayer(trained_model_path, False))
    #game_env = BriscolaCustomEnemyPlayer(PseudoRandomPlayer())

    dev_mode = True

    # Start the GUI
    root = tk.Tk()
    app = BriscolaGUI(root, game_env, dev_mode=dev_mode)
    root.mainloop()
