import 'package:DeepBriscaApp/brisca_logic/card.dart';
import 'package:DeepBriscaApp/brisca_logic/players/base_player.dart';

class HumanPlayer extends BasePlayer {
  @override
  int chooseCard(List<Card> table, Card briscola, dynamic state) {
    // Return -1 to indicate manual input required
    return -1;
  }
}