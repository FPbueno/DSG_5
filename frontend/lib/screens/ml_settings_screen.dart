import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../widgets/logo_widget.dart';

class MLSettingsScreen extends StatefulWidget {
  const MLSettingsScreen({super.key});

  @override
  State<MLSettingsScreen> createState() => _MLSettingsScreenState();
}

class _MLSettingsScreenState extends State<MLSettingsScreen> {
  bool _isLoading = false;
  Map<String, dynamic>? _lastRetrainResult;
  Map<String, dynamic>? _lastPopulateResult;

  Future<void> _retrainModels() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final result = await ApiService.retrainMLModels();
      setState(() {
        _lastRetrainResult = result;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('✅ Modelos retreinados com sucesso!'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('❌ Erro ao retreinar: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _populateTrainingData() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final result = await ApiService.populateTrainingData();
      setState(() {
        _lastPopulateResult = result;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('✅ Dados de treinamento adicionados!'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('❌ Erro ao popular dados: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _testPrediction() async {
    setState(() {
      _isLoading = true;
    });

    try {
      // Testa predição de categoria
      final categoryResult = await ApiService.predictCategory(
        "instalacao eletrica",
      );

      // Testa predição de preço
      final priceResult = await ApiService.predictPrice("pintura parede");

      if (mounted) {
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('🧪 Teste de Predições'),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('📊 Categoria para "instalacao eletrica":'),
                Text(
                  '• ${categoryResult['predicted_category']}',
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 16),
                Text('💰 Preço para "pintura parede":'),
                Text(
                  '• R\$ ${priceResult['suggested_price'].toStringAsFixed(2)}',
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                Text('• Faixa: ${priceResult['price_range']}'),
              ],
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('OK'),
              ),
            ],
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('❌ Erro no teste: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFf8f9fa),
      body: Column(
        children: [
          // Header
          Container(
            height: 80,
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
                children: [
                  // Title
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
                          '🤖 Configurações ML',
                          style: Theme.of(context).textTheme.displaySmall,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Gerencie os modelos de Machine Learning',
                          style: Theme.of(context).textTheme.bodyLarge
                              ?.copyWith(color: const Color(0xFF666666)),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 24),

                  // Actions
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
                        // Popular Dados de Treinamento
                        _buildActionCard(
                          title: '📊 Popular Dados de Treinamento',
                          description:
                              'Adiciona 65+ serviços residenciais ao sistema',
                          buttonText: 'Popular Dados',
                          onPressed: _isLoading ? null : _populateTrainingData,
                          color: Colors.blue,
                        ),

                        const SizedBox(height: 16),

                        // Retreinar Modelos
                        _buildActionCard(
                          title: '🔄 Retreinar Modelos',
                          description:
                              'Retreina os modelos com dados atualizados',
                          buttonText: 'Retreinar',
                          onPressed: _isLoading ? null : _retrainModels,
                          color: Colors.orange,
                        ),

                        const SizedBox(height: 16),

                        // Testar Predições
                        _buildActionCard(
                          title: '🧪 Testar Predições',
                          description: 'Testa categoria e preço de serviços',
                          buttonText: 'Testar',
                          onPressed: _isLoading ? null : _testPrediction,
                          color: Colors.green,
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 24),

                  // Results
                  if (_lastRetrainResult != null || _lastPopulateResult != null)
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
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            '📋 Últimos Resultados',
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                          const SizedBox(height: 16),

                          if (_lastPopulateResult != null) ...[
                            _buildResultItem(
                              'Dados Populados',
                              '${_lastPopulateResult!['services_created']} de ${_lastPopulateResult!['total_training_services']} serviços',
                            ),
                            const SizedBox(height: 8),
                          ],

                          if (_lastRetrainResult != null) ...[
                            _buildResultItem(
                              'Retreinamento',
                              _lastRetrainResult!['message'] ?? 'Concluído',
                            ),
                            _buildResultItem(
                              'Timestamp',
                              _lastRetrainResult!['timestamp']?.substring(
                                    0,
                                    19,
                                  ) ??
                                  'N/A',
                            ),
                          ],
                        ],
                      ),
                    ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionCard({
    required String title,
    required String description,
    required String buttonText,
    required VoidCallback? onPressed,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        // ignore: deprecated_member_use
        color: color.withOpacity(0.05),
        borderRadius: BorderRadius.circular(12),
        // ignore: deprecated_member_use
        border: Border.all(color: color.withOpacity(0.2)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: Theme.of(
              context,
            ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          Text(
            description,
            style: Theme.of(
              context,
            ).textTheme.bodyMedium?.copyWith(color: const Color(0xFF666666)),
          ),
          const SizedBox(height: 16),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: onPressed,
              style: ElevatedButton.styleFrom(
                backgroundColor: color,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 12),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
              child: _isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                      ),
                    )
                  : Text(buttonText),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildResultItem(String label, String value) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('$label: ', style: const TextStyle(fontWeight: FontWeight.w600)),
        Expanded(child: Text(value)),
      ],
    );
  }
}
