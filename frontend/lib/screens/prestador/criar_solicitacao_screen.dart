import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../../constants/app_constants.dart';
import '../../constants/categorias.dart';

class CriarSolicitacaoScreen extends StatefulWidget {
  final int clienteId;
  const CriarSolicitacaoScreen({super.key, required this.clienteId});

  @override
  State<CriarSolicitacaoScreen> createState() => _CriarSolicitacaoScreenState();
}

class _CriarSolicitacaoScreenState extends State<CriarSolicitacaoScreen> {
  final _formKey = GlobalKey<FormState>();
  final _descricaoController = TextEditingController();
  final _localizacaoController = TextEditingController();
  bool _isLoading = false;

  String? _categoriaSelecionada;
  String? _subcategoriaSelecionada;
  DateTime? _prazoSelecionado;
  TimeOfDay? _horaSelecionada;

  Future<void> _selecionarData() async {
    final data = await showDatePicker(
      context: context,
      initialDate: DateTime.now().add(const Duration(days: 1)),
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: const ColorScheme.dark(
              primary: Color(0xFFf5c116),
              onPrimary: Colors.black,
              surface: Color(0xFF1a1a1a),
              onSurface: Colors.white,
            ),
          ),
          child: child!,
        );
      },
    );

    if (data != null) {
      setState(() => _prazoSelecionado = data);
    }
  }

  Future<void> _selecionarHora() async {
    final hora = await showTimePicker(
      context: context,
      initialTime: TimeOfDay.now(),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            timePickerTheme: const TimePickerThemeData(
              backgroundColor: Color(0xFF1a1a1a),
              hourMinuteColor: Color(0xFF121212),
              dialBackgroundColor: Color(0xFF121212),
            ),
            colorScheme: const ColorScheme.dark(
              primary: Color(0xFFf5c116),
              onPrimary: Colors.black,
              surface: Color(0xFF1a1a1a),
              onSurface: Colors.white,
            ),
          ),
          child: child!,
        );
      },
    );

    if (hora != null) {
      setState(() => _horaSelecionada = hora);
    }
  }

  Future<void> _criar() async {
    if (!_formKey.currentState!.validate()) return;

    if (_subcategoriaSelecionada == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Selecione a categoria'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      final response = await http.post(
        Uri.parse(
          '${AppConstants.baseUrl}/solicitacoes/criar?cliente_id=${widget.clienteId}',
        ),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'categoria': _subcategoriaSelecionada,
          'descricao': _descricaoController.text,
          'localizacao': _localizacaoController.text,
          'prazo_desejado': _prazoSelecionado != null
              ? '${_prazoSelecionado!.day}/${_prazoSelecionado!.month}/${_prazoSelecionado!.year}'
              : null,
          // Hora desejada apenas informativa por enquanto
          'hora_desejada': _horaSelecionada != null
              ? '${_horaSelecionada!.hour.toString().padLeft(2, '0')}:${_horaSelecionada!.minute.toString().padLeft(2, '0')}'
              : null,
        }),
      );

      if (response.statusCode == 201) {
        if (mounted) Navigator.pop(context, true);
      } else {
        throw Exception('Erro ao criar');
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
        title: const Text('Nova Solicitação'),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            _buildDropdown(
              label: 'Categoria',
              value: _categoriaSelecionada,
              items: Categorias.categoriasComSubcategorias.keys.toList(),
              onChanged: (valor) {
                setState(() {
                  _categoriaSelecionada = valor;
                  _subcategoriaSelecionada = null;
                });
              },
            ),
            if (_categoriaSelecionada != null) ...[
              const SizedBox(height: 16),
              _buildDropdown(
                label: 'Subcategoria',
                value: _subcategoriaSelecionada,
                items: Categorias
                    .categoriasComSubcategorias[_categoriaSelecionada]!,
                onChanged: (valor) {
                  setState(() => _subcategoriaSelecionada = valor);
                },
              ),
            ],
            const SizedBox(height: 16),
            _buildField(
              _descricaoController,
              'Descrição',
              'Descreva o serviço',
              maxLines: 3,
            ),
            _buildField(_localizacaoController, 'Localização', 'Cidade/Bairro'),
            const SizedBox(height: 16),
            _buildDateField(),
            const SizedBox(height: 12),
            _buildTimeField(),
            const SizedBox(height: 24),
            SizedBox(
              height: 56,
              child: ElevatedButton(
                onPressed: _isLoading ? null : _criar,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFFf5c116),
                ),
                child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.black)
                    : const Text(
                        'Solicitar Orçamentos',
                        style: TextStyle(fontSize: 18, color: Colors.black),
                      ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDropdown({
    required String label,
    required String? value,
    required List<String> items,
    required void Function(String?) onChanged,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12),
      decoration: BoxDecoration(
        color: const Color(0xFF1a1a1a),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey[800]!),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          value: value,
          hint: Text(label, style: TextStyle(color: Colors.grey[400])),
          isExpanded: true,
          dropdownColor: const Color(0xFF1a1a1a),
          style: const TextStyle(color: Colors.white, fontSize: 16),
          items: items.map((item) {
            return DropdownMenuItem(value: item, child: Text(item));
          }).toList(),
          onChanged: onChanged,
        ),
      ),
    );
  }

  Widget _buildDateField() {
    return GestureDetector(
      onTap: _selecionarData,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: const Color(0xFF1a1a1a),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: Colors.grey[800]!),
        ),
        child: Row(
          children: [
            const Icon(Icons.calendar_today, color: Color(0xFFf5c116)),
            const SizedBox(width: 12),
            Text(
              _prazoSelecionado == null
                  ? 'Selecionar prazo (opcional)'
                  : '${_prazoSelecionado!.day}/${_prazoSelecionado!.month}/${_prazoSelecionado!.year}',
              style: TextStyle(
                color: _prazoSelecionado == null
                    ? Colors.grey[400]
                    : Colors.white,
                fontSize: 16,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTimeField() {
    return GestureDetector(
      onTap: _selecionarHora,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: const Color(0xFF1a1a1a),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: Colors.grey[800]!),
        ),
        child: Row(
          children: [
            const Icon(Icons.schedule, color: Color(0xFFf5c116)),
            const SizedBox(width: 12),
            Text(
              _horaSelecionada == null
                  ? 'Selecionar horário (opcional)'
                  : '${_horaSelecionada!.hour.toString().padLeft(2, '0')}:${_horaSelecionada!.minute.toString().padLeft(2, '0')}',
              style: TextStyle(
                color: _horaSelecionada == null
                    ? Colors.grey[400]
                    : Colors.white,
                fontSize: 16,
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
    String hint, {
    int maxLines = 1,
    bool required = true,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: TextFormField(
        controller: controller,
        maxLines: maxLines,
        style: const TextStyle(color: Colors.white),
        decoration: InputDecoration(
          labelText: label,
          hintText: hint,
          filled: true,
          fillColor: const Color(0xFF1a1a1a),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
        ),
        validator: (v) =>
            required && (v == null || v.isEmpty) ? 'Campo obrigatório' : null,
      ),
    );
  }
}
