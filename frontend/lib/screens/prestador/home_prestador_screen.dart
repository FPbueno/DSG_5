import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../../constants/app_constants.dart';
import '../../models/solicitacao.dart';
import '../../models/orcamento.dart';
import 'detalhes_solicitacao_prestador_screen.dart';

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
  List<Solicitacao> _solicitacoes = [];
  List<Orcamento> _agenda = [];
  bool _isLoading = true;
  DateTime _diaSelecionado = DateTime.now();

  @override
  void initState() {
    super.initState();
    _carregarSolicitacoes();
  }

  Future<void> _carregarSolicitacoes() async {
    setState(() => _isLoading = true);

    try {
      final respSolic = await http.get(
        Uri.parse(
          '${AppConstants.baseUrl}/solicitacoes/disponiveis?prestador_id=${widget.usuarioId}',
        ),
      );

      if (respSolic.statusCode == 200) {
        final List data = jsonDecode(respSolic.body);
        _solicitacoes = data.map((json) => Solicitacao.fromJson(json)).toList();
      }

      final respAgenda = await http.get(
        Uri.parse(
          '${AppConstants.baseUrl}/orcamentos/meus-orcamentos?prestador_id=${widget.usuarioId}',
        ),
      );
      if (respAgenda.statusCode == 200) {
        final List data = jsonDecode(respAgenda.body);
        _agenda = data.map((j) => Orcamento.fromJson(j)).toList();
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
                    onPressed: _carregarSolicitacoes,
                  ),
                ],
              ),
            ),
            _buildAgendaHeader(),
            const SizedBox(height: 12),
            _buildCalendario(),
            const SizedBox(height: 8),
            Expanded(child: _buildBody()),
          ],
        ),
      ),
    );
  }

  List<Orcamento> get _itensDoDia {
    return _agenda.where((o) {
      final dt = o.datetimeInicio ?? o.createdAt;
      return dt.year == _diaSelecionado.year &&
          dt.month == _diaSelecionado.month &&
          dt.day == _diaSelecionado.day;
    }).toList()..sort((a, b) {
      final da = a.datetimeInicio ?? a.createdAt;
      final db = b.datetimeInicio ?? b.createdAt;
      return da.compareTo(db);
    });
  }

  Widget _buildAgendaHeader() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Text(
            'Agenda',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          Text(
            '${_diaSelecionado.day}/${_diaSelecionado.month}',
            style: const TextStyle(color: Colors.grey),
          ),
        ],
      ),
    );
  }

  Widget _buildCalendario() {
    final hoje = DateTime.now();
    final inicio = DateTime(hoje.year, hoje.month, hoje.day);
    final dias = List.generate(7, (i) => inicio.add(Duration(days: i)));

    return SizedBox(
      height: 72,
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        itemBuilder: (_, i) {
          final dia = dias[i];
          final ativo =
              dia.day == _diaSelecionado.day &&
              dia.month == _diaSelecionado.month &&
              dia.year == _diaSelecionado.year;
          final temServico = _agenda.any((o) {
            final dt = o.datetimeInicio ?? o.createdAt;
            return dt.year == dia.year &&
                dt.month == dia.month &&
                dt.day == dia.day;
          });

          return GestureDetector(
            onTap: () => setState(() => _diaSelecionado = dia),
            child: Container(
              width: 56,
              decoration: BoxDecoration(
                color: ativo
                    ? const Color(0xFFf5c116)
                    : const Color(0xFF1a1a1a),
                borderRadius: BorderRadius.circular(12),
                border: temServico
                    ? Border.all(color: Colors.greenAccent, width: 2)
                    : null,
              ),
              padding: const EdgeInsets.symmetric(vertical: 8),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    '${dia.day}',
                    style: TextStyle(
                      color: ativo ? Colors.black : Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    [
                      'Dom',
                      'Seg',
                      'Ter',
                      'Qua',
                      'Qui',
                      'Sex',
                      'Sáb',
                    ][dia.weekday % 7],
                    style: TextStyle(
                      color: ativo ? Colors.black87 : Colors.grey[400],
                      fontSize: 10,
                    ),
                  ),
                ],
              ),
            ),
          );
        },
        separatorBuilder: (_, __) => const SizedBox(width: 8),
        itemCount: dias.length,
      ),
    );
  }

  Widget _buildBody() {
    return _isLoading
        ? const Center(
            child: CircularProgressIndicator(color: Color(0xFFf5c116)),
          )
        : _solicitacoes.isEmpty && _itensDoDia.isEmpty
        ? Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.work_off, size: 80, color: Colors.grey[700]),
                const SizedBox(height: 16),
                Text(
                  'Nenhuma solicitação disponível ou serviço agendado',
                  style: TextStyle(fontSize: 18, color: Colors.grey[400]),
                ),
              ],
            ),
          )
        : RefreshIndicator(
            onRefresh: _carregarSolicitacoes,
            color: const Color(0xFFf5c116),
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                if (_itensDoDia.isNotEmpty) ...[
                  const Text(
                    'Serviços do dia',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  ..._itensDoDia.map(_buildAgendaItem),
                  const SizedBox(height: 24),
                ],
                const Text(
                  'Solicitações disponíveis',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                ..._solicitacoes.map(_buildCard),
              ],
            ),
          );
  }

  Widget _buildAgendaItem(Orcamento o) {
    final inicio = o.datetimeInicio ?? o.createdAt;
    final fim = o.datetimeFim;
    final hora =
        '${inicio.hour.toString().padLeft(2, '0')}:${inicio.minute.toString().padLeft(2, '0')}';
    final horaFim = fim != null
        ? '${fim.hour.toString().padLeft(2, '0')}:${fim.minute.toString().padLeft(2, '0')}'
        : null;

    return Card(
      color: const Color(0xFF1a1a1a),
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        onTap: () => _abrirDetalhesAgenda(o),
        leading: const Icon(Icons.event_available, color: Colors.green),
        title: Text(
          o.categoria ?? 'Serviço',
          style: const TextStyle(color: Colors.white),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              horaFim != null ? '$hora - $horaFim' : hora,
              style: TextStyle(color: Colors.grey[300], fontSize: 12),
            ),
            if (o.descricao != null)
              Text(
                o.descricao!,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(color: Colors.grey[400], fontSize: 12),
              ),
          ],
        ),
        trailing: const Icon(Icons.arrow_forward_ios, color: Color(0xFFf5c116)),
      ),
    );
  }

  Future<void> _abrirDetalhesAgenda(Orcamento o) async {
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
                    'Serviço agendado',
                    style: TextStyle(
                      fontSize: 20,
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
              const SizedBox(height: 16),
              Text(
                o.categoria ?? 'Serviço',
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                o.descricao ?? '',
                style: TextStyle(color: Colors.grey[300], fontSize: 14),
              ),
              const SizedBox(height: 16),
              Text(
                'Horário: ${_formatarIntervalo(o)}',
                style: const TextStyle(color: Colors.white, fontSize: 14),
              ),
              const SizedBox(height: 8),
              Text(
                'Status: ${o.statusFormatado}',
                style: const TextStyle(color: Colors.white, fontSize: 14),
              ),
              const SizedBox(height: 16),
              Text(
                'Valor: R\$ ${o.valorProposto.toStringAsFixed(2)}',
                style: const TextStyle(
                  color: Color(0xFFf5c116),
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _formatarIntervalo(Orcamento o) {
    final inicio = o.datetimeInicio ?? o.createdAt;
    final fim = o.datetimeFim;
    final hIni =
        '${inicio.day.toString().padLeft(2, '0')}/${inicio.month.toString().padLeft(2, '0')} ${inicio.hour.toString().padLeft(2, '0')}:${inicio.minute.toString().padLeft(2, '0')}';
    if (fim == null) return hIni;
    final hFim =
        '${fim.day.toString().padLeft(2, '0')}/${fim.month.toString().padLeft(2, '0')} ${fim.hour.toString().padLeft(2, '0')}:${fim.minute.toString().padLeft(2, '0')}';
    return '$hIni - $hFim';
  }

  Widget _buildCard(Solicitacao sol) {
    return Card(
      color: const Color(0xFF1a1a1a),
      margin: const EdgeInsets.only(bottom: 16),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        title: Text(
          sol.categoria,
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
              sol.descricao,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: TextStyle(color: Colors.grey[400]),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Icon(Icons.location_on, size: 16, color: Colors.grey[500]),
                const SizedBox(width: 4),
                Expanded(
                  child: Text(
                    sol.localizacao,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(color: Colors.grey[500], fontSize: 12),
                  ),
                ),
                const SizedBox(width: 8),
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
        trailing: const Icon(Icons.arrow_forward_ios, color: Color(0xFFf5c116)),
        onTap: () async {
          final result = await Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => DetalhesSolicitacaoPrestadorScreen(
                solicitacaoId: sol.id,
                prestadorId: widget.usuarioId,
              ),
            ),
          );
          if (result == true) _carregarSolicitacoes();
        },
      ),
    );
  }
}
