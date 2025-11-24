import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../../constants/app_constants.dart';
import '../../models/orcamento.dart';
import '../../models/solicitacao.dart';

class DetalhesSolicitacaoPrestadorScreen extends StatefulWidget {
  final int solicitacaoId;
  final int prestadorId;

  const DetalhesSolicitacaoPrestadorScreen({
    super.key,
    required this.solicitacaoId,
    required this.prestadorId,
  });

  @override
  State<DetalhesSolicitacaoPrestadorScreen> createState() =>
      _DetalhesSolicitacaoPrestadorScreenState();
}

class _DetalhesSolicitacaoPrestadorScreenState
    extends State<DetalhesSolicitacaoPrestadorScreen> {
  Solicitacao? _solicitacao;
  LimitesPreco? _limites;
  final _valorController = TextEditingController();
  final _obsController = TextEditingController();
  DateTime? _prazoSelecionado;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _carregarDados();
  }

  Future<void> _carregarDados() async {
    setState(() => _isLoading = true);

    try {
      // Busca solicitação
      final solResp = await http.get(
        Uri.parse(
          '${AppConstants.baseUrl}/solicitacoes/${widget.solicitacaoId}',
        ),
      );
      if (solResp.statusCode == 200) {
        setState(
          () => _solicitacao = Solicitacao.fromJson(jsonDecode(solResp.body)),
        );
      }

      // Busca limites ML
      final limResp = await http.get(
        Uri.parse(
          '${AppConstants.baseUrl}/orcamentos/calcular-limites/${widget.solicitacaoId}',
        ),
      );
      if (limResp.statusCode == 200) {
        setState(() {
          _limites = LimitesPreco.fromJson(jsonDecode(limResp.body));
          _valorController.text = _limites!.valorSugerido.toStringAsFixed(2);
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

  Future<void> _selecionarPrazo() async {
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

  Future<void> _enviarOrcamento() async {
    if (_valorController.text.isEmpty || _prazoSelecionado == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Preencha valor e prazo'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    final valor = double.tryParse(_valorController.text);
    if (valor == null) return;

    if (_limites != null &&
        (valor < _limites!.valorMinimo || valor > _limites!.valorMaximo)) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Valor deve estar entre R\$ ${_limites!.valorMinimo.toStringAsFixed(2)} e R\$ ${_limites!.valorMaximo.toStringAsFixed(2)}',
          ),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    try {
      final response = await http.post(
        Uri.parse(
          '${AppConstants.baseUrl}/orcamentos/criar?prestador_id=${widget.prestadorId}',
        ),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'solicitacao_id': widget.solicitacaoId,
          'valor_proposto': valor,
          'prazo_execucao':
              '${_prazoSelecionado!.day}/${_prazoSelecionado!.month}/${_prazoSelecionado!.year}',
          'observacoes': _obsController.text,
        }),
      );

      if (response.statusCode == 201 && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Orçamento enviado!'),
            backgroundColor: Colors.green,
          ),
        );
        Navigator.pop(context, true);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erro: $e'), backgroundColor: Colors.red),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text('Enviar Orçamento'),
      ),
      body: _isLoading
          ? const Center(
              child: CircularProgressIndicator(color: Color(0xFFf5c116)),
            )
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                if (_solicitacao != null) ...[
                  _buildInfoCard(),
                  const SizedBox(height: 16),
                ],
                if (_limites != null) ...[
                  _buildLimitesCard(),
                  const SizedBox(height: 16),
                ],
                _buildFormulario(),
                const SizedBox(height: 24),
                SizedBox(
                  height: 56,
                  child: ElevatedButton(
                    onPressed: _enviarOrcamento,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFFf5c116),
                    ),
                    child: const Text(
                      'Enviar Orçamento',
                      style: TextStyle(fontSize: 18, color: Colors.black),
                    ),
                  ),
                ),
              ],
            ),
    );
  }

  Widget _buildInfoCard() {
    return Card(
      color: const Color(0xFF1a1a1a),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              _solicitacao!.categoria,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              _solicitacao!.descricao,
              style: TextStyle(color: Colors.grey[300]),
            ),
            const SizedBox(height: 8),
            Text(
              'Local: ${_solicitacao!.localizacao}',
              style: TextStyle(color: Colors.grey[400]),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLimitesCard() {
    return Card(
      color: const Color(0xFF1a1a1a),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Orientação de Preço (ML)',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: Color(0xFFf5c116),
              ),
            ),
            const SizedBox(height: 12),
            Text(
              'Sugerido: R\$ ${_limites!.valorSugerido.toStringAsFixed(2)}',
              style: const TextStyle(color: Colors.white, fontSize: 18),
            ),
            Text(
              'Mínimo: R\$ ${_limites!.valorMinimo.toStringAsFixed(2)} | Máximo: R\$ ${_limites!.valorMaximo.toStringAsFixed(2)}',
              style: TextStyle(color: Colors.grey[400]),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFormulario() {
    return Column(
      children: [
        _buildField(_valorController, 'Valor (R\$)', TextInputType.number),
        _buildDateField(),
        const SizedBox(height: 16),
        _buildField(
          _obsController,
          'Observações',
          TextInputType.text,
          3,
          false,
        ),
      ],
    );
  }

  Widget _buildDateField() {
    return GestureDetector(
      onTap: _selecionarPrazo,
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
                  ? 'Selecionar prazo de execução'
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

  Widget _buildField(
    TextEditingController controller,
    String label, [
    TextInputType? type,
    int maxLines = 1,
    bool required = true,
  ]) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: TextFormField(
        controller: controller,
        keyboardType: type,
        maxLines: maxLines,
        style: const TextStyle(color: Colors.white),
        decoration: InputDecoration(
          labelText: label,
          filled: true,
          fillColor: const Color(0xFF1a1a1a),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
        ),
      ),
    );
  }
}
