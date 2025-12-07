import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../constants/app_constants.dart';

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
  final _categoriasController = TextEditingController();
  final _regioesController = TextEditingController();
  bool _isLoading = false;
  bool _enable2fa = true;

  Future<void> _registrar() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    try {
      final endpoint = widget.tipoUsuario == 'cliente'
          ? '/registrar'
          : '/prestadores/registrar';

      final body = widget.tipoUsuario == 'cliente'
          ? {
              'nome': _nomeController.text,
              'email': _emailController.text,
              'telefone': _telefoneController.text,
              'endereco': _enderecoController.text,
              'senha': _senhaController.text,
              'enable_2fa': _enable2fa,
            }
          : {
              'nome': _nomeController.text,
              'email': _emailController.text,
              'senha': _senhaController.text,
              'telefone': _telefoneController.text,
              'categorias': _categoriasController.text
                  .split(',')
                  .map((e) => e.trim())
                  .toList(),
              'regioes_atendimento': _regioesController.text
                  .split(',')
                  .map((e) => e.trim())
                  .toList(),
              'enable_2fa': _enable2fa,
            };

      final response = await http.post(
        Uri.parse('${AppConstants.baseUrl}$endpoint'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Cadastro realizado com sucesso.'),
              backgroundColor: Colors.green,
            ),
          );
          Navigator.pop(context); // Volta para tela de login
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
          'Cadastro ${widget.tipoUsuario == "cliente" ? "Cliente" : "Prestador"}',
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
                  required: false,
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
                const SizedBox(height: 12),
                _buildTwoFactorSelector(),
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

  Widget _buildTwoFactorSelector() {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: const Color(0xFFf5c116).withValues(alpha: 0.3),
          width: 1.4,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Autenticação em 2 Fatores',
            style: TextStyle(
              color: Colors.white,
              fontSize: 16,
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              ChoiceChip(
                label: const Text('Habilitar'),
                selected: _enable2fa,
                selectedColor: const Color(0xFFf5c116),
                labelStyle: TextStyle(
                  color: _enable2fa ? Colors.black : Colors.white,
                  fontWeight: FontWeight.w600,
                ),
                onSelected: (_) => setState(() => _enable2fa = true),
              ),
              ChoiceChip(
                label: const Text('Desabilitar'),
                selected: !_enable2fa,
                selectedColor: Colors.grey[800],
                labelStyle: TextStyle(
                  color: !_enable2fa ? Colors.black : Colors.white,
                  fontWeight: FontWeight.w600,
                ),
                onSelected: (_) => setState(() => _enable2fa = false),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            _enable2fa
                ? 'Solicitaremos o código 2FA nos logins.'
                : 'Cadastro sem exigir segundo fator (se permitido pelo backend).',
            style: TextStyle(
              color: Colors.grey[400],
              fontSize: 12,
            ),
          ),
        ],
      ),
    );
  }
}
