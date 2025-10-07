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
  bool _isLoading = false;

  Future<void> _registrar() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    try {
      final endpoint = widget.tipoUsuario == 'cliente'
          ? '/clientes/registrar'
          : '/prestadores/registrar';

      final body = widget.tipoUsuario == 'cliente'
          ? {
              'nome': _nomeController.text,
              'email': _emailController.text,
              'senha': _senhaController.text,
              'telefone': _telefoneController.text,
            }
          : {
              'nome': _nomeController.text,
              'email': _emailController.text,
              'senha': _senhaController.text,
              'telefone': _telefoneController.text,
              'categorias': ['Serviços Gerais'],
              'regioes_atendimento': ['Todas'],
            };

      final response = await http.post(
        Uri.parse('${AppConstants.baseUrl}$endpoint'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );

      if (response.statusCode == 201 && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Cadastro realizado!'),
            backgroundColor: Colors.green,
          ),
        );
        Navigator.pop(context);
      } else {
        throw Exception('Erro no cadastro');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erro: $e'), backgroundColor: Colors.red),
        );
      }
    } finally {
      setState(() => _isLoading = false);
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
            _buildField(_nomeController, 'Nome Completo', Icons.person),
            _buildField(
              _emailController,
              'Email',
              Icons.email,
              type: TextInputType.emailAddress,
            ),
            _buildField(_senhaController, 'Senha', Icons.lock, obscure: true),
            _buildField(
              _telefoneController,
              'Telefone',
              Icons.phone,
              required: false,
            ),
            const SizedBox(height: 24),
            SizedBox(
              height: 56,
              child: ElevatedButton(
                onPressed: _isLoading ? null : _registrar,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFFf5c116),
                ),
                child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.black)
                    : const Text(
                        'Cadastrar',
                        style: TextStyle(fontSize: 18, color: Colors.black),
                      ),
              ),
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
