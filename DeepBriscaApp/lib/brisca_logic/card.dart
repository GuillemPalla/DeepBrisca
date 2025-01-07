import 'dart:math';

import 'package:DeepBriscaApp/brisca_logic/constants.dart';
import 'package:DeepBriscaApp/brisca_logic/seed.dart';

class Card {
  final int value;
  final int seed;
  final int points;
  final int id;

  Card(this.value, this.seed)
      : points = valuesPoints[value] ?? 0,
        id = seed * 10 + value {
    if (value < 0 || value > 10) {
      throw ArgumentError('Invalid card value: $value');
    }
    if (seed < 0 || seed > 4) {
      throw ArgumentError('Invalid card seed: $seed');
    }
  }

  int getValueCard(){
    int mappedValue = value;
    
    if (value == 8){
      mappedValue = 10;
    }
    else if (value == 9){
      mappedValue = 11;
    }
    else if (value == 10){
      mappedValue = 12;
    }

    return mappedValue;
  }

  List<int> vector() => [value, seed, points];
}

class Deck {
  List<Card> cards = [];

  Deck() {
    cards = allCards();
    cards.shuffle(Random());
  }

  static List<Card> allCards() {
    return List.generate(40, (i) => Card(i % 10 + 1, Seed.getSeed(i ~/ 10)));
  }

  Card draw() {
    if (cards.isEmpty) {
      throw StateError('Deck is empty');
    }
    return cards.removeAt(0);
  }

  bool isEmpty() => cards.isEmpty;
}