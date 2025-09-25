import 'package:flutter/material.dart';
import '../widgets/footer_menu.dart';
import 'home_screen.dart';
import 'history_screen.dart';
import 'analytics_screen.dart';
import 'settings_screen.dart';

class MainNavigationScreen extends StatefulWidget {
  const MainNavigationScreen({super.key});

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  int _currentIndex = 0;
  String _currentScreen = 'Home';

  final List<Widget> _screens = [
    const HomeScreen(),
    const HistoryScreen(),
    const AnalyticsScreen(),
    const SettingsScreen(),
  ];

  void _onNavigateToHome() {
    setState(() {
      _currentIndex = 0;
      _currentScreen = 'Home';
    });
  }

  void _onNavigateToHistory() {
    setState(() {
      _currentIndex = 1;
      _currentScreen = 'History';
    });
  }

  void _onNavigateToDashboard() {
    setState(() {
      _currentIndex = 2;
      _currentScreen = 'Dashboard';
    });
  }

  void _onNavigateToSettings() {
    setState(() {
      _currentIndex = 3;
      _currentScreen = 'Settings';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Conteúdo principal
          Positioned.fill(
            bottom: 70, // Espaço para o footer
            child: _screens[_currentIndex],
          ),
          // Footer menu
          Positioned(
            left: 0,
            right: 0,
            bottom: 0,
            child: FooterMenu(
              currentScreen: _currentScreen,
              onNavigateToHome: _onNavigateToHome,
              onNavigateToHistory: _onNavigateToHistory,
              onNavigateToDashboard: _onNavigateToDashboard,
              onNavigateToSettings: _onNavigateToSettings,
            ),
          ),
        ],
      ),
    );
  }
}
