import 'package:DeepBriscaApp/brisca_game_page.dart';
import 'package:DeepBriscaApp/brisca_logic/values.dart';
import 'package:flutter/material.dart';

class ChoosePlayerScreen extends StatefulWidget {
  const ChoosePlayerScreen({super.key});

  @override
  State<ChoosePlayerScreen> createState() => _ChoosePlayerScreenState();
}

class _ChoosePlayerScreenState extends State<ChoosePlayerScreen> {
  PlayerDifficulty selectedPlayerType = PlayerDifficulty.random;
  bool adminMode = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Choose Player'),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        elevation: 0,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              'Select your opponent:',
              style: TextStyle(
                fontSize: 18,
                color: Colors.black,
              ),
            ),
            const SizedBox(height: 20),
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _buildPlayerOption(
                  PlayerDifficulty.random
                ),
                const SizedBox(height: 20),
                _buildPlayerOption(
                  PlayerDifficulty.modelEasy
                ),
                const SizedBox(height: 20),
                _buildPlayerOption(
                  PlayerDifficulty.modelMedium
                ),
                const SizedBox(height: 20),
                _buildPlayerOption(
                  PlayerDifficulty.modelHard
                ),
              ],
            ),
            const SizedBox(height: 30),
            // Admin Mode Toggle with Info
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Switch(
                  value: adminMode,
                  onChanged: (value) {
                    setState(() => adminMode = value);
                  },
                  activeColor: Colors.black,
                  inactiveTrackColor: Colors.white,
                ),
                const Text(
                  'Admin Mode',
                  style: TextStyle(color: Colors.black),
                ),
                IconButton(
                  icon: const Icon(Icons.info_outline, color: Colors.grey),
                  onPressed: () {
                    showDialog(
                      context: context,
                      builder: (context) => AlertDialog(
                        backgroundColor: Colors.white,
                        title: const Center(
                          child: Text(
                            'Admin Mode',
                            style: TextStyle(color: Colors.black),
                          ),
                        ),
                        content: const Text(
                          adminModeExplanation,
                          style: TextStyle(color: Colors.grey),
                        ),
                        actions: [
                          TextButton(
                            onPressed: () => Navigator.pop(context),
                            child: const Text(
                              'Close',
                              style: TextStyle(color: Colors.black),
                            ),
                          ),
                        ],
                      ),
                    );
                  },
                ),
              ],
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => BriscaGamePage(
                    playerDifficulty: selectedPlayerType,
                    adminMode: adminMode,
                  ),
                ),
              ),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.black,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 15),
                shape: const RoundedRectangleBorder(
                  borderRadius: BorderRadius.zero,
                ),
                elevation: 0,
              ),
              child: const Text('Start Game'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPlayerOption(PlayerDifficulty type) {
    return Column(
      children: [
        Row(
          children: [
            Radio<PlayerDifficulty>(
              value: type,
              groupValue: selectedPlayerType,
              onChanged: (PlayerDifficulty? value) {
                setState(() => selectedPlayerType = value!);
              },
              activeColor: Colors.black,
            ),
            Text(
              playerInfo[type]?['name'] ?? '',
              style: const TextStyle(color: Colors.black),
            ),
            IconButton(
              icon: const Icon(Icons.info_outline, color: Colors.grey),
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    backgroundColor: Colors.white,
                    title: Column(
                      children: [
                        Text(
                          playerInfo[type]?['name'] ?? '',
                          style: const TextStyle(color: Colors.black),
                        ),
                        Text(
                          playerInfo[type]?['random_winrate'] != null && (playerInfo[type]?['random_winrate'] as String).isNotEmpty
                              ? '${playerInfo[type]?['random_winrate']} winrate vs Random Player'
                              : '',
                          textAlign: TextAlign.left,
                          style: const TextStyle(
                            color: Colors.grey,
                            fontSize: 15,
                          ),
                        ),
                      ],
                    ),
                    content: Text(
                      playerInfo[type]?['info'] ?? '',
                      style: const TextStyle(color: Colors.grey),
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text(
                          'Close',
                          style: TextStyle(color: Colors.black),
                        ),
                      ),
                    ],
                  ),
                );
              },
            ),
          ],
        ),
      ],
    );
  }
}
