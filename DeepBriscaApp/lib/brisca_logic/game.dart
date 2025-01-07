import 'package:DeepBriscaApp/brisca_logic/card.dart';
import 'package:DeepBriscaApp/brisca_logic/game_rules.dart';
import 'package:DeepBriscaApp/brisca_logic/players/base_player.dart';
import 'package:DeepBriscaApp/brisca_logic/constants.dart';

import 'dart:math';

import 'package:DeepBriscaApp/brisca_logic/players/human_player.dart';

class LaBriscaGame {
  Deck deck = Deck();
  BasePlayer myPlayer = HumanPlayer();
  BasePlayer otherPlayer;
  Card briscaCard = Card(0,0);
  int turn = 0;
  List<Card> discardedCards = [];
  List<Card> table = [];
  bool turnMyPlayer = true;

  LaBriscaGame(this.otherPlayer);

  void startGame() {
    turn = 0;
    myPlayer.resetPlayer();
    otherPlayer.resetPlayer();
    deck = Deck();
    discardedCards = [];
    table = [];

    turnMyPlayer = Random().nextBool();

    briscaCard = deck.draw();

    deck.cards.add(briscaCard);

    // Deal cards to players
    for (int i = 0; i < 3; i++) {
      myPlayer.addToHand(deck.draw());
      otherPlayer.addToHand(deck.draw());
    }

    if(!turnMyPlayer){
      table.add(otherPlayer.discardCard(table, briscaCard, modelState()));
    }
  }

  bool playRound(int action) {
    if(action<0 || action>myPlayer.hand.length-1){
      throw Exception('Invalid action');
    }

    turn+=1;
    table.add(myPlayer.hand.removeAt(action));

    if(turnMyPlayer){
      table.add(otherPlayer.discardCard(table, briscaCard, modelState()));
    }

    bool winner = selectWinner(table, briscaCard);
    stateUpdateAfterWinner(winner);
    drawPhase();

    if(!turnMyPlayer && !isFinish()){
      table.add(otherPlayer.discardCard(table, briscaCard, modelState()));
    }

    return isFinish();
  }

  void stateUpdateAfterWinner(bool winner){
    int gainedPoints = table
      .map((c) => valuesPoints[c.value])
      .fold(0, (sum, points) => sum + points!);

    discardedCards.add(table[0]);
    discardedCards.add(table[1]);

    if(winner == turnMyPlayer){
      myPlayer.addScore(gainedPoints);
      turnMyPlayer = true;
    }
    else{
      otherPlayer.addScore(gainedPoints);
      turnMyPlayer = false;
    }

    table = [];
  }

  void drawPhase(){
    if(!deck.isEmpty()){
      Card c1 = deck.draw();
      Card c2 = deck.draw();

      if (turnMyPlayer){
        myPlayer.addToHand(c1);
        otherPlayer.addToHand(c2);
      }
      else{
        myPlayer.addToHand(c2);
        otherPlayer.addToHand(c1);
      }
    }
  }

  List<double> modelState() {
    List<double> state = [
      otherPlayer.score.toDouble(),
      myPlayer.score.toDouble(),
      // ignore: unnecessary_null_comparison
      deck != null ? deck.cards.length.toDouble() : 0.0,
      turnMyPlayer ? 1.0 : 0.0,
    ];

    state.addAll([briscaCard.value.toDouble(), briscaCard.seed.toDouble()]);

    const int maxHandSize = 3;
    const int maxTableSize = 1;

    List<double> padCards(List<Card> cards, int maxSize) {
      List<double> padded = List.generate(maxSize * 2, (_) => 0.0);
      for (int i = 0; i < cards.length && i < maxSize; i++) {
        padded[i * 2] = cards[i].value.toDouble();
        padded[i * 2 + 1] = cards[i].seed.toDouble();
      }
      return padded;
    }

    state.addAll(padCards(table, maxTableSize));
    state.addAll(padCards(otherPlayer.hand, maxHandSize));

    const int totalCards = 40;
    List<double> discardedVector = List.filled(totalCards, 0.0);

    for (var card in discardedCards) {
      // Adjust card indexing for values 1-10 and seeds 1-4
      int cardIndex = (card.value - 1) + ((card.seed - 1) * 10);
      discardedVector[cardIndex] = 1.0;
    }

    state.addAll(discardedVector);

    // // Pad the state to match the observation space
    // const int observationSpaceSize = 100; // Adjust based on your actual observation space
    // if (state.length < observationSpaceSize) {
    //   state.addAll(List.filled(observationSpaceSize - state.length, 0.0));
    // }

    return state;
  }

  bool isFinish(){
    // return (myPlayer.score>60 || otherPlayer.score>60 || (deck.isEmpty() && myPlayer.hand.isEmpty && otherPlayer.hand.isEmpty));
    return (deck.isEmpty() && myPlayer.hand.isEmpty && otherPlayer.hand.isEmpty);
  }
}