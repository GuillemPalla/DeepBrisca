enum PlayerDifficulty { random, modelEasy, modelMedium, modelHard }

const playerInfo = {
  PlayerDifficulty.random: {
    'name': 'Random Player',
    'info': 'Makes completely random decisions.',
    'model_path': '',
  },
  PlayerDifficulty.modelEasy: {
    'name': 'Easy Model Player',
    'random_winrate': '64.35%',
    'info': 'This AI agent used a DQN (Deep Q-Network) reinforcement learning algorithm with a small neural network '
            '(23,939 parameters). It has learned using different techniques playing 50,000 training games.',
    'model_path': 'assets/models/dqn_greedy-50_000-800KMem-1e_4LR-128BS_float32.tflite',
  },
  PlayerDifficulty.modelMedium: {
    'name': 'Medium Model Player',
    'random_winrate': '78.97%',
    'info': 'This AI agent used a DQN (Deep Q-Network) reinforcement learning algorithm with a larger neural network '
            '(40,451 parameters). It has learned using different techniques playing 100,000 training games.',
    'model_path': 'assets/models/dqn_greedy-100_000-800KMem-1e_4LR-128BS-NNv2_float32.tflite',
  },
  PlayerDifficulty.modelHard: {
    'name': 'Hard Model Player',
    'random_winrate': '88.10%',
    'info': 'This AI agent used a DQN (Deep Q-Network) reinforcement learning algorithm with a larger neural network '
            '(40,451 parameters). It has learned using different techniques playing 600,000 training games.',
    'model_path': 'assets/models/dqn_greedy_model-600_000-800KMem-1e_4LR-128BS-NNv2_float32.tflite',
  },
};

const String adminModeExplanation = 'Admin Mode allows you to see the cards of the opponent player. '
  'This is useful for debugging or learning strategies but removes the challenge of the game.';