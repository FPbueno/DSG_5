import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../../constants/app_constants.dart';
import '../../constants/categorias.dart';
import '../tipo_usuario_screen.dart';

class SettingsPrestadorScreen extends StatefulWidget {
  final int usuarioId;
  final String nome;

  const SettingsPrestadorScreen({
    super.key,
    required this.usuarioId,
    required this.nome,
  });

  @override
  State<SettingsPrestadorScreen> createState() =>
      _SettingsPrestadorScreenState();
}

class _SettingsPrestadorScreenState extends State<SettingsPrestadorScreen> {
  final List<String> _todasCategorias = Categorias.todasSubcategorias;

  List<String> _categoriasSelecionadas = [];
  double _avaliacaoMedia = 0.0;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _carregarCategorias();
  }

  Future<void> _carregarCategorias() async {
    setState(() => _isLoading = true);

    try {
      final response = await http.get(
        Uri.parse('${AppConstants.baseUrl}/prestadores/${widget.usuarioId}'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _categoriasSelecionadas = List<String>.from(data['categorias'] ?? []);
          _avaliacaoMedia = (data['avaliacao_media'] ?? 0.0).toDouble();
        });
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

  Future<void> _salvarCategorias() async {
    try {
      final response = await http.put(
        Uri.parse('${AppConstants.baseUrl}/prestadores/${widget.usuarioId}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'categorias': _categoriasSelecionadas}),
      );

      if (response.statusCode == 200 && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Áreas atualizadas!'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erro: $e'), backgroundColor: Colors.red),
        );
      }
    }
  }

  Future<void> _logout() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1a1a1a),
        title: const Text('Sair', style: TextStyle(color: Colors.white)),
        content: const Text(
          'Deseja sair da conta?',
          style: TextStyle(color: Colors.grey),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, true),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('Sair'),
          ),
        ],
      ),
    );

    if (confirmed == true && mounted) {
      Navigator.of(context).pushAndRemoveUntil(
        MaterialPageRoute(builder: (_) => const TipoUsuarioScreen()),
        (route) => false,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text('Configurações'),
        automaticallyImplyLeading: false,
      ),
      body: _isLoading
          ? const Center(
              child: CircularProgressIndicator(color: Color(0xFFf5c116)),
            )
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                Card(
                  color: const Color(0xFF1a1a1a),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: [
                        CircleAvatar(
                          radius: 40,
                          backgroundColor: const Color(0xFFf5c116),
                          child: const Icon(
                            Icons.work,
                            size: 40,
                            color: Colors.black,
                          ),
                        ),
                        const SizedBox(height: 16),
                        Text(
                          widget.nome,
                          style: const TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          'Prestador',
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.grey[400],
                          ),
                        ),
                        const SizedBox(height: 12),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(
                              Icons.star,
                              color: Color(0xFFf5c116),
                              size: 24,
                            ),
                            const SizedBox(width: 8),
                            Text(
                              _avaliacaoMedia > 0
                                  ? _avaliacaoMedia.toStringAsFixed(1)
                                  : 'Sem avaliações',
                              style: const TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: Color(0xFFf5c116),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 24),

                Text(
                  'Áreas de Atuação',
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  'Selecione as áreas em que você presta serviço',
                  style: TextStyle(fontSize: 14, color: Colors.grey[400]),
                ),
                const SizedBox(height: 16),

                Card(
                  color: const Color(0xFF1a1a1a),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: _todasCategorias.map((categoria) {
                        final selecionada = _categoriasSelecionadas.contains(
                          categoria,
                        );
                        return FilterChip(
                          label: Text(categoria),
                          selected: selecionada,
                          onSelected: (selected) {
                            setState(() {
                              if (selected) {
                                _categoriasSelecionadas.add(categoria);
                              } else {
                                _categoriasSelecionadas.remove(categoria);
                              }
                            });
                            _salvarCategorias();
                          },
                          selectedColor: const Color(0xFFf5c116),
                          backgroundColor: const Color(0xFF2a2a2a),
                          labelStyle: TextStyle(
                            color: selecionada ? Colors.black : Colors.white,
                            fontWeight: selecionada
                                ? FontWeight.bold
                                : FontWeight.normal,
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                ),
                const SizedBox(height: 24),

                ListTile(
                  tileColor: const Color(0xFF1a1a1a),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  leading: const Icon(Icons.logout, color: Colors.red),
                  title: const Text(
                    'Sair',
                    style: TextStyle(color: Colors.red),
                  ),
                  onTap: _logout,
                ),
              ],
            ),
    );
  }
}
