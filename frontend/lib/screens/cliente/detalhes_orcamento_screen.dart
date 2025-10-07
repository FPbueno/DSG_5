import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../../constants/app_constants.dart';
import '../../models/orcamento.dart';
import '../../utils/status_colors.dart';

class DetalhesOrcamentoScreen extends StatelessWidget {
  final Orcamento orcamento;
  final int clienteId;

  const DetalhesOrcamentoScreen({
    super.key,
    required this.orcamento,
    required this.clienteId,
  });

  Future<void> _aceitar(BuildContext context) async {
    try {
      final response = await http.put(
        Uri.parse(
          '${AppConstants.baseUrl}/orcamentos/${orcamento.id}/aceitar?cliente_id=$clienteId',
        ),
      );

      if (response.statusCode == 200 && context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Orçamento aceito!'),
            backgroundColor: Colors.green,
          ),
        );
        Navigator.pop(context, true);
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erro: $e'), backgroundColor: Colors.red),
        );
      }
    }
  }

  Color _getStatusColor(String status) {
    return StatusColors.getOrcamentoColor(status);
  }

  Future<void> _avaliar(BuildContext context) async {
    int estrelas = 0;
    final comentarioCtrl = TextEditingController();

    await showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF1a1a1a),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
      ),
      builder: (ctx) {
        return StatefulBuilder(
          builder: (ctx, setModalState) => Padding(
            padding: const EdgeInsets.all(16),
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
                              '{"orcamento_id": ${orcamento.id}, "cliente_id": $clienteId, "prestador_id": ${orcamento.prestadorId}, "estrelas": $estrelas, "comentario": "${comentarioCtrl.text.replaceAll('"', '\\"')}"}',
                        );
                        if (!context.mounted) return;
                        if (resp.statusCode == 201) {
                          Navigator.pop(ctx);
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              content: Text('Avaliação enviada!'),
                              backgroundColor: Colors.green,
                            ),
                          );
                          Navigator.pop(context, true);
                        } else {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text(
                                'Erro ao enviar (${resp.statusCode})',
                              ),
                              backgroundColor: Colors.red,
                            ),
                          );
                        }
                      } catch (e) {
                        if (!context.mounted) return;
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text('Erro: $e'),
                            backgroundColor: Colors.red,
                          ),
                        );
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text('Detalhes do Orçamento'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
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
                          orcamento.prestadorNome ?? 'Prestador',
                          style: const TextStyle(
                            fontSize: 22,
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
                              orcamento.status,
                            ).withValues(alpha: 0.2),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(
                            orcamento.statusFormatado,
                            style: TextStyle(
                              color: _getStatusColor(orcamento.status),
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ),
                      ],
                    ),
                    if (orcamento.prestadorAvaliacao != null) ...[
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          const Icon(
                            Icons.star,
                            color: Color(0xFFf5c116),
                            size: 20,
                          ),
                          const SizedBox(width: 4),
                          Text(
                            orcamento.prestadorAvaliacao!.toStringAsFixed(1),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ],
                      ),
                    ],
                    const SizedBox(height: 24),
                    const Text(
                      'Valor Proposto',
                      style: TextStyle(color: Colors.grey, fontSize: 14),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'R\$ ${orcamento.valorProposto.toStringAsFixed(2)}',
                      style: const TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFFf5c116),
                      ),
                    ),
                    const SizedBox(height: 24),
                    _buildInfoRow('Prazo de Execução', orcamento.prazoExecucao),
                    if (orcamento.observacoes != null &&
                        orcamento.observacoes!.isNotEmpty) ...[
                      const SizedBox(height: 20),
                      const Text(
                        'Observações',
                        style: TextStyle(color: Colors.grey, fontSize: 14),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        orcamento.observacoes!,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                        ),
                      ),
                    ],
                    if (orcamento.condicoes != null &&
                        orcamento.condicoes!.isNotEmpty) ...[
                      const SizedBox(height: 20),
                      const Text(
                        'Condições',
                        style: TextStyle(color: Colors.grey, fontSize: 14),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        orcamento.condicoes!,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                        ),
                      ),
                    ],
                  ],
                ),
              ),
            ),
            if (orcamento.status == 'aguardando') ...[
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () => _aceitar(context),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFFf5c116),
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: const Text(
                    'Aceitar Orçamento',
                    style: TextStyle(
                      color: Colors.black,
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ],
            if (orcamento.status == 'realizado') ...[
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: OutlinedButton(
                  onPressed: () => _avaliar(context),
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: Color(0xFFf5c116)),
                    foregroundColor: const Color(0xFFf5c116),
                    padding: const EdgeInsets.symmetric(vertical: 14),
                  ),
                  child: const Text('Avaliar serviço (1–5 estrelas)'),
                ),
              ),
            ],
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
