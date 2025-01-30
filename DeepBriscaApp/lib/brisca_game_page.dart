import 'package:DeepBriscaApp/brisca_logic/game.dart';
import 'package:DeepBriscaApp/brisca_logic/players/base_player.dart';
import 'package:DeepBriscaApp/brisca_logic/players/model_player.dart';
import 'package:DeepBriscaApp/brisca_logic/players/random_player.dart';
import 'package:DeepBriscaApp/brisca_logic/seed.dart';
import 'package:DeepBriscaApp/brisca_logic/values.dart';
import 'package:flutter/material.dart';

class BriscaGamePage extends StatefulWidget {
  final PlayerDifficulty playerDifficulty;
  final bool adminMode;

  const BriscaGamePage({super.key, required this.playerDifficulty, required this.adminMode});

  @override
  State<BriscaGamePage> createState() => _BriscaGamePageState();
}

class _BriscaGamePageState extends State<BriscaGamePage> with TickerProviderStateMixin {
  late LaBriscaGame game;
  late AnimationController animationControllerPlayer;
  late AnimationController animationControllerOpponent;
  late Animation<Offset> opponentCardAnimation;
  late Animation<Offset> playerCardAnimation;

  String yourScore = "0";
  String opponentScore = "0";
  String briscolaCard = "";
  List<String> playerHand = [];
  List<String> opponentHand = [];
  String? tableCard;
  int deckLength = 0;
  String? opponentPlayedCard;
  String? playerPlayedCard;

  bool _isInitialized = false;

