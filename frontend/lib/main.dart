import 'package:flutter/material.dart';
import 'screens/simple_home_screen.dart';
import 'screens/history_screen.dart';
import 'screens/analytics_screen.dart';
import 'screens/settings_screen.dart';
import 'screens/login_screen.dart';
import 'widgets/footer_menu.dart';
import 'constants/app_theme.dart';
import 'services/auth_service.dart';

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
      home: const AuthWrapper(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class AuthWrapper extends StatefulWidget {
  const AuthWrapper({super.key});

  @override
  State<AuthWrapper> createState() => _AuthWrapperState();
}

class _AuthWrapperState extends State<AuthWrapper> {
  bool _isLoading = true;
  bool _isLoggedIn = false;

  @override
  void initState() {
    super.initState();
    _checkAuthStatus();
  }

  Future<void> _checkAuthStatus() async {
    final isLoggedIn = await AuthService.isLoggedIn();
    setState(() {
      _isLoggedIn = isLoggedIn;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    if (_isLoggedIn) {
      return const MainNavigationScreen();
    } else {
      return const LoginScreen();
    }
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
    const SettingsScreen(),
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
            : _currentIndex == 2
            ? 'Dashboard'
            : 'Settings',
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
        onNavigateToSettings: () {
          setState(() {
            _currentIndex = 3;
          });
        },
      ),
    );
  }
}
