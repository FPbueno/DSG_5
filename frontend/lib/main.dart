import 'package:flutter/material.dart';
import 'screens/simple_home_screen.dart';
import 'screens/history_screen.dart';
import 'screens/analytics_screen.dart';
import 'widgets/footer_menu.dart';
import 'constants/app_theme.dart';

void main() {
  runApp(const WorcaFlowApp());
}

class WorcaFlowApp extends StatelessWidget {
  const WorcaFlowApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'WorcaFlow',
      theme: AppTheme.lightTheme,
      home: const MainNavigationScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class MainNavigationScreen extends StatefulWidget {
  const MainNavigationScreen({super.key});

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  int _currentIndex = 0;

  final List<Widget> _screens = [
    const SimpleHomeScreen(),
    const HistoryScreen(),
    const AnalyticsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: FooterMenu(
        currentScreen: _currentIndex == 0
            ? 'Home'
            : _currentIndex == 1
            ? 'History'
            : 'Dashboard',
        onNavigateToHome: () {
          setState(() {
            _currentIndex = 0;
          });
        },
        onNavigateToHistory: () {
          setState(() {
            _currentIndex = 1;
          });
        },
        onNavigateToDashboard: () {
          setState(() {
            _currentIndex = 2;
          });
        },
      ),
    );
  }
}
