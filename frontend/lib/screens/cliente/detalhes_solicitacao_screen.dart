import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../../constants/app_constants.dart';
import '../../models/orcamento.dart';

class DetalhesSolicitacaoScreen extends StatefulWidget {
  final int solicitacaoId;
  final int clienteId;

  const DetalhesSolicitacaoScreen({
    super.key,
    required this.solicitacaoId,
    required this.clienteId,
  });

  @override
  State<DetalhesSolicitacaoScreen> createState() =>
      _DetalhesSolicitacaoScreenState();
}

class _DetalhesSolicitacaoScreenState extends State<DetalhesSolicitacaoScreen> {
  List<Orcamento> _orcamentos = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _carregarOrcamentos();
  }

  Future<void> _carregarOrcamentos() async {
    setState(() => _isLoading = true);

    try {
      final response = await http.get(
        Uri.parse(
          '${AppConstants.baseUrl}/orcamentos/solicitacao/${widget.solicitacaoId}?cliente_id=${widget.clienteId}',
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
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text('Orçamentos Recebidos'),
      ),
      body: _isLoading
          ? const Center(
              child: CircularProgressIndicator(color: Color(0xFFf5c116)),
            )
          : _orcamentos.isEmpty
          ? Center(
              child: Text(
                'Aguardando orçamentos...',
                style: TextStyle(fontSize: 18, color: Colors.grey[400]),
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _orcamentos.length,
              itemBuilder: (_, i) => _buildOrcamentoCard(_orcamentos[i]),
            ),
    );
  }

  Widget _buildOrcamentoCard(Orcamento orc) {
    return Card(
      color: const Color(0xFF1a1a1a),
      margin: const EdgeInsets.only(bottom: 16),
      child: InkWell(
        onTap: () => _mostrarDetalhesOrcamento(orc),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    orc.prestadorNome ?? 'Prestador',
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
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Valor:', style: TextStyle(color: Colors.grey)),
                  Text(
                    'R\$ ${orc.valorProposto.toStringAsFixed(2)}',
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFFf5c116),
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
                const SizedBox(height: 8),
                Text(
                  orc.observacoes!,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(color: Colors.grey[300]),
                ),
              ],
              const SizedBox(height: 12),
              Row(
                children: [
                  const Spacer(),
                  Icon(
                    Icons.arrow_forward_ios,
                    size: 16,
                    color: Colors.grey[500],
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _mostrarDetalhesOrcamento(Orcamento orc) async {
    final result = await showModalBottomSheet(
      context: context,
      backgroundColor: Colors.black,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => DraggableScrollableSheet(
        initialChildSize: 0.9,
        minChildSize: 0.5,
        maxChildSize: 0.95,
        expand: false,
        builder: (_, scrollController) =>
            _buildModalContent(orc, scrollController),
      ),
    );
    if (result == true) _carregarOrcamentos();
  }

  Widget _buildModalContent(Orcamento orc, ScrollController scrollController) {
    return SingleChildScrollView(
      controller: scrollController,
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Detalhes do Orçamento',
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              IconButton(
                icon: const Icon(Icons.close, color: Colors.white),
                onPressed: () => Navigator.pop(context),
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
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        orc.prestadorNome ?? 'Prestador',
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
                          color: _getStatusColor(
                            orc.status,
                          ).withValues(alpha: 0.2),
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
                    'Valor Proposto',
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
                  if (orc.condicoes != null && orc.condicoes!.isNotEmpty) ...[
                    const SizedBox(height: 16),
                    _buildInfoRow('Condições', orc.condicoes!),
                  ],
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          if (orc.status == 'aguardando')
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () => _aceitarOrcamento(orc),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFFf5c116),
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
          if (orc.status == 'realizado')
            SizedBox(
              width: double.infinity,
              child: OutlinedButton(
                onPressed: () => _avaliar(orc),
                style: OutlinedButton.styleFrom(
                  side: const BorderSide(color: Color(0xFFf5c116)),
                  foregroundColor: const Color(0xFFf5c116),
                  padding: const EdgeInsets.symmetric(vertical: 14),
                ),
                child: const Text('Avaliar serviço'),
              ),
            ),
        ],
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

  Future<void> _aceitarOrcamento(Orcamento orc) async {
    try {
      final response = await http.put(
        Uri.parse(
          '${AppConstants.baseUrl}/orcamentos/${orc.id}/aceitar?cliente_id=${widget.clienteId}',
        ),
      );

      if (response.statusCode == 200 && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Orçamento aceito!'),
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

  Future<void> _avaliar(Orcamento orc) async {
    int estrelas = 0;
    final comentarioCtrl = TextEditingController();

    await showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF1a1a1a),
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
      ),
      builder: (ctx) {
        return StatefulBuilder(
          builder: (ctx, setModalState) => Padding(
            padding: EdgeInsets.only(
              left: 16,
              right: 16,
              top: 16,
              bottom: MediaQuery.of(ctx).viewInsets.bottom + 16,
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Avaliar serviço',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 12),
                Row(
                  children: List.generate(5, (i) {
                    final idx = i + 1;
                    final ativo = estrelas >= idx;
                    return IconButton(
                      onPressed: () => setModalState(() => estrelas = idx),
                      icon: Icon(
                        Icons.star,
                        color: ativo
                            ? const Color(0xFFf5c116)
                            : Colors.grey[700],
                      ),
                    );
                  }),
                ),
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
                const SizedBox(height: 12),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
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
                          body:
                              '{"orcamento_id": ${orc.id}, "cliente_id": ${widget.clienteId}, "prestador_id": ${orc.prestadorId}, "estrelas": $estrelas, "comentario": "${comentarioCtrl.text.replaceAll('"', '\\"')}"}',
                        );
                        if (!mounted) return;
                        if (resp.statusCode == 201) {
                          if (ctx.mounted) Navigator.pop(ctx);
                          if (mounted) {
                            Navigator.pop(context, true);
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text('Avaliação enviada!'),
                                backgroundColor: Colors.green,
                              ),
                            );
                          }
                        } else if (mounted) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text('Erro (${resp.statusCode})'),
                              backgroundColor: Colors.red,
                            ),
                          );
                        }
                      } catch (e) {
                        if (!mounted) return;
                        if (mounted) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text('Erro: $e'),
                              backgroundColor: Colors.red,
                            ),
                          );
                        }
                      }
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFFf5c116),
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                    child: const Text(
                      'Enviar Avaliação',
                      style: TextStyle(
                        color: Colors.black,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'aceito':
      case 'fechado':
        return Colors.green;
      case 'recusado':
        return Colors.red;
      default:
        return const Color(0xFFf5c116);
    }
  }
}
