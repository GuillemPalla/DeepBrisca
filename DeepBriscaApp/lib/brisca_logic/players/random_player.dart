import 'dart:math';

import 'package:DeepBriscaApp/brisca_logic/card.dart';
import 'package:DeepBriscaApp/brisca_logic/players/base_player.dart';

class RandomPlayer extends BasePlayer {
  RandomPlayer() {
    name = 'RandomPlayer';
  }

  @override
  int chooseCard(List<Card> table, Card briscola, List<double> state) {
    return Random().nextInt(hand.length);
  }
}