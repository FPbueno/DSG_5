import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:convert';

/// Tela para mostrar o código secreto 2FA após registro
/// Permite copiar o código e mostra instruções de configuração
class Setup2FAScreen extends StatelessWidget {
  final String totpSecret;
  final String email;
  final String tipoUsuario;
  final String? qrCode;
  final List<String>? backupCodes;

  const Setup2FAScreen({
    super.key,
    required this.totpSecret,
    required this.email,
    required this.tipoUsuario,
    this.qrCode,
    this.backupCodes,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text(
          'Configurar 2FA',
          style: TextStyle(color: Colors.white),
        ),
        iconTheme: const IconThemeData(color: Color(0xFFf5c116)),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 20),

              // Ícone
              const Icon(Icons.security, size: 80, color: Color(0xFFf5c116)),
              const SizedBox(height: 24),

              // Título
              const Text(
                'Configuração de Autenticação em Dois Fatores',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),

              // Instruções
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Instruções:',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 12),
                    const Text(
                      '1. Abra o app autenticador no seu celular (Google Authenticator, Authy, Microsoft Authenticator, etc.)',
                      style: TextStyle(color: Colors.white70, fontSize: 14),
                    ),
                    const SizedBox(height: 8),
                    if (qrCode != null) ...[
                      const Text(
                        '2. Escaneie o QR Code abaixo',
                        style: TextStyle(color: Colors.white70, fontSize: 14),
                      ),
                      const SizedBox(height: 8),
                      const Text(
                        '3. Ou digite o código secreto manualmente se preferir',
                        style: TextStyle(color: Colors.white70, fontSize: 14),
                      ),
                    ] else ...[
                      const Text(
                        '2. Adicione uma nova conta manualmente',
                        style: TextStyle(color: Colors.white70, fontSize: 14),
                      ),
                      const SizedBox(height: 8),
                      const Text(
                        '3. Digite o código secreto abaixo',
                        style: TextStyle(color: Colors.white70, fontSize: 14),
                      ),
                    ],
                    const SizedBox(height: 8),
                    const Text(
                      '4. Salve o código em local seguro (você precisará dele caso perca o acesso ao app)',
                      style: TextStyle(color: Colors.white70, fontSize: 14),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // QR Code
              if (qrCode != null) ...[
                const Text(
                  'QR Code:',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: const Color(0xFFf5c116),
                      width: 2,
                    ),
                  ),
                  child: (qrCode != null && qrCode!.isNotEmpty)
                      ? Image.memory(
                          base64Decode(
                            qrCode!.contains(',')
                                ? qrCode!.split(',')[1]
                                : qrCode!,
                          ),
                          width: 250,
                          height: 250,
                          errorBuilder: (context, error, stackTrace) {
                            debugPrint('Erro ao carregar QR Code: $error');
                            return const Icon(
                              Icons.error_outline,
                              color: Colors.red,
                              size: 250,
                            );
                          },
                        )
                      : const CircularProgressIndicator(),
                ),
                const SizedBox(height: 24),
              ],

              // Código Secreto
              const Text(
                'Código Secreto (Base32):',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  color: Colors.white,
                ),
              ),
              const SizedBox(height: 8),

              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.9),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: const Color(0xFFf5c116), width: 2),
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: SelectableText(
                        totpSecret,
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.black,
                          letterSpacing: 2,
                        ),
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.copy, color: Color(0xFFf5c116)),
                      onPressed: () {
                        Clipboard.setData(ClipboardData(text: totpSecret));
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text(
                              'Código copiado para a área de transferência!',
                            ),
                            backgroundColor: Colors.green,
                            duration: Duration(seconds: 2),
                          ),
                        );
                      },
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Backup Codes
              if (backupCodes != null && backupCodes!.isNotEmpty) ...[
                const Text(
                  'Códigos de Backup (Salve em local seguro):',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 8),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.orange.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.orange, width: 2),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'IMPORTANTE: Estes códigos permitem recuperar acesso se você perder o app autenticador. Cada código só pode ser usado uma vez.',
                        style: TextStyle(
                          color: Colors.orange,
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 12),
                      ...backupCodes!.map(
                        (code) => Padding(
                          padding: const EdgeInsets.symmetric(vertical: 4),
                          child: Row(
                            children: [
                              Expanded(
                                child: SelectableText(
                                  code,
                                  style: const TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.white,
                                    letterSpacing: 1,
                                  ),
                                ),
                              ),
                              IconButton(
                                icon: const Icon(
                                  Icons.copy,
                                  color: Color(0xFFf5c116),
                                  size: 20,
                                ),
                                onPressed: () {
                                  Clipboard.setData(ClipboardData(text: code));
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    SnackBar(
                                      content: Text('Código $code copiado!'),
                                      backgroundColor: Colors.green,
                                      duration: const Duration(seconds: 2),
                                    ),
                                  );
                                },
                              ),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(height: 8),
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          onPressed: () {
                            final allCodes = backupCodes!.join('\n');
                            Clipboard.setData(ClipboardData(text: allCodes));
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text('Todos os códigos copiados!'),
                                backgroundColor: Colors.green,
                                duration: Duration(seconds: 2),
                              ),
                            );
                          },
                          icon: const Icon(Icons.copy_all, color: Colors.black),
                          label: const Text(
                            'Copiar Todos',
                            style: TextStyle(
                              color: Colors.black,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFFf5c116),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(8),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 24),
              ],

              // Botão de ajuda
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.blue.withValues(alpha: 0.2),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: const Row(
                  children: [
                    Icon(Icons.info_outline, color: Colors.blue, size: 20),
                    SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        'Após configurar, você precisará do código gerado pelo app ou um código de backup para fazer login.',
                        style: TextStyle(color: Colors.white70, fontSize: 12),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 32),

              // Botão Continuar
              SizedBox(
                height: 56,
                child: ElevatedButton(
                  onPressed: () {
                    // Navega de volta para login
                    Navigator.of(context).popUntil((route) => route.isFirst);
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFFf5c116),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Text(
                    'Continuar para Login',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                      color: Colors.black,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
