import 'package:DeepBriscaApp/home.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';


class DeepBrisca extends StatelessWidget {
  const DeepBrisca({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'DeepBrisca',
      theme: ThemeData(
        // Minimalistic black, white, and grey theme
        scaffoldBackgroundColor: Colors.white, // Background color for screens
        primaryColor: Colors.black, // Primary color for elements like AppBar
        colorScheme: const ColorScheme.light(
          primary: Colors.black,   // Main theme color
          secondary: Colors.white,  // Accent color
          surface: Colors.white, // Background color
        ),
        textTheme: const TextTheme(
          bodyLarge: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w600,
            color: Colors.black, // Text color
          ),
          bodyMedium: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w500,
            color: Colors.grey, // Secondary text color
          ),
          bodySmall: TextStyle(
            fontSize: 14,
            color: Colors.grey, // Small text color
          ),
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.white, // AppBar background color
          foregroundColor: Colors.black, // AppBar text/icon color
          elevation: 0, // Remove shadow for minimalistic design
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.black, // Button background color
            foregroundColor: Colors.white, // Button text color
            shape: const RoundedRectangleBorder(
              borderRadius: BorderRadius.zero, // Flat design
            ),
          ),
        ),
        outlinedButtonTheme: OutlinedButtonThemeData(
          style: OutlinedButton.styleFrom(
            side: const BorderSide(color: Colors.black), // Border color
            foregroundColor: Colors.black, // Text color
            shape: const RoundedRectangleBorder(
              borderRadius: BorderRadius.zero, // Flat design
            ),
          ),
        ),
        inputDecorationTheme: const InputDecorationTheme(
          border: OutlineInputBorder(
            borderSide: BorderSide(color: Colors.white), // Border for inputs
          ),
          focusedBorder: OutlineInputBorder(
            borderSide: BorderSide(color: Colors.black), // Focused border
          ),
          enabledBorder: OutlineInputBorder(
            borderSide: BorderSide(color: Colors.white), // Enabled border
          ),
          hintStyle: TextStyle(color: Colors.white), // Hint text color
        ),
      ),
      home: const HomeScreen(),
    );
  }
}

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]).then((_) {
    runApp(const DeepBrisca());
  });
}
