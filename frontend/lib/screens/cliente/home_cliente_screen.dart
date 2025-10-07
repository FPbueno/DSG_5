import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../../constants/app_constants.dart';
import '../../models/solicitacao.dart';
import '../../utils/status_colors.dart';
import '../prestador/criar_solicitacao_screen.dart';

const _primaryColor = Color(0xFFf5c116);
const _cardColor = Color(0xFF1a1a1a);
const _cardDarkerColor = Color(0xFF121212);

class HomeClienteScreen extends StatefulWidget {
  final int usuarioId;
  final String nome;

  const HomeClienteScreen({
    super.key,
    required this.usuarioId,
    required this.nome,
  });

  @override
  State<HomeClienteScreen> createState() => _HomeClienteScreenState();
}

class _HomeClienteScreenState extends State<HomeClienteScreen> {
  List<Solicitacao> _solicitacoes = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _carregarSolicitacoes();
  }

  Future<void> _carregarSolicitacoes() async {
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
                    icon: const Icon(Icons.refresh, color: _primaryColor),
                    onPressed: _carregarSolicitacoes,
                  ),
                ],
              ),
            ),
            Expanded(child: _buildBody()),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: _primaryColor,
        foregroundColor: Colors.black,
        onPressed: () async {
          final result = await Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) =>
                  CriarSolicitacaoScreen(clienteId: widget.usuarioId),
            ),
          );
          if (result == true) _carregarSolicitacoes();
        },
        icon: const Icon(Icons.add),
        label: const Text('Nova Solicitação'),
      ),
    );
  }

  Widget _buildBody() {
    return _isLoading
        ? const Center(child: CircularProgressIndicator(color: _primaryColor))
        : _solicitacoes.isEmpty
        ? Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.search_off, size: 80, color: Colors.grey[700]),
                const SizedBox(height: 16),
                Text(
                  'Nenhuma solicitação ainda',
                  style: TextStyle(fontSize: 18, color: Colors.grey[400]),
                ),
              ],
            ),
          )
        : RefreshIndicator(
            onRefresh: _carregarSolicitacoes,
            color: _primaryColor,
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _solicitacoes.length,
              itemBuilder: (_, index) =>
                  _buildSolicitacaoCard(_solicitacoes[index]),
            ),
          );
  }

  Widget _buildSolicitacaoCard(Solicitacao sol) {
    final podeDeltar = sol.status != 'fechada';

    return Card(
      color: _cardColor,
      margin: const EdgeInsets.only(bottom: 16),
      child: InkWell(
        onTap: () => _mostrarOrcamentos(sol),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
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
                  if (podeDeltar)
                    IconButton(
                      icon: const Icon(
                        Icons.delete,
                        color: Colors.red,
                        size: 20,
                      ),
                      onPressed: () => _confirmarDeletar(sol.id),
                      padding: EdgeInsets.zero,
                      constraints: const BoxConstraints(),
                    ),
                  const SizedBox(width: 8),
                  const Icon(
                    Icons.arrow_forward_ios,
                    color: _primaryColor,
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

  Color _getStatusColor(String status) {
    return StatusColors.getSolicitacaoColor(status);
  }

  Future<void> _confirmarDeletar(int solicitacaoId) async {
    final confirmar = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: _cardColor,
        title: const Text(
          'Deletar Solicitação',
          style: TextStyle(color: Colors.white),
        ),
        content: const Text(
          'Tem certeza que deseja deletar esta solicitação? Todos os orçamentos recebidos também serão deletados. Esta ação não pode ser desfeita.',
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
      await _deletarSolicitacao(solicitacaoId);
    }
  }

  Future<void> _deletarSolicitacao(int solicitacaoId) async {
    try {
      final resp = await http.delete(
        Uri.parse(
          '${AppConstants.baseUrl}/solicitacoes/$solicitacaoId?cliente_id=${widget.usuarioId}',
        ),
      );
      if (!mounted) return;
      if (resp.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Solicitação deletada'),
            backgroundColor: Colors.green,
          ),
        );
        _carregarSolicitacoes();
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

  Future<void> _mostrarOrcamentos(Solicitacao sol) async {
    // Carrega orçamentos
    List<dynamic> orcamentos = [];
    bool isLoading = true;

    await showModalBottomSheet(
      context: context,
      backgroundColor: Colors.black,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (modalContext) => StatefulBuilder(
        builder: (stfContext, setModalState) {
          if (isLoading) {
            // Carrega orçamentos
            http
                .get(
                  Uri.parse(
                    '${AppConstants.baseUrl}/orcamentos/solicitacao/${sol.id}?cliente_id=${widget.usuarioId}',
                  ),
                )
                .then((response) {
                  if (response.statusCode == 200) {
                    final List data = jsonDecode(response.body);
                    setModalState(() {
                      orcamentos = data;
                      isLoading = false;
                    });
                  } else {
                    setModalState(() => isLoading = false);
                  }
                })
                .catchError((_) {
                  setModalState(() => isLoading = false);
                });
          }

          return DraggableScrollableSheet(
            initialChildSize: 0.9,
            minChildSize: 0.5,
            maxChildSize: 0.95,
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
                      Expanded(
                        child: Text(
                          'Orçamentos - ${sol.categoria}',
                          style: const TextStyle(
                            fontSize: 22,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                      ),
                      IconButton(
                        icon: const Icon(Icons.close, color: Colors.white),
                        onPressed: () {
                          Navigator.pop(modalContext);
                          _carregarSolicitacoes();
                        },
                      ),
                    ],
                  ),
                  const SizedBox(height: 20),
                  if (isLoading)
                    const Center(
                      child: CircularProgressIndicator(color: _primaryColor),
                    )
                  else if (orcamentos.isEmpty)
                    Center(
                      child: Padding(
                        padding: const EdgeInsets.all(40),
                        child: Text(
                          'Aguardando orçamentos...',
                          style: TextStyle(
                            color: Colors.grey[400],
                            fontSize: 16,
                          ),
                        ),
                      ),
                    )
                  else
                    ...orcamentos.map(
                      (orc) => _buildOrcamentoCompleto(
                        orc,
                        modalContext,
                        setModalState,
                      ),
                    ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildOrcamentoCompleto(
    dynamic orc,
    BuildContext modalContext,
    StateSetter setModalState,
  ) {
    return Card(
      color: _cardColor,
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  orc['prestador_nome'] ?? 'Prestador',
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: _getOrcamentoStatusColor(
                      orc['status'],
                    ).withValues(alpha: 0.2),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    _formatarStatus(orc['status']),
                    style: TextStyle(
                      color: _getOrcamentoStatusColor(orc['status']),
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
            if (orc['prestador_avaliacao'] != null) ...[
              const SizedBox(height: 8),
              Row(
                children: [
                  const Icon(Icons.star, color: _primaryColor, size: 18),
                  const SizedBox(width: 4),
                  Text(
                    orc['prestador_avaliacao'].toStringAsFixed(1),
                    style: const TextStyle(color: Colors.white),
                  ),
                ],
              ),
            ],
            const SizedBox(height: 20),
            const Text(
              'Valor Proposto',
              style: TextStyle(color: Colors.grey, fontSize: 14),
            ),
            const SizedBox(height: 8),
            Text(
              'R\$ ${orc['valor_proposto'].toStringAsFixed(2)}',
              style: const TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: _primaryColor,
              ),
            ),
            const SizedBox(height: 20),
            _buildInfoRow('Prazo de Execução', orc['prazo_execucao']),
            if (orc['observacoes'] != null &&
                orc['observacoes'].isNotEmpty) ...[
              const SizedBox(height: 16),
              _buildInfoRow('Observações', orc['observacoes']),
            ],
            if (orc['condicoes'] != null && orc['condicoes'].isNotEmpty) ...[
              const SizedBox(height: 16),
              _buildInfoRow('Condições', orc['condicoes']),
            ],
            const SizedBox(height: 20),
            if (orc['status'] == 'aguardando')
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () => _aceitarOrcamento(orc['id'], modalContext),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: _primaryColor,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: const Text(
                    'Aceitar Orçamento',
                    style: TextStyle(
                      color: Colors.black,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            if (orc['status'] == 'realizado' && orc['ja_avaliado'] == false)
              SizedBox(
                width: double.infinity,
                child: OutlinedButton(
                  onPressed: () => _avaliarNoModal(orc, modalContext),
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: _primaryColor),
                    foregroundColor: _primaryColor,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                  ),
                  child: const Text('Avaliar serviço'),
                ),
              ),
            if (orc['status'] == 'realizado' && orc['ja_avaliado'] == true)
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

  Color _getOrcamentoStatusColor(String status) {
    return StatusColors.getOrcamentoColor(status);
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

  Future<void> _aceitarOrcamento(
    int orcamentoId,
    BuildContext modalContext,
  ) async {
    try {
      final response = await http.put(
        Uri.parse(
          '${AppConstants.baseUrl}/orcamentos/$orcamentoId/aceitar?cliente_id=${widget.usuarioId}',
        ),
      );

      if (!mounted) return;
      if (response.statusCode == 200) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Orçamento aceito!'),
              backgroundColor: Colors.green,
            ),
          );
        }
        if (modalContext.mounted) Navigator.pop(modalContext);
        _carregarSolicitacoes();
      } else if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Erro ao aceitar orçamento'),
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

  Future<void> _avaliarNoModal(dynamic orc, BuildContext modalContext) async {
    int estrelas = 0;
    final comentarioCtrl = TextEditingController();

    await showDialog(
      context: modalContext,
      builder: (dialogContext) => StatefulBuilder(
        builder: (ctx, setDialogState) => AlertDialog(
          backgroundColor: _cardColor,
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
                      color: ativo ? _primaryColor : Colors.grey[700],
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
                  fillColor: _cardDarkerColor,
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
                      'orcamento_id': orc['id'],
                      'cliente_id': widget.usuarioId,
                      'prestador_id': orc['prestador_id'],
                      'estrelas': estrelas,
                      'comentario': comentarioCtrl.text,
                    }),
                  );
                  if (!mounted) return;
                  if (resp.statusCode == 201) {
                    if (dialogContext.mounted) Navigator.pop(dialogContext);
                    if (modalContext.mounted) Navigator.pop(modalContext);
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('Avaliação enviada!'),
                          backgroundColor: Colors.green,
                        ),
                      );
                    }
                    _carregarSolicitacoes();
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
                style: TextStyle(color: _primaryColor),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
