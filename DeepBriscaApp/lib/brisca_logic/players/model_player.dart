import 'package:DeepBriscaApp/brisca_logic/card.dart';
import 'package:DeepBriscaApp/brisca_logic/players/base_player.dart';
import 'package:DeepBriscaApp/brisca_logic/values.dart';
import 'package:tflite_flutter/tflite_flutter.dart';

class ModelPlayer extends BasePlayer {
  late Interpreter interpreter;
  bool _isModelLoaded = false;
  PlayerDifficulty modelDifficulty;

  ModelPlayer(this.modelDifficulty) {
    initializeModel();
  }

  Future<void> initializeModel() async {
    try {
      //await Future.delayed(const Duration(seconds: 15));
      interpreter = await Interpreter.fromAsset(playerInfo[modelDifficulty]?['model_path'] ?? '',);
      _isModelLoaded = true;
    } catch (e) {
      throw Exception("Error loading model: $e");
    }
  }

  @override
  int chooseCard(List<Card> table, Card briscola, List<double> state) {
    if (!_isModelLoaded) {
      throw Exception("Model is not loaded yet. Please wait.");
    }

    // Preprocess the state to the required tensor shape
    List<List<double>> input = [state]; // Add batch dimension
    var output = List.filled(3, 0.0).reshape([1, 3]); // Assuming 3 actions

    // Run inference
    interpreter.run(input, output);

    // Process output to get the action
    List<double> actionLogits = output[0];
    int action = actionLogits.indexOf(actionLogits.reduce((a, b) => a > b ? a : b));
    return action;
  }
}
