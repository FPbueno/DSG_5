import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../../constants/app_constants.dart';
import '../../models/orcamento.dart';
import '../../utils/status_colors.dart';

class HistoricoPrestadorScreen extends StatefulWidget {
  final int usuarioId;
  final String nome;

  const HistoricoPrestadorScreen({
    super.key,
    required this.usuarioId,
    required this.nome,
  });

  @override
  State<HistoricoPrestadorScreen> createState() =>
      _HistoricoPrestadorScreenState();
}

class _HistoricoPrestadorScreenState extends State<HistoricoPrestadorScreen> {
  List<Orcamento> _orcamentos = [];
  bool _isLoading = true;
  String _filtro = 'todos';

  @override
  void initState() {
    super.initState();
    _carregarHistorico();
  }

  Future<void> _carregarHistorico() async {
    setState(() => _isLoading = true);

    try {
      final response = await http.get(
        Uri.parse(
          '${AppConstants.baseUrl}/orcamentos/meus-orcamentos?prestador_id=${widget.usuarioId}',
        ),
      );

      if (response.statusCode == 200) {
        final List data = jsonDecode(response.body);
        setState(() {
          _orcamentos = data.map((json) => Orcamento.fromJson(json)).toList();
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

  List<Orcamento> get _orcamentosFiltrados {
    if (_filtro == 'todos') return _orcamentos;
    return _orcamentos.where((o) => o.status == _filtro).toList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'Meus Orçamentos',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.refresh, color: Color(0xFFf5c116)),
                    onPressed: _carregarHistorico,
                  ),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Column(
                children: [
                  Row(
                    children: [
                      Expanded(child: _buildFiltroChip('Todos', 'todos')),
                      const SizedBox(width: 8),
                      Expanded(
                        child: _buildFiltroChip('Aguard.', 'aguardando'),
                      ),
                      const SizedBox(width: 8),
                      Expanded(child: _buildFiltroChip('Aceitos', 'aceito')),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      Expanded(
                        child: _buildFiltroChip('Recusados', 'recusado'),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: _buildFiltroChip('Realizados', 'realizado'),
                      ),
                      const SizedBox(width: 8),
                      Expanded(child: Container()),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            Expanded(child: _buildBody()),
          ],
        ),
      ),
    );
  }

  Widget _buildFiltroChip(String label, String valor) {
    final ativo = _filtro == valor;
    return GestureDetector(
      onTap: () => setState(() => _filtro = valor),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10),
        decoration: BoxDecoration(
          color: ativo ? const Color(0xFFf5c116) : const Color(0xFF1a1a1a),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Center(
          child: Text(
            label,
            style: TextStyle(
              color: ativo ? Colors.black : Colors.white,
              fontWeight: ativo ? FontWeight.bold : FontWeight.normal,
              fontSize: 12,
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(
        child: CircularProgressIndicator(color: Color(0xFFf5c116)),
      );
    }

    final orcamentosFiltrados = _orcamentosFiltrados;

    if (orcamentosFiltrados.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.work_history, size: 80, color: Colors.grey[700]),
            const SizedBox(height: 16),
            Text(
              'Nenhum orçamento enviado',
              style: TextStyle(fontSize: 18, color: Colors.grey[400]),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _carregarHistorico,
      color: const Color(0xFFf5c116),
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: orcamentosFiltrados.length,
        itemBuilder: (_, i) => _buildCard(orcamentosFiltrados[i]),
      ),
    );
  }

  Widget _buildCard(Orcamento orc) {
    return Card(
      color: const Color(0xFF1a1a1a),
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'R\$ ${orc.valorProposto.toStringAsFixed(2)}',
                  style: const TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFFf5c116),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: _getStatusColor(orc.status).withValues(alpha: 0.2),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    orc.statusFormatado,
                    style: TextStyle(
                      color: _getStatusColor(orc.status),
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              'Prazo: ${orc.prazoExecucao}',
              style: TextStyle(color: Colors.grey[400]),
            ),
            if (orc.observacoes != null && orc.observacoes!.isNotEmpty) ...[
              const SizedBox(height: 4),
              Text(
                orc.observacoes!,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(color: Colors.grey[300]),
              ),
            ],
            const SizedBox(height: 12),
            if (orc.status == 'aceito')
              SizedBox(
                width: double.infinity,
                child: OutlinedButton(
                  onPressed: () => _marcarRealizado(orc.id),
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: Color(0xFFf5c116)),
                    foregroundColor: const Color(0xFFf5c116),
                  ),
                  child: const Text('Marcar realizado'),
                ),
              ),
            if (orc.status == 'aguardando')
              SizedBox(
                width: double.infinity,
                child: OutlinedButton(
                  onPressed: () => _confirmarDeletar(orc.id),
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: Colors.red),
                    foregroundColor: Colors.red,
                  ),
                  child: const Text('Deletar orçamento'),
                ),
              ),
          ],
        ),
      ),
    );
  }

  Color _getStatusColor(String status) {
    return StatusColors.getOrcamentoColor(status);
  }

  Future<void> _marcarRealizado(int orcamentoId) async {
    try {
      final resp = await http.put(
        Uri.parse(
          '${AppConstants.baseUrl}/orcamentos/$orcamentoId/realizado?prestador_id=${widget.usuarioId}',
        ),
      );
      if (!mounted) return;
      if (resp.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Marcado como realizado'),
            backgroundColor: Colors.green,
          ),
        );
        _carregarHistorico();
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Erro (${resp.statusCode})'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Erro: $e'), backgroundColor: Colors.red),
      );
    }
  }

  Future<void> _confirmarDeletar(int orcamentoId) async {
    final confirmar = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF1a1a1a),
        title: const Text(
          'Deletar Orçamento',
          style: TextStyle(color: Colors.white),
        ),
        content: const Text(
          'Tem certeza que deseja deletar este orçamento? Esta ação não pode ser desfeita.',
          style: TextStyle(color: Colors.grey),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('Cancelar', style: TextStyle(color: Colors.grey)),
          ),
          TextButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Deletar', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );

    if (confirmar == true) {
      await _deletarOrcamento(orcamentoId);
    }
  }

  Future<void> _deletarOrcamento(int orcamentoId) async {
    try {
      final resp = await http.delete(
        Uri.parse(
          '${AppConstants.baseUrl}/orcamentos/$orcamentoId?prestador_id=${widget.usuarioId}',
        ),
      );
      if (!mounted) return;
      if (resp.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Orçamento deletado'),
            backgroundColor: Colors.green,
          ),
        );
        _carregarHistorico();
      } else {
        final erro = jsonDecode(resp.body)['detail'] ?? 'Erro desconhecido';
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(erro), backgroundColor: Colors.red),
        );
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Erro: $e'), backgroundColor: Colors.red),
      );
    }
  }
}
