import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import '../widgets/logo_widget.dart';
import '../constants/app_constants.dart';
import 'login_screen.dart';

class SimpleHomeScreen extends StatefulWidget {
  const SimpleHomeScreen({super.key});

  @override
  State<SimpleHomeScreen> createState() => _SimpleHomeScreenState();
}

class _SimpleHomeScreenState extends State<SimpleHomeScreen> {
  final _formKey = GlobalKey<FormState>();
  final _clientNameController = TextEditingController();
  final _requestDateController = TextEditingController();

  String _selectedCategory = '';
  String _selectedSubcategory = '';
  bool _isLoading = false;
  bool _showResult = false;
  Map<String, dynamic>? _mlResponse;

  @override
  void dispose() {
    _clientNameController.dispose();
    _requestDateController.dispose();
    super.dispose();
  }

  void _showCategoryPicker() {
    showModalBottomSheet(
      context: context,
      builder: (context) => Container(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'Selecionar Categoria',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            ...AppConstants.categoryOptions.map(
              (option) => ListTile(
                leading: Text(
                  option['label']!.split(' ')[0],
                  style: const TextStyle(fontSize: 20),
                ),
                title: Text(option['label']!.substring(2)),
                onTap: () {
                  setState(() {
                    _selectedCategory = option['value']!;
                    _selectedSubcategory = '';
                  });
                  Navigator.pop(context);
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showSubcategoryPicker() {
    if (_selectedCategory.isEmpty) return;

    final subcategories =
        AppConstants.serviceCategories[_selectedCategory] ?? [];

    showModalBottomSheet(
      context: context,
      builder: (context) => Container(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'Selecionar Subcategoria',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            ...subcategories.map(
              (option) => ListTile(
                title: Text(option['label']!),
                onTap: () {
                  setState(() {
                    _selectedSubcategory = option['value']!;
                  });
                  Navigator.pop(context);
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _selectDate() async {
    try {
      final DateTime? picked = await showDatePicker(
        context: context,
        initialDate: DateTime.now(),
        firstDate: DateTime(2020),
        lastDate: DateTime(2030),
        builder: (context, child) {
          return Theme(
            data: Theme.of(context).copyWith(
              colorScheme: const ColorScheme.light(
                primary: Color(0xFF6366f1),
                onPrimary: Colors.white,
                surface: Colors.white,
                onSurface: Colors.black,
              ),
            ),
            child: child!,
          );
        },
      );

      if (picked != null) {
        setState(() {
          _requestDateController.text =
              '${picked.day.toString().padLeft(2, '0')}/${picked.month.toString().padLeft(2, '0')}/${picked.year}';
        });
      }
    } catch (e) {
      ScaffoldMessenger.of(
        // ignore: use_build_context_synchronously
        context,
      ).showSnackBar(SnackBar(content: Text('Erro ao abrir calendário: $e')));
    }
  }

  Future<void> _generateQuote() async {
    if (!_formKey.currentState!.validate()) return;
    if (_requestDateController.text.isEmpty) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('Selecione uma data')));
      return;
    }
    if (_selectedCategory.isEmpty || _selectedSubcategory.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Selecione categoria e subcategoria')),
      );
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      final response = await ApiService.smartCreateItem(
        _selectedSubcategory,
        _selectedCategory,
      );

      setState(() {
        _mlResponse = response;
        _showResult = true;
      });
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Erro: $e')));
      }
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _resetForm() {
    setState(() {
      _clientNameController.clear();
      _requestDateController.clear();
      _selectedCategory = '';
      _selectedSubcategory = '';
      _showResult = false;
      _mlResponse = null;
    });
  }

  Future<void> _logout() async {
    await AuthService.logout();
    if (mounted) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (context) => const LoginScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFf8f9fa),
      appBar: AppBar(
        title: const Text('WorcaFlow'),
        backgroundColor: const Color(0xFF667eea),
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _logout,
            tooltip: 'Sair',
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Header
            Container(
              padding: const EdgeInsets.all(20),
              decoration: const BoxDecoration(
                color: Colors.white,
                boxShadow: [
                  BoxShadow(
                    color: Color(0x1A000000),
                    offset: Offset(0, 2),
                    blurRadius: 3.84,
                  ),
                ],
              ),
              child: Center(
                child: const LogoWidget(size: 'large', showText: false),
              ),
            ),

            // Content
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(16),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    if (!_showResult) ...[
                      // Title Section
                      Container(
                        padding: const EdgeInsets.all(24),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(16),
                          boxShadow: [
                            BoxShadow(
                              color: const Color(0x1A000000),
                              offset: const Offset(0, 2),
                              blurRadius: 3.84,
                            ),
                          ],
                        ),
                        child: Column(
                          children: [
                            Text(
                              'Criar Novo Orçamento',
                              style: Theme.of(context).textTheme.displaySmall,
                              textAlign: TextAlign.center,
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Preencha os dados. O ML criará o orçamento completo automaticamente!',
                              style: Theme.of(context).textTheme.bodyLarge
                                  ?.copyWith(color: const Color(0xFF666666)),
                              textAlign: TextAlign.center,
                            ),
                          ],
                        ),
                      ),

                      const SizedBox(height: 16),

                      // Form
                      Container(
                        padding: const EdgeInsets.all(24),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(16),
                          boxShadow: [
                            BoxShadow(
                              color: const Color(0x1A000000),
                              offset: const Offset(0, 2),
                              blurRadius: 3.84,
                            ),
                          ],
                        ),
                        child: Form(
                          key: _formKey,
                          child: Column(
                            children: [
                              Text(
                                '📋 Solicitação de Serviço',
                                style: Theme.of(
                                  context,
                                ).textTheme.headlineSmall,
                                textAlign: TextAlign.center,
                              ),
                              const SizedBox(height: 24),

                              // Nome do Cliente
                              TextFormField(
                                controller: _clientNameController,
                                decoration: const InputDecoration(
                                  labelText: 'Nome da Pessoa *',
                                  hintText: 'Ex: João Silva',
                                ),
                                validator: (value) {
                                  if (value == null || value.trim().isEmpty) {
                                    return 'Nome é obrigatório';
                                  }
                                  return null;
                                },
                              ),
                              const SizedBox(height: 20),

                              // Data da Solicitação
                              GestureDetector(
                                onTap: _selectDate,
                                child: Container(
                                  padding: const EdgeInsets.all(16),
                                  decoration: BoxDecoration(
                                    color: Colors.white,
                                    border: Border.all(
                                      color: const Color(0xFFDDDDDD),
                                    ),
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Row(
                                    children: [
                                      const Icon(
                                        Icons.calendar_today,
                                        color: Color(0xFF6366f1),
                                        size: 20,
                                      ),
                                      const SizedBox(width: 12),
                                      Expanded(
                                        child: Text(
                                          _requestDateController.text.isEmpty
                                              ? 'Selecione uma data'
                                              : _requestDateController.text,
                                          style: TextStyle(
                                            color:
                                                _requestDateController
                                                    .text
                                                    .isEmpty
                                                ? const Color(0xFF999999)
                                                : const Color(0xFF333333),
                                            fontSize: 16,
                                          ),
                                        ),
                                      ),
                                      const Icon(
                                        Icons.keyboard_arrow_down,
                                        color: Color(0xFF6366f1),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                              const SizedBox(height: 20),

                              // Categoria
                              GestureDetector(
                                onTap: _showCategoryPicker,
                                child: Container(
                                  padding: const EdgeInsets.all(12),
                                  decoration: BoxDecoration(
                                    color: Colors.white,
                                    border: Border.all(
                                      color: const Color(0xFFDDDDDD),
                                    ),
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Row(
                                    children: [
                                      Expanded(
                                        child: Text(
                                          _selectedCategory.isEmpty
                                              ? 'Selecione uma categoria...'
                                              : AppConstants.categoryOptions
                                                    .firstWhere(
                                                      (opt) =>
                                                          opt['value'] ==
                                                          _selectedCategory,
                                                    )['label']!,
                                          style: TextStyle(
                                            color: _selectedCategory.isEmpty
                                                ? const Color(0xFF999999)
                                                : const Color(0xFF333333),
                                          ),
                                        ),
                                      ),
                                      const Icon(Icons.keyboard_arrow_down),
                                    ],
                                  ),
                                ),
                              ),
                              const SizedBox(height: 20),

                              // Subcategoria
                              GestureDetector(
                                onTap: _selectedCategory.isNotEmpty
                                    ? _showSubcategoryPicker
                                    : null,
                                child: Container(
                                  padding: const EdgeInsets.all(12),
                                  decoration: BoxDecoration(
                                    color: _selectedCategory.isEmpty
                                        ? const Color(0xFFf8f9fa)
                                        : Colors.white,
                                    border: Border.all(
                                      color: _selectedCategory.isEmpty
                                          ? const Color(0xFFe9ecef)
                                          : const Color(0xFFDDDDDD),
                                    ),
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Row(
                                    children: [
                                      Expanded(
                                        child: Text(
                                          _selectedCategory.isEmpty
                                              ? 'Selecione uma categoria primeiro'
                                              : _selectedSubcategory.isEmpty
                                              ? 'Selecione uma subcategoria...'
                                              : AppConstants
                                                    .serviceCategories[_selectedCategory]!
                                                    .firstWhere(
                                                      (opt) =>
                                                          opt['value'] ==
                                                          _selectedSubcategory,
                                                    )['label']!,
                                          style: TextStyle(
                                            color: _selectedCategory.isEmpty
                                                ? const Color(0xFF6c757d)
                                                : _selectedSubcategory.isEmpty
                                                ? const Color(0xFF999999)
                                                : const Color(0xFF333333),
                                          ),
                                        ),
                                      ),
                                      Icon(
                                        Icons.keyboard_arrow_down,
                                        color: _selectedCategory.isEmpty
                                            ? const Color(0xFF6c757d)
                                            : const Color(0xFF666666),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                              const SizedBox(height: 24),

                              // Botão Gerar Orçamento
                              SizedBox(
                                width: double.infinity,
                                child: ElevatedButton(
                                  onPressed: _isLoading ? null : _generateQuote,
                                  child: _isLoading
                                      ? const SizedBox(
                                          height: 20,
                                          width: 20,
                                          child: CircularProgressIndicator(
                                            strokeWidth: 2,
                                            valueColor:
                                                AlwaysStoppedAnimation<Color>(
                                                  Colors.white,
                                                ),
                                          ),
                                        )
                                      : const Text('Gerar Orçamento'),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ] else ...[
                      // Resultado do ML
                      Container(
                        padding: const EdgeInsets.all(24),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(16),
                          boxShadow: [
                            BoxShadow(
                              color: const Color(0x1A000000),
                              offset: const Offset(0, 2),
                              blurRadius: 3.84,
                            ),
                          ],
                        ),
                        child: Column(
                          children: [
                            Text(
                              '🤖 Resultado do ML',
                              style: Theme.of(context).textTheme.headlineSmall,
                              textAlign: TextAlign.center,
                            ),
                            const SizedBox(height: 20),

                            if (_mlResponse != null) ...[
                              Container(
                                padding: const EdgeInsets.all(20),
                                decoration: BoxDecoration(
                                  color: const Color(0xFFf8f9fa),
                                  borderRadius: BorderRadius.circular(12),
                                  border: Border.all(
                                    color: const Color(0xFFe9ecef),
                                  ),
                                ),
                                child: Column(
                                  children: [
                                    Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.center,
                                      children: [
                                        const Text(
                                          '⚡',
                                          style: TextStyle(fontSize: 20),
                                        ),
                                        const SizedBox(width: 8),
                                        Text(
                                          _mlResponse!['ml_predictions']?['professional_title'] ??
                                              'Análise Técnica',
                                          style: Theme.of(
                                            context,
                                          ).textTheme.headlineSmall,
                                        ),
                                      ],
                                    ),
                                    const SizedBox(height: 16),

                                    _buildResultItem(
                                      'Serviço:',
                                      _mlResponse!['ml_predictions']?['name'] ??
                                          'N/A',
                                    ),
                                    _buildResultItem(
                                      'Especificação Técnica:',
                                      _mlResponse!['ml_predictions']?['description'] ??
                                          'N/A',
                                    ),
                                    _buildResultItem(
                                      'Especialização:',
                                      _mlResponse!['ml_predictions']?['category'] ??
                                          'N/A',
                                    ),
                                    _buildResultItem(
                                      'Valor Estimado:',
                                      'R\$ ${(_mlResponse!['ml_predictions']?['price_suggestion']?['suggested_price'] ?? 0).toStringAsFixed(2)}',
                                      isPrice: true,
                                    ),
                                    _buildResultItem(
                                      'Classificação:',
                                      _mlResponse!['ml_predictions']?['price_suggestion']?['price_range'] ??
                                          'N/A',
                                    ),
                                    if (_mlResponse!['ml_predictions']?['price_suggestion']?['reasoning'] !=
                                        null)
                                      _buildResultItem(
                                        'Análise de Mercado:',
                                        _mlResponse!['ml_predictions']?['price_suggestion']?['reasoning'],
                                        isReasoning: true,
                                      ),
                                  ],
                                ),
                              ),
                            ],

                            const SizedBox(height: 20),

                            // Botões
                            Row(
                              children: [
                                Expanded(
                                  child: OutlinedButton(
                                    onPressed: () {
                                      setState(() {
                                        _showResult = false;
                                      });
                                    },
                                    child: const Text('Voltar'),
                                  ),
                                ),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: ElevatedButton(
                                    onPressed: _resetForm,
                                    style: ElevatedButton.styleFrom(
                                      backgroundColor: const Color(0xFF7c3aed),
                                    ),
                                    child: const Text('Novo Orçamento'),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ],
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildResultItem(
    String label,
    String value, {
    bool isPrice = false,
    bool isReasoning = false,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w600,
              color: const Color(0xFF666666),
            ),
          ),
          const SizedBox(height: 4),
          Container(
            padding: isReasoning ? const EdgeInsets.all(12) : null,
            decoration: isReasoning
                ? BoxDecoration(
                    color: const Color(0xFFf8f9fa),
                    borderRadius: BorderRadius.circular(8),
                  )
                : null,
            child: Text(
              value,
              style: TextStyle(
                fontSize: isPrice ? 24 : 16,
                fontWeight: isPrice ? FontWeight.bold : FontWeight.normal,
                color: isPrice
                    ? const Color(0xFF2196F3)
                    : const Color(0xFF333333),
                fontStyle: isReasoning ? FontStyle.italic : FontStyle.normal,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
