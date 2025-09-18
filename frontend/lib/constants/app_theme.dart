import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: const Color(0xFF2196F3), // Azul vibrante do logo
        brightness: Brightness.light,
      ),
      textTheme: const TextTheme(
        displayLarge: TextStyle(
          fontSize: 32,
          fontWeight: FontWeight.bold,
          color: Color(0xFF1976D2), // Azul escuro do texto WorcaFlow
        ),
        displayMedium: TextStyle(
          fontSize: 28,
          fontWeight: FontWeight.bold,
          color: Color(0xFF1976D2),
        ),
        displaySmall: TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.bold,
          color: Color(0xFF1976D2),
        ),
        headlineLarge: TextStyle(
          fontSize: 22,
          fontWeight: FontWeight.w600,
          color: Color(0xFF1976D2),
        ),
        headlineMedium: TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.w600,
          color: Color(0xFF1976D2),
        ),
        headlineSmall: TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.w600,
          color: Color(0xFF1976D2),
        ),
        titleLarge: TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.w600,
          color: Color(0xFF333333),
        ),
        titleMedium: TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.w600,
          color: Color(0xFF333333),
        ),
        titleSmall: TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.w600,
          color: Color(0xFF333333),
        ),
        bodyLarge: TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.normal,
          color: Color(0xFF333333),
        ),
        bodyMedium: TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.normal,
          color: Color(0xFF333333),
        ),
        bodySmall: TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.normal,
          color: Color(0xFF666666),
        ),
        labelLarge: TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.w600,
          color: Color(0xFF2196F3),
        ),
        labelMedium: TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.w600,
          color: Color(0xFF2196F3),
        ),
        labelSmall: TextStyle(
          fontSize: 10,
          fontWeight: FontWeight.w600,
          color: Color(0xFF2196F3),
        ),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Color(0xFFFFFFFF),
        foregroundColor: Color(0xFF1976D2),
        elevation: 2,
        shadowColor: Color(0x1A000000),
        titleTextStyle: TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.w600,
          color: Color(0xFF1976D2),
        ),
      ),
      cardTheme: CardThemeData(
        color: const Color(0xFFFFFFFF),
        elevation: 4,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: const Color(0xFF2196F3), // Azul vibrante do logo
          foregroundColor: Colors.white,
          elevation: 4,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: const Color(0xFF2196F3),
          side: const BorderSide(color: Color(0xFF2196F3)),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: const Color(0xFF2196F3),
          textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: const Color(0xFFFFFFFF),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: Color(0xFFDDDDDD)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: Color(0xFFDDDDDD)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: Color(0xFF2196F3), width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: Color(0xFFf44336)),
        ),
        focusedErrorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: Color(0xFFf44336), width: 2),
        ),
        labelStyle: const TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.w600,
          color: Color(0xFF333333),
        ),
        hintStyle: const TextStyle(fontSize: 16, color: Color(0xFF999999)),
      ),
      bottomNavigationBarTheme: const BottomNavigationBarThemeData(
        backgroundColor: Color(0xFFFFFFFF),
        selectedItemColor: Color(0xFF2196F3),
        unselectedItemColor: Color(0xFF666666),
        elevation: 8,
        type: BottomNavigationBarType.fixed,
      ),
    );
  }
}
