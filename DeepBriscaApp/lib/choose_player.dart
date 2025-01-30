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
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      appBar: AppBar(
        title: RichText(
          text: const TextSpan(
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: Colors.black,
            ),
            children: <TextSpan>[
              TextSpan(text: 'DeepBrisca', style: TextStyle(fontSize: 30)),
              TextSpan(
                text: 'v1',
                style: TextStyle(
                  fontSize: 20,
                  color: Colors.grey,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        elevation: 0,
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                'SELECT OPPONENT',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 22, 
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(height: screenHeight * 0.03),
              Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: _buildPlayerOptions(),
              ),
              SizedBox(height: screenHeight * 0.04),
              _buildAdminModeToggle(),
              SizedBox(height: screenHeight * 0.04),
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
                  padding: EdgeInsets.symmetric(
                    horizontal: screenWidth * 0.2,
                    vertical: screenHeight * 0.02,
                  ),
                  shape: const RoundedRectangleBorder(
                    borderRadius: BorderRadius.horizontal(),
                  ),
                  elevation: 0,
                ),
                child: const Text('Start Game'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  List<Widget> _buildPlayerOptions() {
    return PlayerDifficulty.values.map((type) {
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 8.0),
        child: _buildPlayerOption(type),
      );
    }).toList();
  }

  Widget _buildPlayerOption(PlayerDifficulty type) {
    return Row(
      mainAxisSize: MainAxisSize.min,
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
                title: Text(
                  playerInfo[type]?['name'] ?? '',
                  style: const TextStyle(color: Colors.black),
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
    );
  }

  Widget _buildAdminModeToggle() {
    return Row(
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
                title: const Text(
                  'Admin Mode',
                  style: TextStyle(color: Colors.black),
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
    );
  }
}
