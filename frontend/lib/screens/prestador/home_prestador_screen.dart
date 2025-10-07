import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../../constants/app_constants.dart';
import '../../models/orcamento.dart';
import '../../utils/status_colors.dart';

class HomePrestadorScreen extends StatefulWidget {
  final int usuarioId;
  final String nome;

  const HomePrestadorScreen({
    super.key,
    required this.usuarioId,
    required this.nome,
  });

  @override
  State<HomePrestadorScreen> createState() => _HomePrestadorScreenState();
}

class _HomePrestadorScreenState extends State<HomePrestadorScreen> {
  List<Orcamento> _orcamentos = [];
  bool _isLoading = true;
  String _filtro = 'todos';

  @override
  void initState() {
    super.initState();
    _carregarOrcamentos();
  }

  List<Orcamento> get _orcamentosFiltrados {
    List<Orcamento> lista;
    if (_filtro == 'todos') {
      lista = _orcamentos;
    } else {
      lista = _orcamentos.where((o) => o.status == _filtro).toList();
    }

    // Sempre ordena: aguardando primeiro, depois aceito, depois outros
    lista.sort((a, b) {
      const ordem = {
        'aguardando': 0,
        'aceito': 1,
        'realizado': 2,
        'recusado': 3,
      };
      return (ordem[a.status] ?? 99).compareTo(ordem[b.status] ?? 99);
    });

    return lista;
  }

  Future<void> _carregarOrcamentos() async {
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
                  Text(
                    'Olá, ${widget.nome}',
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.refresh, color: Color(0xFFf5c116)),
                    onPressed: _carregarOrcamentos,
                  ),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Row(
                children: [
                  Expanded(child: _buildFiltroChip('Todos', 'todos')),
                  const SizedBox(width: 8),
                  Expanded(child: _buildFiltroChip('Aguard.', 'aguardando')),
                  const SizedBox(width: 8),
                  Expanded(child: _buildFiltroChip('Aceitos', 'aceito')),
                  const SizedBox(width: 8),
                  Expanded(child: _buildFiltroChip('Realizados', 'realizado')),
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
    return _isLoading
        ? const Center(
            child: CircularProgressIndicator(color: Color(0xFFf5c116)),
          )
        : _orcamentosFiltrados.isEmpty
        ? Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.work_off, size: 80, color: Colors.grey[700]),
                const SizedBox(height: 16),
                Text(
                  _filtro == 'todos'
                      ? 'Nenhum orçamento enviado'
                      : 'Nenhum orçamento ${_formatarStatus(_filtro).toLowerCase()}',
                  style: TextStyle(fontSize: 18, color: Colors.grey[400]),
                ),
              ],
            ),
          )
        : RefreshIndicator(
            onRefresh: _carregarOrcamentos,
            color: const Color(0xFFf5c116),
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _orcamentosFiltrados.length,
              itemBuilder: (_, i) => _buildCard(_orcamentosFiltrados[i]),
            ),
          );
  }

  Widget _buildCard(Orcamento orc) {
    return Card(
      color: const Color(0xFF1a1a1a),
      margin: const EdgeInsets.only(bottom: 16),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        title: Text(
          orc.categoria ?? 'Sem categoria',
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 8),
            Text(
              orc.descricao ?? 'Sem descrição',
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: TextStyle(color: Colors.grey[400]),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: _getStatusColor(orc.status).withValues(alpha: 0.2),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    _formatarStatus(orc.status),
                    style: TextStyle(
                      color: _getStatusColor(orc.status),
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Icon(Icons.attach_money, size: 16, color: Colors.grey[500]),
                const SizedBox(width: 4),
                Text(
                  'R\$ ${orc.valorProposto.toStringAsFixed(2)}',
                  style: TextStyle(color: Colors.grey[500], fontSize: 12),
                ),
              ],
            ),
          ],
        ),
        trailing: _getTrailingIcon(orc.status, orc.id),
        onTap: () => _mostrarDetalhes(orc),
      ),
    );
  }

  Widget _getTrailingIcon(String status, int orcamentoId) {
    switch (status) {
      case 'aceito':
        return IconButton(
          icon: const Icon(Icons.check_circle, color: Color(0xFFf5c116)),
          onPressed: () => _marcarRealizado(orcamentoId),
        );
      case 'realizado':
        return const Icon(Icons.done_all, color: Colors.green);
      default:
        return const Icon(Icons.arrow_forward_ios, color: Color(0xFFf5c116));
    }
  }

  String _formatarStatus(String status) {
    switch (status) {
      case 'aguardando':
        return 'Aguardando';
      case 'aceito':
        return 'Aceito';
      case 'recusado':
        return 'Recusado';
      case 'realizado':
        return 'Realizado';
      default:
        return status;
    }
  }

  Color _getStatusColor(String status) {
    return StatusColors.getOrcamentoColor(status);
  }

  void _mostrarDetalhes(Orcamento orc) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF1a1a1a),
        title: Text(
          orc.categoria ?? 'Sem categoria',
          style: const TextStyle(color: Colors.white),
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              orc.descricao ?? 'Sem descrição',
              style: TextStyle(color: Colors.grey[400]),
            ),
            const SizedBox(height: 16),
            Text(
              'Valor: R\$ ${orc.valorProposto.toStringAsFixed(2)}',
              style: const TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Prazo: ${orc.prazoExecucao}',
              style: TextStyle(color: Colors.grey[400]),
            ),
            if (orc.observacoes != null && orc.observacoes!.isNotEmpty) ...[
              const SizedBox(height: 8),
              Text(
                'Observações: ${orc.observacoes}',
                style: TextStyle(color: Colors.grey[400]),
              ),
            ],
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(
                color: _getStatusColor(orc.status).withValues(alpha: 0.2),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                _formatarStatus(orc.status),
                style: TextStyle(
                  color: _getStatusColor(orc.status),
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ],
        ),
        actions: [
          if (orc.status == 'aceito')
            TextButton(
              onPressed: () => _marcarRealizado(orc.id),
              child: const Text(
                'Marcar como Realizado',
                style: TextStyle(color: Color(0xFFf5c116)),
              ),
            ),
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Fechar', style: TextStyle(color: Colors.grey)),
          ),
        ],
      ),
    );
  }

  Future<void> _marcarRealizado(int orcamentoId) async {
    try {
      final response = await http.put(
        Uri.parse(
          '${AppConstants.baseUrl}/orcamentos/$orcamentoId/realizado?prestador_id=${widget.usuarioId}',
        ),
      );

      if (!mounted) return;
      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Orçamento marcado como realizado!'),
            backgroundColor: Colors.green,
          ),
        );
        _carregarOrcamentos();
        Navigator.pop(context); // Fecha o dialog
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Erro ao marcar como realizado'),
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
}
