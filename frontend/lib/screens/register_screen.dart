import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../constants/app_constants.dart';
import '../services/rsa_service.dart'; // Importe o serviço RSA

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
  String? _totpSecret; // Para armazenar o código 2FA retornado

  Future<void> _registrar() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    try {
      final endpoint = widget.tipoUsuario == 'cliente' ? '/registrar' : '/prestadores/registrar';

      // Criptografa a senha usando o RSAService
      final senhaCriptografada = await RSAService.encryptPassword(_senhaController.text);

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
              'categorias': _categoriasController.text.split(',').map((e) => e.trim()).toList(),
              'regioes_atendimento': _regioesController.text.split(',').map((e) => e.trim()).toList(),
            };

      final response = await http.post(
        Uri.parse('${AppConstants.baseUrl}$endpoint'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        final data = jsonDecode(response.body);
        setState(() {
          _totpSecret = data['codigo_2fa'];
        });
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(data['mensagem']),
              backgroundColor: Colors.green,
            ),
          );
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
            if (_totpSecret == null)
              Column(
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
                  if (widget.tipoUsuario == 'cliente')
                    _buildField(_enderecoController, 'Endereço', Icons.location_on),
                  if (widget.tipoUsuario == 'prestador') ...[
                    _buildField(_categoriasController, 'Categorias (separadas por vírgula)', Icons.category),
                    _buildField(_regioesController, 'Regiões de Atendimento (separadas por vírgula)', Icons.map),
                  ],
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
            if (_totpSecret != null)
              Column(
                children: [
                  const SizedBox(height: 20),
                  Text(
                    'Cadastro realizado com sucesso! Use o código abaixo no seu app autenticador (Google Authenticator, Authy etc.) para ativar o 2FA:',
                    style: TextStyle(color: Colors.white, fontSize: 16),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 20),
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.9),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      _totpSecret!,
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.black),
                      textAlign: TextAlign.center,
                    ),
                  ),
                  const SizedBox(height: 24),
                  SizedBox(
                    height: 56,
                    child: ElevatedButton(
                      onPressed: () {
                        // Redirecionar para login ou home
                        Navigator.pop(context);
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFFf5c116),
                      ),
                      child: const Text(
                        'Continuar',
                        style: TextStyle(fontSize: 18, color: Colors.black),
                      ),
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
          color: Colors.white.withOpacity(0.9),
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