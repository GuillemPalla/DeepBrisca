import 'package:DeepBriscaApp/brisca_logic/card.dart';

abstract class BasePlayer {
  List<Card> hand = [];
  String? name;
  int score = 0;

  void resetPlayer() {
    hand.clear();
    score = 0;
  }

  int chooseCard(List<Card> table, Card briscola, List<double> state);

  Card discardCard(List<Card> table, Card briscola, List<double> state) {
    int i = chooseCard(table, briscola, state);
    if(hand.length < i+1){
      i = hand.length-1;
    }
    return hand.removeAt(i);
  }

  void addToHand(Card card) {
    hand.add(card);
  }

void addScore(int points) {
    score += points;
  }

  void onEnemyDiscard(Card card) {}

  bool isEmptyHand() => hand.isEmpty;

  void notifyTurnWinner(int points) {}

  void notifyGameWinner(String name) {}
}