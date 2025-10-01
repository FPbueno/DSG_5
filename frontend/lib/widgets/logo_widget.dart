import 'package:flutter/material.dart';

class LogoWidget extends StatelessWidget {
  final String size;
  final bool showText;

  const LogoWidget({super.key, this.size = 'medium', this.showText = true});

  @override
  Widget build(BuildContext context) {
    double logoSize;

    switch (size) {
      case 'small':
        logoSize = 80;
        break;
      case 'large':
        logoSize = 120;
        break;
      default:
        logoSize = 100;
    }

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Logo da imagem
        Container(
          width: logoSize,
          height: logoSize,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(logoSize / 2),
            boxShadow: [
              BoxShadow(
                color: const Color(0xFF2196F3).withValues(alpha: 0.3),
                blurRadius: 20,
                spreadRadius: 2,
              ),
            ],
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(logoSize / 2),
            child: Image.asset(
              'assets/images/logo.png',
              width: logoSize,
              height: logoSize,
              fit: BoxFit.contain,
              errorBuilder: (context, error, stackTrace) {
                // Fallback caso a imagem não carregue
                return Container(
                  width: logoSize,
                  height: logoSize,
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                      colors: [
                        Color(0xFF2196F3), // Azul vibrante
                        Color(0xFF00BCD4), // Azul turquesa
                      ],
                    ),
                    borderRadius: BorderRadius.circular(logoSize / 2),
                  ),
                  child: const Center(
                    child: Text(
                      '\$',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
        ),
        // Texto WorcaFlow
        if (showText) ...[
          const SizedBox(height: 8),
          Text(
            'WorcaFlow',
            style: TextStyle(
              fontSize: logoSize * 0.2,
              fontWeight: FontWeight.bold,
              color: const Color(0xFF1976D2), // Azul escuro do texto
              letterSpacing: 1.2,
            ),
          ),
        ],
      ],
    );
  }
}
