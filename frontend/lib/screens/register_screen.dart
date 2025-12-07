import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../constants/app_constants.dart';
import '../services/rsa_service.dart';
import 'setup_2fa_screen.dart';

class RegisterScreen extends StatefulWidget {
  final String tipoUsuario;
  const RegisterScreen({super.key, required this.tipoUsuario});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nomeController = TextEditingController();
  final _emailController = TextEditingController();
  final _senhaController = TextEditingController();
  final _telefoneController = TextEditingController();
  final _enderecoController = TextEditingController();
  final _categoriasController = TextEditingController(); // Para prestador
  final _regioesController = TextEditingController(); // Para prestador
  bool _isLoading = false;

  Future<void> _registrar() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    try {
      final endpoint = widget.tipoUsuario == 'cliente'
          ? '/registrar'
          : '/prestadores/registrar';

      // Criptografa a senha usando o RSAService
      final senhaCriptografada = await RSAService.encryptPassword(
        _senhaController.text,
      );

      final body = widget.tipoUsuario == 'cliente'
          ? {
              'nome': _nomeController.text,
              'email': _emailController.text,
              'telefone': _telefoneController.text,
              'endereco': _enderecoController.text,
              'senha': senhaCriptografada,
            }
          : {
              'nome': _nomeController.text,
              'email': _emailController.text,
              'senha': senhaCriptografada,
              'telefone': _telefoneController.text,
              'categorias': _categoriasController.text
                  .split(',')
                  .map((e) => e.trim())
                  .toList(),
              'regioes_atendimento': _regioesController.text
                  .split(',')
                  .map((e) => e.trim())
                  .toList(),
            };

      final response = await http.post(
        Uri.parse('${AppConstants.baseUrl}$endpoint'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        final data = jsonDecode(response.body);
        final totpSecret = data['codigo_2fa'];
        final qrCode = data['qr_code'] as String?;
        final backupCodes = data['backup_codes'] != null
            ? List<String>.from(data['backup_codes'])
            : null;

        debugPrint('QR Code recebido: ${qrCode != null ? "Sim" : "Não"}');
        debugPrint(
          'Backup codes recebidos: ${backupCodes != null ? backupCodes.length : 0}',
        );

        if (mounted && totpSecret != null) {
          // Navega para tela de configuração do 2FA
          Navigator.of(context).pushReplacement(
            MaterialPageRoute(
              builder: (context) => Setup2FAScreen(
                totpSecret: totpSecret,
                email: _emailController.text.trim(),
                tipoUsuario: widget.tipoUsuario,
                qrCode: qrCode,
                backupCodes: backupCodes,
              ),
            ),
          );
        } else {
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text(
                  'Cadastro realizado, mas código 2FA não foi retornado',
                ),
                backgroundColor: Colors.orange,
              ),
            );
          }
        }
      } else {
        final error = jsonDecode(response.body);
        throw Exception(error['detail'] ?? 'Erro no cadastro');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erro: $e'), backgroundColor: Colors.red),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: Text(
          'Cadastro ${widget.tipoUsuario == 'cliente' ? 'Cliente' : 'Prestador'}',
        ),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(24),
          children: [
            Column(
              children: [
                _buildField(_nomeController, 'Nome Completo', Icons.person),
                _buildField(
                  _emailController,
                  'Email',
                  Icons.email,
                  type: TextInputType.emailAddress,
                ),
                _buildField(
                  _senhaController,
                  'Senha',
                  Icons.lock,
                  obscure: true,
                ),
                _buildField(
                  _telefoneController,
                  'Telefone',
                  Icons.phone,
                  required: false,
                ),
                if (widget.tipoUsuario == 'cliente')
                  _buildField(
                    _enderecoController,
                    'Endereço',
                    Icons.location_on,
                    required: false,
                  ),
                if (widget.tipoUsuario == 'prestador') ...[
                  _buildField(
                    _categoriasController,
                    'Categorias (separadas por vírgula)',
                    Icons.category,
                  ),
                  _buildField(
                    _regioesController,
                    'Regiões de Atendimento (separadas por vírgula)',
                    Icons.map,
                  ),
                ],
                const SizedBox(height: 24),
                SizedBox(
                  height: 56,
                  child: ElevatedButton(
                    onPressed: _isLoading ? null : _registrar,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFFf5c116),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: _isLoading
                        ? const CircularProgressIndicator(color: Colors.black)
                        : const Text(
                            'Cadastrar',
                            style: TextStyle(
                              fontSize: 18,
                              color: Colors.black,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                  ),
                ),
                const SizedBox(height: 16),
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text(
                    'Já tem conta? Faça login',
                    style: TextStyle(color: Color(0xFFf5c116)),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildField(
    TextEditingController controller,
    String label,
    IconData icon, {
    bool obscure = false,
    TextInputType? type,
    bool required = true,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          color: Colors.white.withValues(alpha: 0.9),
        ),
        child: TextFormField(
          controller: controller,
          obscureText: obscure,
          keyboardType: type,
          decoration: InputDecoration(
            labelText: label,
            prefixIcon: Icon(icon, color: Colors.grey[600]),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: BorderSide.none,
            ),
          ),
          validator: (v) =>
              required && (v == null || v.isEmpty) ? 'Campo obrigatório' : null,
        ),
      ),
    );
  }
}
