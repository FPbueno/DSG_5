import 'package:flutter/material.dart';
import 'home_prestador_screen.dart';
import 'settings_prestador_screen.dart';
import 'historico_prestador_screen.dart';
import '../../widgets/footer_menu.dart';

class MainPrestadorScreen extends StatefulWidget {
  final int usuarioId;
  final String nome;

  const MainPrestadorScreen({
    super.key,
    required this.usuarioId,
    required this.nome,
  });

  @override
  State<MainPrestadorScreen> createState() => _MainPrestadorScreenState();
}

class _MainPrestadorScreenState extends State<MainPrestadorScreen> {
  String _currentScreen = 'Home';

  Widget _getCurrentScreen() {
    switch (_currentScreen) {
      case 'Settings':
        return SettingsPrestadorScreen(
          usuarioId: widget.usuarioId,
          nome: widget.nome,
        );
      case 'Historico':
        return HistoricoPrestadorScreen(
          usuarioId: widget.usuarioId,
          nome: widget.nome,
        );
      default:
        return HomePrestadorScreen(
          usuarioId: widget.usuarioId,
          nome: widget.nome,
        );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _getCurrentScreen(),
      bottomNavigationBar: FooterMenu(
        currentScreen: _currentScreen,
        onNavigateToHome: () => setState(() => _currentScreen = 'Home'),
        onNavigateToSettings: () => setState(() => _currentScreen = 'Settings'),
        onNavigateToHistorico: () =>
            setState(() => _currentScreen = 'Historico'),
      ),
    );
  }
}
