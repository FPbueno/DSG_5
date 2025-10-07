import 'package:flutter/material.dart';
import 'screens/tipo_usuario_screen.dart';
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
      home: const TipoUsuarioScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
