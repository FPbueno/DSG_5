import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../../constants/app_constants.dart';
import '../../models/solicitacao.dart';
import '../../models/orcamento.dart';
import '../../utils/status_colors.dart';

class HistoricoClienteScreen extends StatefulWidget {
  final int usuarioId;
  final String nome;

  const HistoricoClienteScreen({
    super.key,
    required this.usuarioId,
    required this.nome,
  });

  @override
  State<HistoricoClienteScreen> createState() => _HistoricoClienteScreenState();
}

class _HistoricoClienteScreenState extends State<HistoricoClienteScreen> {
  List<Solicitacao> _solicitacoes = [];
  List<Orcamento> _orcamentosRealizados = [];
  bool _isLoading = true;
  String _filtro = 'todas';

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
          '${AppConstants.baseUrl}/solicitacoes/minhas?cliente_id=${widget.usuarioId}',
        ),
      );

      if (response.statusCode == 200) {
        final List data = jsonDecode(response.body);
        setState(() {
          _solicitacoes = data
              .map((json) => Solicitacao.fromJson(json))
              .toList();
        });
      }

      final orcResp = await http.get(
        Uri.parse(
          '${AppConstants.baseUrl}/orcamentos/cliente/${widget.usuarioId}/realizados',
        ),
      );

      if (orcResp.statusCode == 200) {
        final List orcData = jsonDecode(orcResp.body);
        setState(() {
          _orcamentosRealizados = orcData
              .map((json) => Orcamento.fromJson(json))
              .toList();
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

  List<Solicitacao> get _solicitacoesFiltradas {
    if (_filtro == 'todas') return _solicitacoes;
    if (_filtro == 'realizados' || _filtro == 'fechada') {
      return []; // Realizados e fechadas são mostrados separadamente
    }
    return _solicitacoes.where((s) => s.status == _filtro).toList();
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
                    'Histórico',
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
                      Expanded(child: _buildFiltroChip('Todas', 'todas')),
                      const SizedBox(width: 8),
                      Expanded(
                        child: _buildFiltroChip('Aguard.', 'com_orcamentos'),
                      ),
                      const SizedBox(width: 8),
                      Expanded(child: _buildFiltroChip('Fechadas', 'fechada')),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      Expanded(
                        child: _buildFiltroChip('Canceladas', 'cancelada'),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: _buildFiltroChip('Realizados', 'realizados'),
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

    if (_filtro == 'realizados' || _filtro == 'fechada') {
      if (_orcamentosRealizados.isEmpty) {
        return Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.check_circle, size: 80, color: Colors.grey[700]),
              const SizedBox(height: 16),
              Text(
                _filtro == 'realizados'
                    ? 'Nenhum serviço realizado'
                    : 'Nenhuma solicitação fechada',
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
          itemCount: _orcamentosRealizados.length,
          itemBuilder: (_, index) =>
              _buildOrcamentoRealizadoCard(_orcamentosRealizados[index]),
        ),
      );
    }

    final solicitacoesFiltradas = _solicitacoesFiltradas;

    if (solicitacoesFiltradas.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.history, size: 80, color: Colors.grey[700]),
            const SizedBox(height: 16),
            Text(
              'Nenhuma solicitação',
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
        itemCount: solicitacoesFiltradas.length,
        itemBuilder: (_, index) => _buildCard(solicitacoesFiltradas[index]),
      ),
    );
  }

  Widget _buildCard(Solicitacao sol) {
    return Card(
      color: const Color(0xFF1a1a1a),
      margin: const EdgeInsets.only(bottom: 16),
      child: InkWell(
        onTap: () => _mostrarDetalhesSolicitacao(sol),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Text(
                      sol.categoria,
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ),
                  const Icon(
                    Icons.arrow_forward_ios,
                    color: Color(0xFFf5c116),
                    size: 16,
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Text(
                sol.descricao,
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
                      color: _getStatusColor(sol.status).withValues(alpha: 0.2),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      sol.statusFormatado,
                      style: TextStyle(
                        color: _getStatusColor(sol.status),
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Icon(Icons.description, size: 16, color: Colors.grey[500]),
                  const SizedBox(width: 4),
                  Text(
                    '${sol.quantidadeOrcamentos ?? 0} orçamentos',
                    style: TextStyle(color: Colors.grey[500], fontSize: 12),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _mostrarDetalhesSolicitacao(Solicitacao sol) async {
    await showModalBottomSheet(
      context: context,
      backgroundColor: Colors.black,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => DraggableScrollableSheet(
        initialChildSize: 0.7,
        minChildSize: 0.5,
        maxChildSize: 0.9,
        expand: false,
        builder: (_, scrollController) => SingleChildScrollView(
          controller: scrollController,
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'Detalhes da Solicitação',
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close, color: Colors.white),
                    onPressed: () => Navigator.pop(ctx),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              Card(
                color: const Color(0xFF1a1a1a),
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        sol.categoria,
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 12),
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 6,
                        ),
                        decoration: BoxDecoration(
                          color: _getStatusColor(
                            sol.status,
                          ).withValues(alpha: 0.2),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          sol.statusFormatado,
                          style: TextStyle(
                            color: _getStatusColor(sol.status),
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),
                      _buildInfoRow('Descrição', sol.descricao),
                      const SizedBox(height: 16),
                      _buildInfoRow('Localização', sol.localizacao),
                      if (sol.prazoDesejado != null &&
                          sol.prazoDesejado!.isNotEmpty) ...[
                        const SizedBox(height: 16),
                        _buildInfoRow('Prazo Desejado', sol.prazoDesejado!),
                      ],
                      if (sol.informacoesAdicionais != null &&
                          sol.informacoesAdicionais!.isNotEmpty) ...[
                        const SizedBox(height: 16),
                        _buildInfoRow(
                          'Informações Adicionais',
                          sol.informacoesAdicionais!,
                        ),
                      ],
                      const SizedBox(height: 16),
                      Row(
                        children: [
                          Icon(
                            Icons.description,
                            size: 18,
                            color: Colors.grey[400],
                          ),
                          const SizedBox(width: 8),
                          Text(
                            '${sol.quantidadeOrcamentos ?? 0} orçamento(s) recebido(s)',
                            style: TextStyle(
                              color: Colors.grey[300],
                              fontSize: 14,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Color _getStatusColor(String status) {
    return StatusColors.getSolicitacaoColor(status);
  }

  Widget _buildOrcamentoRealizadoCard(Orcamento orc) {
    return Card(
      color: const Color(0xFF1a1a1a),
      margin: const EdgeInsets.only(bottom: 16),
      child: InkWell(
        onTap: () => _mostrarDetalhesOrcamento(orc),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              const Icon(Icons.check_circle, color: Colors.green, size: 40),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      orc.prestadorNome ?? 'Prestador',
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'R\$ ${orc.valorProposto.toStringAsFixed(2)}',
                      style: const TextStyle(
                        fontSize: 16,
                        color: Color(0xFFf5c116),
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Prazo: ${orc.prazoExecucao}',
                      style: TextStyle(color: Colors.grey[400], fontSize: 12),
                    ),
                    const SizedBox(height: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 4,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.green.withValues(alpha: 0.2),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        orc.jaAvaliado ? 'AVALIADO' : 'REALIZADO',
                        style: TextStyle(
                          color: orc.jaAvaliado ? Colors.amber : Colors.green,
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const Icon(
                Icons.arrow_forward_ios,
                color: Color(0xFFf5c116),
                size: 20,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _mostrarDetalhesOrcamento(Orcamento orc) async {
    await showModalBottomSheet(
      context: context,
      backgroundColor: Colors.black,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => DraggableScrollableSheet(
        initialChildSize: 0.7,
        minChildSize: 0.5,
        maxChildSize: 0.9,
        expand: false,
        builder: (_, scrollController) => SingleChildScrollView(
          controller: scrollController,
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'Detalhes do Serviço',
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close, color: Colors.white),
                    onPressed: () => Navigator.pop(ctx),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              Card(
                color: const Color(0xFF1a1a1a),
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(
                            Icons.check_circle,
                            color: Colors.green,
                            size: 30,
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Text(
                              orc.prestadorNome ?? 'Prestador',
                              style: const TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                          ),
                        ],
                      ),
                      if (orc.prestadorAvaliacao != null) ...[
                        const SizedBox(height: 8),
                        Row(
                          children: [
                            const Icon(
                              Icons.star,
                              color: Color(0xFFf5c116),
                              size: 18,
                            ),
                            const SizedBox(width: 4),
                            Text(
                              orc.prestadorAvaliacao!.toStringAsFixed(1),
                              style: const TextStyle(color: Colors.white),
                            ),
                          ],
                        ),
                      ],
                      const SizedBox(height: 20),
                      const Text(
                        'Valor',
                        style: TextStyle(color: Colors.grey, fontSize: 14),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'R\$ ${orc.valorProposto.toStringAsFixed(2)}',
                        style: const TextStyle(
                          fontSize: 32,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFFf5c116),
                        ),
                      ),
                      const SizedBox(height: 20),
                      _buildInfoRow('Prazo de Execução', orc.prazoExecucao),
                      if (orc.observacoes != null &&
                          orc.observacoes!.isNotEmpty) ...[
                        const SizedBox(height: 16),
                        _buildInfoRow('Observações', orc.observacoes!),
                      ],
                      if (orc.condicoes != null &&
                          orc.condicoes!.isNotEmpty) ...[
                        const SizedBox(height: 16),
                        _buildInfoRow('Condições', orc.condicoes!),
                      ],
                      const SizedBox(height: 20),
                      if (orc.status == 'realizado' && !orc.jaAvaliado)
                        SizedBox(
                          width: double.infinity,
                          child: OutlinedButton(
                            onPressed: () => _avaliar(orc, ctx),
                            style: OutlinedButton.styleFrom(
                              side: const BorderSide(color: Color(0xFFf5c116)),
                              foregroundColor: const Color(0xFFf5c116),
                              padding: const EdgeInsets.symmetric(vertical: 14),
                            ),
                            child: const Text('Avaliar serviço'),
                          ),
                        )
                      else if (orc.status == 'realizado' && orc.jaAvaliado)
                        Container(
                          width: double.infinity,
                          padding: const EdgeInsets.symmetric(vertical: 14),
                          decoration: BoxDecoration(
                            color: Colors.grey.withValues(alpha: 0.2),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: const Text(
                            'Já avaliado',
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              color: Colors.grey,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _avaliar(Orcamento orc, BuildContext bottomSheetContext) async {
    int estrelas = 0;
    final comentarioCtrl = TextEditingController();

    await showDialog(
      context: context,
      builder: (dialogContext) => StatefulBuilder(
        builder: (ctx, setDialogState) => AlertDialog(
          backgroundColor: const Color(0xFF1a1a1a),
          title: const Text(
            'Avaliar serviço',
            style: TextStyle(
              color: Colors.white,
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(5, (i) {
                  final idx = i + 1;
                  final ativo = estrelas >= idx;
                  return IconButton(
                    onPressed: () => setDialogState(() => estrelas = idx),
                    icon: Icon(
                      Icons.star,
                      color: ativo ? const Color(0xFFf5c116) : Colors.grey[700],
                      size: 32,
                    ),
                  );
                }),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: comentarioCtrl,
                maxLines: 3,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  hintText: 'Comentário (opcional)',
                  hintStyle: TextStyle(color: Colors.grey[500]),
                  filled: true,
                  fillColor: const Color(0xFF121212),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: BorderSide.none,
                  ),
                ),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(dialogContext),
              child: const Text(
                'Cancelar',
                style: TextStyle(color: Colors.grey),
              ),
            ),
            TextButton(
              onPressed: () async {
                if (estrelas < 1) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Selecione de 1 a 5 estrelas'),
                    ),
                  );
                  return;
                }
                try {
                  final resp = await http.post(
                    Uri.parse('${AppConstants.baseUrl}/avaliacoes/'),
                    headers: {'Content-Type': 'application/json'},
                    body: jsonEncode({
                      'orcamento_id': orc.id,
                      'cliente_id': widget.usuarioId,
                      'prestador_id': orc.prestadorId,
                      'estrelas': estrelas,
                      'comentario': comentarioCtrl.text,
                    }),
                  );
                  if (!mounted) return;
                  if (resp.statusCode == 201) {
                    if (dialogContext.mounted) Navigator.pop(dialogContext);
                    if (bottomSheetContext.mounted) {
                      Navigator.pop(bottomSheetContext);
                    }
                    await _carregarHistorico();
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('Avaliação enviada!'),
                          backgroundColor: Colors.green,
                        ),
                      );
                    }
                  }
                } catch (e) {
                  if (!mounted) return;
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text('Erro: $e'),
                      backgroundColor: Colors.red,
                    ),
                  );
                }
              },
              child: const Text(
                'Enviar',
                style: TextStyle(color: Color(0xFFf5c116)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(color: Colors.grey, fontSize: 14)),
        const SizedBox(height: 4),
        Text(value, style: const TextStyle(color: Colors.white, fontSize: 16)),
      ],
    );
  }
}
