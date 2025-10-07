import 'package:flutter/material.dart';
import 'home_cliente_screen.dart';
import 'settings_cliente_screen.dart';
import 'historico_cliente_screen.dart';
import '../../widgets/footer_menu.dart';

class MainClienteScreen extends StatefulWidget {
  final int usuarioId;
  final String nome;

  const MainClienteScreen({
    super.key,
    required this.usuarioId,
    required this.nome,
  });

  @override
  State<MainClienteScreen> createState() => _MainClienteScreenState();
}

class _MainClienteScreenState extends State<MainClienteScreen> {
  String _currentScreen = 'Home';

  Widget _getCurrentScreen() {
    switch (_currentScreen) {
      case 'Settings':
        return SettingsClienteScreen(
          usuarioId: widget.usuarioId,
          nome: widget.nome,
        );
      case 'Historico':
        return HistoricoClienteScreen(
          usuarioId: widget.usuarioId,
          nome: widget.nome,
        );
      default:
        return HomeClienteScreen(
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
