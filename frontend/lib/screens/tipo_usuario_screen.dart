import 'package:flutter/material.dart';
import 'login_screen.dart';

class TipoUsuarioScreen extends StatelessWidget {
  const TipoUsuarioScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(color: Colors.black),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24.0),
            child: SingleChildScrollView(
              child: Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Logo
                    Image.asset(
                      'assets/images/Worca.png',
                      height: 200,
                      width: 250,
                      fit: BoxFit.contain,
                      errorBuilder: (context, error, stackTrace) {
                        return Icon(
                          Icons.home_work,
                          size: 200,
                          color: Color(0xFFf5c116),
                        );
                      },
                    ),
                    const SizedBox(height: 40),

                    // Título
                    const Text(
                      'Bem-vindo ao Worca!',
                      style: TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 16),

                    Text(
                      'Escolha como deseja continuar',
                      style: TextStyle(fontSize: 16, color: Colors.grey[300]),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 60),

                    // Card Cliente
                    _buildUserTypeCard(
                      context,
                      icon: Icons.person,
                      title: 'Sou Cliente',
                      subtitle: 'Quero solicitar orçamentos',
                      tipoUsuario: 'cliente',
                    ),
                    const SizedBox(height: 24),

                    // Card Prestador
                    _buildUserTypeCard(
                      context,
                      icon: Icons.work,
                      title: 'Sou Prestador',
                      subtitle: 'Quero oferecer meus serviços',
                      tipoUsuario: 'prestador',
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildUserTypeCard(
    BuildContext context, {
    required IconData icon,
    required String title,
    required String subtitle,
    required String tipoUsuario,
  }) {
    return GestureDetector(
      onTap: () {
        Navigator.of(context).push(
          MaterialPageRoute(
            builder: (context) => LoginScreen(tipoUsuario: tipoUsuario),
          ),
        );
      },
      child: Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          color: const Color(0xFF1a1a1a),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: const Color(0xFF333333), width: 2),
          boxShadow: [
            BoxShadow(
              color: const Color(0xFFf5c116).withValues(alpha: 0.1),
              blurRadius: 15,
              offset: const Offset(0, 5),
            ),
          ],
        ),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFFf5c116),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(icon, size: 40, color: Colors.black),
            ),
            const SizedBox(width: 20),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    subtitle,
                    style: TextStyle(fontSize: 14, color: Colors.grey[400]),
                  ),
                ],
              ),
            ),
            Icon(
              Icons.arrow_forward_ios,
              color: const Color(0xFFf5c116),
              size: 24,
            ),
          ],
        ),
      ),
    );
  }
}
