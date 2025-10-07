import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../../constants/app_constants.dart';
import '../../models/solicitacao.dart';
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
          '${AppConstants.baseUrl}/solicitacoes/disponiveis?prestador_id=${widget.usuarioId}',
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
                    icon: const Icon(Icons.refresh, color: Color(0xFFf5c116)),
                    onPressed: _carregarSolicitacoes,
                  ),
                ],
              ),
            ),
            Expanded(child: _buildBody()),
          ],
        ),
      ),
    );
  }

  Widget _buildBody() {
    return _isLoading
        ? const Center(
            child: CircularProgressIndicator(color: Color(0xFFf5c116)),
          )
        : _solicitacoes.isEmpty
        ? Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.work_off, size: 80, color: Colors.grey[700]),
                const SizedBox(height: 16),
                Text(
                  'Nenhuma solicitação disponível',
                  style: TextStyle(fontSize: 18, color: Colors.grey[400]),
                ),
              ],
            ),
          )
        : RefreshIndicator(
            onRefresh: _carregarSolicitacoes,
            color: const Color(0xFFf5c116),
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _solicitacoes.length,
              itemBuilder: (_, i) => _buildCard(_solicitacoes[i]),
            ),
          );
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
