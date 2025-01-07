class Seed {
  static const int Oros = 1;
  static const int Copes = 2;
  static const int Espases = 3;
  static const int Bastos = 4;

  static int getSeed(int i) {
    if (i < 0 || i > 3) {
      throw ArgumentError('Invalid seed index: $i');
    }
    return [Oros, Copes, Espases, Bastos][i];
  }

  static String getNameSeed(int i) {
    switch (i) {
      case Oros:
        return 'Oros';
      case Copes:
        return 'Copes';
      case Espases:
        return 'Espases';
      case Bastos:
        return 'Bastos';
      default:
        throw ArgumentError('Invalid seed: $i');
    }
  }
}