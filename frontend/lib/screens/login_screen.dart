import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import '../constants/app_constants.dart';
import '../services/rsa_service.dart';
import 'cliente/main_cliente_screen.dart';
import 'prestador/main_prestador_screen.dart';
import 'register_screen.dart';

class LoginScreen extends StatefulWidget {
  final String tipoUsuario;

  const LoginScreen({super.key, required this.tipoUsuario});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;
  bool _obscurePassword = true;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _login() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    try {
      final senhaCriptografada = await RSAService.encryptPassword(
        _passwordController.text,
      );

      final response = await http.post(
        Uri.parse('${AppConstants.baseUrl}/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': _emailController.text.trim(),
          'senha': senhaCriptografada,
          'tipo_usuario': widget.tipoUsuario,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        // Verifica se a autenticação de 2FA é necessária
        // A API retorna "require_2fa": true quando precisa de 2FA
        if (data.containsKey('require_2fa') && data['require_2fa'] == true) {
          // Navega para a tela de 2FA
          if (mounted) {
            Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => TwoFactorScreen(
                  email: _emailController.text.trim(),
                  tipoUsuario: widget.tipoUsuario,
                  usuarioId: data['usuario_id'] ?? 0,
                ),
              ),
            );
          }
        } else {
          // Se não requer 2FA, já faz login completo (não deveria acontecer)
          _onLoginSuccess(data);
        }
      } else {
        final errorData = jsonDecode(response.body);
        final errorMsg = errorData['detail'] ?? 'Email ou senha incorretos';

        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(errorMsg), backgroundColor: Colors.red),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erro: $e'), backgroundColor: Colors.red),
        );
      }
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  // Salva dados de login e navega
  Future<void> _onLoginSuccess(Map<String, dynamic> data) async {
    if (!mounted) return;

    try {
      // Salva token e dados do usuário
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('auth_token', data['token'] ?? '');
      await prefs.setString('user_data', jsonEncode(data));
    } catch (e) {
      debugPrint('Erro ao salvar dados: $e');
    }

    if (mounted) {
      // Navega para a tela principal específica do tipo de usuário
      if (widget.tipoUsuario == 'cliente') {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(
            builder: (context) => MainClienteScreen(
              usuarioId: data['usuario_id'] ?? 0,
              nome: data['nome'] ?? '',
            ),
          ),
        );
      } else {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(
            builder: (context) => MainPrestadorScreen(
              usuarioId: data['usuario_id'] ?? 0,
              nome: data['nome'] ?? '',
            ),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final isCliente = widget.tipoUsuario == 'cliente';

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(color: Colors.black),
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24.0),
            child: ConstrainedBox(
              constraints: BoxConstraints(
                minHeight:
                    MediaQuery.of(context).size.height -
                    MediaQuery.of(context).padding.top -
                    MediaQuery.of(context).padding.bottom,
              ),
              child: Column(
                children: [
                  const SizedBox(height: 20),

                  // Botão Voltar
                  Align(
                    alignment: Alignment.centerLeft,
                    child: IconButton(
                      onPressed: () => Navigator.pop(context),
                      icon: const Icon(
                        Icons.arrow_back,
                        color: Color(0xFFf5c116),
                        size: 28,
                      ),
                    ),
                  ),
                  const SizedBox(height: 10),

                  // Logo
                  Image.asset(
                    'assets/images/Worca.png',
                    height: 200,
                    fit: BoxFit.contain,
                    errorBuilder: (_, __, ___) => Icon(
                      Icons.home_work,
                      size: 200,
                      color: Color(0xFFf5c116),
                    ),
                  ),
                  const SizedBox(height: 20),

                  // Título com tipo de usuário
                  Text(
                    isCliente ? 'Login Cliente' : 'Login Prestador',
                    style: const TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 32),

                  // Formulário
                  Form(
                    key: _formKey,
                    child: Column(
                      children: [
                        _buildTextField(
                          controller: _emailController,
                          label: 'Email',
                          icon: Icons.email,
                          validator: (v) => v!.isEmpty || !v.contains('@')
                              ? 'Email inválido'
                              : null,
                        ),
                        const SizedBox(height: 20),

                        _buildTextField(
                          controller: _passwordController,
                          label: 'Senha',
                          icon: Icons.lock,
                          obscure: _obscurePassword,
                          suffixIcon: IconButton(
                            icon: Icon(
                              _obscurePassword
                                  ? Icons.visibility
                                  : Icons.visibility_off,
                              color: Colors.grey[600],
                            ),
                            onPressed: () => setState(
                              () => _obscurePassword = !_obscurePassword,
                            ),
                          ),
                          validator: (v) =>
                              v!.isEmpty ? 'Senha obrigatória' : null,
                        ),
                        const SizedBox(height: 30),

                        // Botão Login
                        SizedBox(
                          width: double.infinity,
                          height: 56,
                          child: ElevatedButton(
                            onPressed: _isLoading ? null : _login,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: const Color(0xFFf5c116),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                            ),
                            child: _isLoading
                                ? const CircularProgressIndicator(
                                    color: Colors.black,
                                  )
                                : const Text(
                                    'Entrar',
                                    style: TextStyle(
                                      fontSize: 18,
                                      fontWeight: FontWeight.w600,
                                      color: Colors.black,
                                    ),
                                  ),
                          ),
                        ),
                        const SizedBox(height: 24),

                        // Link para registro
                        TextButton(
                          onPressed: () => Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => RegisterScreen(
                                tipoUsuario: widget.tipoUsuario,
                              ),
                            ),
                          ),
                          child: RichText(
                            text: TextSpan(
                              style: TextStyle(
                                color: Colors.grey[300],
                                fontSize: 16,
                              ),
                              children: [
                                const TextSpan(text: 'Não tem conta? '),
                                TextSpan(
                                  text: 'Cadastre-se',
                                  style: TextStyle(
                                    color: Color(0xFFf5c116),
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  // Método _buildTextField para TwoFactorScreen
  Widget _buildTextField({
    required TextEditingController controller,
    required String label,
    required IconData icon,
    bool obscure = false,
    Widget? suffixIcon,
    String? Function(String?)? validator,
    TextInputType? keyboardType,
    int? maxLength,
  }) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        color: Colors.white.withValues(alpha: 0.9),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.1),
            blurRadius: 10,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: TextFormField(
        controller: controller,
        obscureText: obscure,
        keyboardType: keyboardType,
        maxLength: maxLength,
        style: const TextStyle(color: Colors.black),
        decoration: InputDecoration(
          labelText: label,
          labelStyle: TextStyle(color: Colors.grey[600]),
          prefixIcon: Icon(icon, color: Colors.grey[600]),
          suffixIcon: suffixIcon,
          counterText: maxLength != null ? '' : null,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide.none,
          ),
          filled: true,
          fillColor: Colors.transparent,
        ),
        validator: validator,
      ),
    );
  }
}

// Tela para autenticação de 2 fatores
class TwoFactorScreen extends StatefulWidget {
  final String email;
  final String tipoUsuario;
  final int usuarioId;

  const TwoFactorScreen({
    super.key,
    required this.email,
    required this.tipoUsuario,
    required this.usuarioId,
  });

  @override
  State<TwoFactorScreen> createState() => _TwoFactorScreenState();
}

class _TwoFactorScreenState extends State<TwoFactorScreen> {
  final _twoFactorController = TextEditingController();
  bool _isLoading = false;

  @override
  void dispose() {
    _twoFactorController.dispose();
    super.dispose();
  }

  Future<void> _verifyTwoFactorCode() async {
    final code = _twoFactorController.text.trim();

    // Validação: aceita código TOTP (6 dígitos) ou backup code (formato XXXX-XXXX-XXXX)
    final codeClean = code
        .replaceAll('-', '')
        .replaceAll(' ', '')
        .toUpperCase();
    final isTOTP =
        codeClean.length == 6 && RegExp(r'^\d+$').hasMatch(codeClean);
    final isBackupCode =
        codeClean.length == 12 &&
        RegExp(r'^[A-F0-9]+$').hasMatch(codeClean) &&
        code.contains('-');

    if (code.isEmpty || (!isTOTP && !isBackupCode)) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'Por favor, insira um código 2FA válido (6 dígitos) ou código de backup (XXXX-XXXX-XXXX)',
          ),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      // Chama o endpoint /login-2fa conforme a API
      final response = await http.post(
        Uri.parse('${AppConstants.baseUrl}/login-2fa'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': widget.email,
          'tipo_usuario': widget.tipoUsuario,
          'codigo': code, // Código de 6 dígitos do app autenticador
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        // Salva token e dados do usuário
        await _saveLoginData(data);

        _onLoginSuccess(data); // Login completo após verificar o código 2FA
      } else {
        final errorData = jsonDecode(response.body);
        final errorMsg = errorData['detail'] ?? 'Código 2FA inválido';

        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(errorMsg), backgroundColor: Colors.red),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Erro ao verificar código 2FA: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  Future<void> _saveLoginData(Map<String, dynamic> data) async {
    try {
      // Salva token usando SharedPreferences
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('auth_token', data['token'] ?? '');
      await prefs.setString('user_data', jsonEncode(data));
    } catch (e) {
      debugPrint('Erro ao salvar dados de login: $e');
    }
  }

  Future<void> _onLoginSuccess(Map<String, dynamic> data) async {
    if (!mounted) return;

    try {
      // Salva token e dados do usuário
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('auth_token', data['token'] ?? '');
      await prefs.setString('user_data', jsonEncode(data));
    } catch (e) {
      debugPrint('Erro ao salvar dados: $e');
    }

    if (mounted) {
      // Navega para a tela principal específica do tipo de usuário
      if (widget.tipoUsuario == 'cliente') {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(
            builder: (context) => MainClienteScreen(
              usuarioId: data['usuario_id'] ?? widget.usuarioId,
              nome: data['nome'] ?? '',
            ),
          ),
        );
      } else {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(
            builder: (context) => MainPrestadorScreen(
              usuarioId: data['usuario_id'] ?? widget.usuarioId,
              nome: data['nome'] ?? '',
            ),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(color: Colors.black),
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24.0),
            child: ConstrainedBox(
              constraints: BoxConstraints(
                minHeight:
                    MediaQuery.of(context).size.height -
                    MediaQuery.of(context).padding.top -
                    MediaQuery.of(context).padding.bottom,
              ),
              child: Column(
                children: [
                  const SizedBox(height: 20),

                  // Botão Voltar
                  Align(
                    alignment: Alignment.centerLeft,
                    child: IconButton(
                      onPressed: () => Navigator.pop(context),
                      icon: const Icon(
                        Icons.arrow_back,
                        color: Color(0xFFf5c116),
                        size: 28,
                      ),
                    ),
                  ),
                  const SizedBox(height: 10),

                  // Logo
                  Image.asset(
                    'assets/images/Worca.png',
                    height: 200,
                    fit: BoxFit.contain,
                    errorBuilder: (_, __, ___) => Icon(
                      Icons.home_work,
                      size: 200,
                      color: Color(0xFFf5c116),
                    ),
                  ),
                  const SizedBox(height: 20),

                  // Título
                  const Text(
                    'Autenticação de Dois Fatores',
                    style: TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 32),

                  // Instruções
                  const Text(
                    'Digite o código de 6 dígitos do app autenticador ou um código de backup (XXXX-XXXX-XXXX)',
                    style: TextStyle(color: Colors.white70, fontSize: 14),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 20),

                  // Campo para código 2FA
                  _buildTextField(
                    controller: _twoFactorController,
                    label: 'Código 2FA ou Backup Code',
                    icon: Icons.lock_clock,
                    keyboardType: TextInputType.text,
                    maxLength: null,
                    validator: (v) {
                      if (v == null || v.isEmpty) {
                        return 'Digite o código 2FA ou backup code';
                      }
                      final codeClean = v
                          .replaceAll('-', '')
                          .replaceAll(' ', '')
                          .toUpperCase();
                      final isTOTP =
                          codeClean.length == 6 &&
                          RegExp(r'^\d+$').hasMatch(codeClean);
                      final isBackupCode =
                          codeClean.length == 12 &&
                          RegExp(r'^[A-F0-9]+$').hasMatch(codeClean) &&
                          v.contains('-');
                      if (!isTOTP && !isBackupCode) {
                        return 'Código inválido. Use 6 dígitos ou formato XXXX-XXXX-XXXX';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 30),

                  // Botão Verificar
                  SizedBox(
                    width: double.infinity,
                    height: 56,
                    child: ElevatedButton(
                      onPressed: _isLoading ? null : _verifyTwoFactorCode,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFFf5c116),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      child: _isLoading
                          ? const CircularProgressIndicator(color: Colors.black)
                          : const Text(
                              'Verificar',
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
        ),
      ),
    );
  }

  // Método _buildTextField para TwoFactorScreen
  Widget _buildTextField({
    required TextEditingController controller,
    required String label,
    required IconData icon,
    bool obscure = false,
    Widget? suffixIcon,
    String? Function(String?)? validator,
    TextInputType? keyboardType,
    int? maxLength,
  }) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        color: Colors.white.withValues(alpha: 0.9),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.1),
            blurRadius: 10,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: TextFormField(
        controller: controller,
        obscureText: obscure,
        keyboardType: keyboardType,
        maxLength: maxLength,
        style: const TextStyle(color: Colors.black),
        decoration: InputDecoration(
          labelText: label,
          labelStyle: TextStyle(color: Colors.grey[600]),
          prefixIcon: Icon(icon, color: Colors.grey[600]),
          suffixIcon: suffixIcon,
          counterText: maxLength != null ? '' : null,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide.none,
          ),
          filled: true,
          fillColor: Colors.transparent,
        ),
        validator: validator,
      ),
    );
  }
}