  @override
  void initState() {
    super.initState();
    initializeGame();
    animationControllerPlayer = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );
    animationControllerOpponent = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );
    opponentCardAnimation = Tween<Offset>(
      begin: const Offset(0, -2),
      end: const Offset(0, 0),
    ).animate(CurvedAnimation(
      parent: animationControllerOpponent,
      curve: Curves.easeOut,
    ));
    playerCardAnimation = Tween<Offset>(
      begin: const Offset(0, 2),
      end: const Offset(0, 0),
    ).animate(CurvedAnimation(
      parent: animationControllerPlayer,
      curve: Curves.easeOut,
    ));
  }

  Future<void> initializeGame() async {
    setState(() {
      game = LaBriscaGame(RandomPlayer()); // Placeholder until initialization
    });

    BasePlayer player;
    if (widget.playerDifficulty == PlayerDifficulty.random) {
      player = RandomPlayer();
    } else {
      player = ModelPlayer(widget.playerDifficulty);
      await (player as ModelPlayer).initializeModel();
    }

    setState(() {
      game = LaBriscaGame(player);
      game.startGame();
      updateUI();
      updateTable();
      _isInitialized = true;
    });
  }

  void updateUI() {
    setState(() {
      yourScore = game.myPlayer.score.toString();
      opponentScore = game.otherPlayer.score.toString();
      briscolaCard = "${game.briscaCard.getValueCard()}_of_${Seed.getNameSeed(game.briscaCard.seed)}";
      deckLength = game.deck.cards.length;
      playerHand = game.myPlayer.hand
          .map((card) => "${card.getValueCard()}_of_${Seed.getNameSeed(card.seed)}")
          .toList();
      if(widget.adminMode){
        opponentHand = game.otherPlayer.hand
          .map((card) => "${card.getValueCard()}_of_${Seed.getNameSeed(card.seed)}")
          .toList();
      }
      else{
        opponentHand = List.generate(game.otherPlayer.hand.length, (index) => "reverse_card");
      }
    });
  }

  void updateTable() {
    setState(() {
      tableCard = game.table.isNotEmpty
          ? "${game.table[0].getValueCard()}_of_${Seed.getNameSeed(game.table[0].seed)}"
          : null;
    });
  }

  void playCard(int cardIndex) {
    if (cardIndex < 0 || cardIndex >= playerHand.length) return; // Prevent out-of-range errors

    setState(() {
      playerPlayedCard = playerHand[cardIndex];
      playerHand.removeAt(cardIndex);
    });

    animationControllerPlayer.reset();
    animationControllerPlayer.forward().then((_) {
      bool isMyPlayerFirst = game.turnMyPlayer;
      bool isFinished = game.playRound(cardIndex);

      setState(() {
        if (isMyPlayerFirst) {
          opponentPlayedCard = game.discardedCards.isNotEmpty
              ? "${game.discardedCards.last.getValueCard()}_of_${Seed.getNameSeed(game.discardedCards.last.seed)}"
              : null;
        }
      });

      animationControllerOpponent.reset();
      animationControllerOpponent.forward().then((_) {
        updateUI();
        if (!isFinished && !game.turnMyPlayer) {
          setState(() {
            tableCard = null;
            playerPlayedCard = null;
            opponentPlayedCard = game.table.isNotEmpty
                ? "${game.table.last.getValueCard()}_of_${Seed.getNameSeed(game.table.last.seed)}"
                : null;
          });
          animationControllerOpponent.reset();
          animationControllerOpponent.forward().then((_) {
            setState(() {
              playerPlayedCard = null;
              opponentPlayedCard = null;
            });
            updateTable();
            if (isFinished) {
              showGameOverDialog();
            }
          });
        } else {
          setState(() {
            playerPlayedCard = null;
            opponentPlayedCard = null;
          });
          updateTable();
          if (isFinished) {
            showGameOverDialog();
          }
        }
      });
    });
  }

  void showGameOverDialog() {
    String winner = game.myPlayer.score > game.otherPlayer.score ? "You" : "Opponent";
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: Colors.white,
        title: const Text("Game Over", style: TextStyle(color: Colors.black)),
        content: Text(
          "$winner won the game!",
          style: const TextStyle(color: Colors.black, fontSize: 16),
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              initializeGame();
            },
            child: const Text(
              "Play Again",
              style: TextStyle(color: Colors.black),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (!_isInitialized) {
      // Show the loading screen only at the start
      return Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.white,
          elevation: 0.0,
          title: const Text(
            'DeepBrisca',
            style: TextStyle(color: Colors.black),
          ),
        ),
        body: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CircularProgressIndicator(),
              SizedBox(height: 20),
              Text("Loading Game...", style: TextStyle(color: Colors.black, fontSize: 18)),
            ],
          ),
        ),
      );
    }

    // Show the game content once initialized
    return PopScope(
      canPop: false,
      onPopInvoked: (didPop) {
        if (didPop) {
          return;
        }
        showExitConfirmationDialog(context);
      },
      child: Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.white,
          elevation: 0.0,
          leading: IconButton(
            icon: const Icon(Icons.exit_to_app, color: Colors.black),
            onPressed: () => showExitConfirmationDialog(context),
          ),
          title: Row(
            children: [
              RichText(
                text: const TextSpan(
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                  children: <TextSpan>[
                    TextSpan(text: 'DeepBrisca', style: TextStyle(fontSize: 23)),
                    TextSpan(
                      text: 'v1',
                      style: TextStyle(
                        fontSize: 15,
                        color: Colors.grey,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 10.0),
              Text(
                playerInfo[widget.playerDifficulty]?['name'] ?? '',
                style: const TextStyle(
                  color: Colors.black,
                  fontSize: 14,
                  fontWeight: FontWeight.w300,
                ),
              ),
            ],
          ),
        ),
        body: buildGameContent(context), // Game UI content
      ),
    );
  }



  Container buildGameContent(BuildContext context) {
    return Container(
      color: Colors.white,
      child: Stack(
        children: [
          // Deck Pile and Brisca
          Positioned(
            left: 20,
            top: MediaQuery.of(context).size.height * 0.2,
            child: Column(
              children: [
                Container(
                  width: 100.0,
                  height: 165.0,
                  padding: const EdgeInsets.all(8.0),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: const BorderRadius.horizontal(),
                    border: Border.all(color: Colors.black),
                  ),
                  child: Column(
                    children: [
                      const Text(
                        "TRUMP",
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 15,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 5),
                      briscolaCard.isNotEmpty
                        ? Image.asset(
                            'assets/cards/$briscolaCard.png',
                            width: 80,
                            height: 120,
                          )
                        : const SizedBox.shrink(),
                    ],
                  ),
                ),
                const SizedBox(height: 10),
                Container(
                  width: 100.0,
                  height: 165.0,
                  padding: const EdgeInsets.all(8.0),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: const BorderRadius.horizontal(),
                    border: Border.all(color: Colors.black),
                  ),
                  child: Column(
                    children: [
                      const Text(
                        "DECK",
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 15,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 5),
                      Stack(
                        alignment: Alignment.center,
                        children: [
                          Image.asset(
                            'assets/cards/reverse_card.png',
                            width: 80,
                            height: 120,
                          ),
                          Text(
                            deckLength.toString(),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                              shadows: <Shadow>[
                                Shadow(
                                  offset: Offset(2.0, 2.0),
                                  blurRadius: 3.0,
                                  color: Color.fromARGB(255, 0, 0, 0),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Scores
          Positioned(
            right: 20,
            top: MediaQuery.of(context).size.height * 0.35,
            child: Container(
              width: 70.0,
              height: 100.0,
              padding: const EdgeInsets.all(8.0),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: const BorderRadius.horizontal(),
                border: Border.all(color: Colors.black),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    "SCORE",
                    style: TextStyle(
                      color: Colors.black,
                      fontSize: 15,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        opponentScore,
                        style: const TextStyle(
                          color: Colors.black,
                          fontSize: 20,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      Text(
                        yourScore,
                        style: const TextStyle(
                          color: Colors.black,
                          fontSize: 20,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),

          // Main Content Column
          Column(
            children: [
              // Opponent's Cards
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 10.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: opponentHand
                      .map((card) => Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 5.0),
                            child: Image.asset('assets/cards/$card.png', width: 80, height: 120),
                          ))
                      .toList(),
                ),
              ),

              // Table Card with Animation
              Expanded(
                child: Center(
                  child: Stack(
                    alignment: Alignment.center,
                    children: [
                      if (tableCard != null)
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 5.0),
                          child: Image.asset('assets/cards/$tableCard.png', width: 110, height: 150),
                        ),
                      if (playerPlayedCard != null)
                        SlideTransition(
                          position: playerCardAnimation,
                          child: Image.asset(
                            'assets/cards/$playerPlayedCard.png',
                            width: 110,
                            height: 150,
                          ),
                        ),
                      if (opponentPlayedCard != null)
                        SlideTransition(
                          position: opponentCardAnimation,
                          child: Image.asset(
                            'assets/cards/$opponentPlayedCard.png',
                            width: 110,
                            height: 150,
                          ),
                        ),
                    ],
                  ),
                ),
              ),

              // Player's Cards
              AbsorbPointer(
                absorbing: animationControllerPlayer.isAnimating || animationControllerOpponent.isAnimating,
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 10.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: playerHand
                        .asMap()
                        .entries
                        .map((entry) => Padding(
                              padding: const EdgeInsets.symmetric(horizontal: 5.0),
                              child: GestureDetector(
                                onTap: () => playCard(entry.key),
                                child: Image.asset('assets/cards/${entry.value}.png', width: 110, height: 150),
                              ),
                            ))
                        .toList(),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  void showExitConfirmationDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: Colors.white,
        title: const Text(
          'Exit Game',
          style: TextStyle(color: Colors.black, fontSize: 16),
        ),
        content: const Text(
          'Are you sure you want to exit the game?',
          style: TextStyle(color: Colors.black, fontSize: 14),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text(
              'Cancel',
              style: TextStyle(color: Colors.black),
            ),
          ),
          TextButton(
            onPressed: () => Navigator.of(context).popUntil((route) => route.isFirst),
            child: const Text(
              'Exit',
              style: TextStyle(color: Colors.black),
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    animationControllerPlayer.dispose();
    animationControllerOpponent.dispose();
    super.dispose();
  }
}