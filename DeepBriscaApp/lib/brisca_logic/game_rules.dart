import 'package:DeepBriscaApp/brisca_logic/card.dart';
import 'package:DeepBriscaApp/brisca_logic/constants.dart';

bool selectWinner(List<Card> table, Card briscola) {
  final first = table[0];
  final second = table[1];
  final firstPoints = valuesPoints[first.value] ?? 0;
  final secondPoints = valuesPoints[second.value] ?? 0;
  final secondBriscola = second.seed == briscola.seed;

  if (second.seed == first.seed) {
    if (firstPoints == 0 && secondPoints == 0) {
      return second.value < first.value;
    } else {
      return secondPoints < firstPoints;
    }
  } else if (secondBriscola) {
    return false;
  } else {
    return true;
  }
}