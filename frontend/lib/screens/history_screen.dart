import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/quote.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  List<Quote> _quotes = [];
  bool _isLoading = true;
  String _error = '';

  @override
  void initState() {
    super.initState();
    _loadQuotes();
  }

  Future<void> _loadQuotes() async {
    if (!mounted) return;

    setState(() {
      _isLoading = true;
      _error = '';
    });

    try {
      final quotes = await ApiService.getAllQuotes();
      if (mounted) {
        setState(() {
          _quotes = quotes;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _error = 'Erro ao carregar orçamentos: $e';
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _deleteQuote(int quoteId) async {
    try {
      await ApiService.deleteQuote(quoteId);
      await _loadQuotes();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Orçamento excluído com sucesso')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erro ao excluir orçamento: $e')),
        );
      }
    }
  }

  void _showDeleteDialog(Quote quote) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Confirmar Exclusão'),
        content: Text('Deseja realmente excluir o orçamento "${quote.title}"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancelar'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              _deleteQuote(quote.id);
            },
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Excluir'),
          ),
        ],
      ),
    );
  }

  void _showEditDialog(Quote quote) {
    final titleController = TextEditingController(text: quote.title);
    final descriptionController = TextEditingController(
      text: quote.description ?? '',
    );
    String selectedStatus = quote.status;
    bool isUpdating = false;

    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setState) => AlertDialog(
          title: const Text('Editar Orçamento'),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextField(
                  controller: titleController,
                  decoration: const InputDecoration(
                    labelText: 'Título',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: descriptionController,
                  decoration: const InputDecoration(
                    labelText: 'Descrição',
                    border: OutlineInputBorder(),
                  ),
                  maxLines: 3,
                ),
                const SizedBox(height: 16),
                DropdownButtonFormField<String>(
                  initialValue: selectedStatus,
                  decoration: const InputDecoration(
                    labelText: 'Status',
                    border: OutlineInputBorder(),
                  ),
                  items: const [
                    DropdownMenuItem(value: 'draft', child: Text('Rascunho')),
                    DropdownMenuItem(value: 'sent', child: Text('Enviado')),
                    DropdownMenuItem(
                      value: 'approved',
                      child: Text('Aprovado'),
                    ),
                    DropdownMenuItem(
                      value: 'rejected',
                      child: Text('Rejeitado'),
                    ),
                    DropdownMenuItem(
                      value: 'pendente',
                      child: Text('Pendente'),
                    ),
                  ],
                  onChanged: (value) {
                    if (value != null) {
                      setState(() {
                        selectedStatus = value;
                      });
                    }
                  },
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancelar'),
            ),
            ElevatedButton(
              onPressed: isUpdating
                  ? null
                  : () async {
                      try {
                        // Validação dos campos
                        if (titleController.text.trim().isEmpty) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              content: Text('Título é obrigatório'),
                              backgroundColor: Colors.red,
                            ),
                          );
                          return;
                        }

                        setState(() {
                          isUpdating = true;
                        });

                        final update = QuoteUpdate(
                          title: titleController.text.trim(),
                          description: descriptionController.text.trim().isEmpty
                              ? null
                              : descriptionController.text.trim(),
                          status: selectedStatus,
                        );

                        await ApiService.updateQuote(quote.id, update);

                        if (mounted) {
                          // ignore: use_build_context_synchronously
                          Navigator.pop(context);
                          await _loadQuotes();
                          // ignore: use_build_context_synchronously
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              content: Text('Orçamento atualizado com sucesso'),
                              backgroundColor: Colors.green,
                            ),
                          );
                        }
                      } catch (e) {
                        if (mounted) {
                          // ignore: use_build_context_synchronously
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text('Erro ao atualizar orçamento: $e'),
                              backgroundColor: Colors.red,
                            ),
                          );
                        }
                      } finally {
                        if (mounted) {
                          setState(() {
                            isUpdating = false;
                          });
                        }
                      }
                    },
              child: isUpdating
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                      ),
                    )
                  : const Text('Salvar'),
            ),
          ],
        ),
      ),
    );
  }

  String _getStatusText(String status) {
    switch (status) {
      case 'draft':
        return 'Rascunho';
      case 'sent':
        return 'Enviado';
      case 'approved':
        return 'Aprovado';
      case 'rejected':
        return 'Rejeitado';
      default:
        return status;
    }
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'draft':
        return Colors.orange;
      case 'sent':
        return Colors.blue;
      case 'approved':
        return Colors.green;
      case 'rejected':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Column(
        children: [
          // Header
          Container(
            padding: const EdgeInsets.all(20),
            decoration: const BoxDecoration(color: Colors.black),
            child: Row(
              children: [
                Image.asset(
                  'assets/images/Worca.png',
                  height: 80,
                  width: 100,
                  fit: BoxFit.contain,
                  errorBuilder: (context, error, stackTrace) {
                    return Icon(
                      Icons.home_work,
                      size: 80,
                      color: Color(0xFFf5c116),
                    );
                  },
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Histórico de Orçamentos',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      Text(
                        'Gerencie seus orçamentos',
                        style: TextStyle(fontSize: 14, color: Colors.grey[400]),
                      ),
                    ],
                  ),
                ),
                IconButton(
                  onPressed: _loadQuotes,
                  icon: const Icon(Icons.refresh, color: Color(0xFFf5c116)),
                  tooltip: 'Atualizar',
                ),
              ],
            ),
          ),

          // Content
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _error.isNotEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(
                          Icons.error_outline,
                          size: 64,
                          color: Colors.red,
                        ),
                        const SizedBox(height: 16),
                        Text(
                          _error,
                          style: Theme.of(context).textTheme.bodyLarge,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 16),
                        ElevatedButton(
                          onPressed: _loadQuotes,
                          child: const Text('Tentar Novamente'),
                        ),
                      ],
                    ),
                  )
                : _quotes.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(
                          Icons.description_outlined,
                          size: 64,
                          color: Color(0xFF666666),
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'Nenhum orçamento encontrado',
                          style: Theme.of(context).textTheme.headlineSmall,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Crie seu primeiro orçamento na tela inicial',
                          style: Theme.of(context).textTheme.bodyLarge
                              ?.copyWith(color: const Color(0xFF666666)),
                        ),
                      ],
                    ),
                  )
                : RefreshIndicator(
                    onRefresh: _loadQuotes,
                    child: ListView.builder(
                      padding: const EdgeInsets.all(16),
                      itemCount: _quotes.length,
                      itemBuilder: (context, index) {
                        final quote = _quotes[index];
                        return Card(
                          margin: const EdgeInsets.only(bottom: 12),
                          elevation: 2,
                          color: Color(0xFF1a1a1a),
                          child: ListTile(
                            contentPadding: const EdgeInsets.all(16),
                            title: Text(
                              quote.title,
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 16,
                                color: Colors.white,
                              ),
                            ),
                            subtitle: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const SizedBox(height: 4),
                                Text(
                                  'Cliente: ${quote.client.name}',
                                  style: TextStyle(color: Color(0xFFBDBDBD)),
                                ),
                                if (quote.description != null &&
                                    quote.description!.isNotEmpty)
                                  Text(
                                    'Descrição: ${quote.description}',
                                    style: TextStyle(color: Color(0xFFBDBDBD)),
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
                                        color: _getStatusColor(
                                          quote.status,
                                        ).withValues(alpha: 0.1),
                                        borderRadius: BorderRadius.circular(12),
                                        border: Border.all(
                                          color: _getStatusColor(quote.status),
                                          width: 1,
                                        ),
                                      ),
                                      child: Text(
                                        _getStatusText(quote.status),
                                        style: TextStyle(
                                          color: _getStatusColor(quote.status),
                                          fontSize: 12,
                                          fontWeight: FontWeight.w600,
                                        ),
                                      ),
                                    ),
                                    const Spacer(),
                                    Text(
                                      'R\$ ${quote.total.toStringAsFixed(2)}',
                                      style: const TextStyle(
                                        fontWeight: FontWeight.bold,
                                        fontSize: 16,
                                        color: Color(0xFFf5c116),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  'Criado em: ${_formatDate(quote.createdAt)}',
                                  style: const TextStyle(
                                    fontSize: 12,
                                    color: Color(0xFFBDBDBD),
                                  ),
                                ),
                              ],
                            ),
                            trailing: PopupMenuButton<String>(
                              onSelected: (value) {
                                if (value == 'edit') {
                                  _showEditDialog(quote);
                                } else if (value == 'delete') {
                                  _showDeleteDialog(quote);
                                }
                              },
                              itemBuilder: (context) => [
                                const PopupMenuItem(
                                  value: 'edit',
                                  child: Row(
                                    children: [
                                      Icon(Icons.edit, size: 20),
                                      SizedBox(width: 8),
                                      Text('Editar'),
                                    ],
                                  ),
                                ),
                                const PopupMenuItem(
                                  value: 'delete',
                                  child: Row(
                                    children: [
                                      Icon(
                                        Icons.delete,
                                        size: 20,
                                        color: Colors.red,
                                      ),
                                      SizedBox(width: 8),
                                      Text(
                                        'Excluir',
                                        style: TextStyle(color: Colors.red),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
                  ),
          ),
        ],
      ),
    );
  }

  String _formatDate(DateTime date) {
    return '${date.day.toString().padLeft(2, '0')}/${date.month.toString().padLeft(2, '0')}/${date.year}';
  }
}
