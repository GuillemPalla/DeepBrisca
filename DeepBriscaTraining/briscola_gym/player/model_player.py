import torch  # Assuming PyTorch for the model
import numpy as np

from briscola_gym.player.base_player import BasePlayer
from pytorch_classes.DQN2 import DQN

class ModelPlayer(BasePlayer):
    def __init__(self, model_path, use_full_model=True):
        super().__init__()
        device = torch.device(
            "cuda" if torch.cuda.is_available() else
            "mps" if torch.backends.mps.is_available() else
            "cpu"
        )
        if use_full_model:
            self.model = torch.load(model_path)
        else:
            n_actions = 3
            n_observations = 54
            checkpoint = torch.load(model_path, map_location=device)
            self.model = DQN(n_observations, n_actions).to(device)
            self.model.load_state_dict(checkpoint["model_state_dict"]) if "model_state_dict" in checkpoint \
                else self.model.load_state_dict(checkpoint)
        self.model.eval()  # Set to evaluation mode

    def choose_card(self, table, briscola, state):
        # Process the state into a format your model understands
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
        with torch.no_grad():
            action_logits = self.model(state_tensor)
        action = torch.argmax(action_logits).item()  # Choose the action with the highest score
        return action
