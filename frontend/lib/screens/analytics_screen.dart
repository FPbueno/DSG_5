import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../utils/format_utils.dart';

class AnalyticsScreen extends StatefulWidget {
  const AnalyticsScreen({super.key});

  @override
  State<AnalyticsScreen> createState() => _AnalyticsScreenState();
}

class _AnalyticsScreenState extends State<AnalyticsScreen>
    with TickerProviderStateMixin {
  late TabController _tabController;
  bool _isLoading = true;
  Map<String, dynamic>? _overviewData;
  Map<String, dynamic>? _servicesData;
  Map<String, dynamic>? _clientsData;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _loadAnalyticsData();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _loadAnalyticsData() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final overview = await ApiService.getAnalyticsOverview();
      final services = await ApiService.getServicesAnalytics();
      final clients = await ApiService.getClientsAnalytics();

      setState(() {
        _overviewData = overview;
        _servicesData = services;
        _clientsData = clients;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erro ao carregar analytics: $e')),
        );
      }
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
            child: Center(
              child: Image.asset(
                'assets/images/Worca.png',
                height: 120,
                width: 150,
                fit: BoxFit.contain,
                errorBuilder: (context, error, stackTrace) {
                  return Icon(
                    Icons.home_work,
                    size: 120,
                    color: Color(0xFFf5c116),
                  );
                },
              ),
            ),
          ),

          // Tabs
          Container(
            color: Colors.black,
            child: TabBar(
              controller: _tabController,
              labelColor: const Color(0xFFf5c116),
              unselectedLabelColor: Colors.grey[400],
              indicatorColor: const Color(0xFFf5c116),
              tabs: const [
                Tab(text: 'Visão Geral'),
                Tab(text: 'Serviços'),
                Tab(text: 'Clientes'),
              ],
            ),
          ),

          // Content
          Expanded(
            child: _isLoading
                ? const Center(
                    child: CircularProgressIndicator(
                      valueColor: AlwaysStoppedAnimation<Color>(
                        Color(0xFF6366f1),
                      ),
                    ),
                  )
                : TabBarView(
                    controller: _tabController,
                    children: [
                      _buildOverviewTab(),
                      _buildServicesTab(),
                      _buildClientsTab(),
                    ],
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildOverviewTab() {
    if (_overviewData == null) {
      return const Center(child: Text('Erro ao carregar dados'));
    }

    final overview = _overviewData!['overview'] ?? {};
    final statusDistribution = _overviewData!['status_distribution'] ?? {};
    final topServices = _overviewData!['top_services'] ?? [];
    final monthlyTrends = _overviewData!['monthly_trends'] ?? [];

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Cards de estatísticas principais
          _buildStatsCards(overview),
          const SizedBox(height: 20),

          // Gráfico de status dos orçamentos
          _buildStatusChart(statusDistribution),
          const SizedBox(height: 20),

          // Top serviços
          _buildTopServices(topServices),
          const SizedBox(height: 20),

          // Tendências mensais
          _buildMonthlyTrends(monthlyTrends),
        ],
      ),
    );
  }

  Widget _buildStatsCards(Map<String, dynamic> overview) {
    return Column(
      children: [
        Row(
          children: [
            Expanded(
              child: _buildStatCard(
                'Total de Orçamentos',
                '${overview['total_quotes'] ?? 0}',
                Icons.description,
                const Color(0xFF6366f1),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildStatCard(
                'Receita Total',
                FormatUtils.formatCurrency(overview['total_revenue'] ?? 0.0),
                Icons.attach_money,
                const Color(0xFF10b981),
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: _buildStatCard(
                'Valor Médio',
                FormatUtils.formatCurrency(overview['avg_quote_value'] ?? 0.0),
                Icons.trending_up,
                const Color(0xFFf59e0b),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildStatCard(
                'Receita 30d',
                FormatUtils.formatCurrency(
                  overview['recent_revenue_30d'] ?? 0.0,
                ),
                Icons.calendar_today,
                const Color(0xFFef4444),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildStatCard(
    String title,
    String value,
    IconData icon,
    Color color,
  ) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Color(0xFF1a1a1a),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Color(0xFFf5c116).withValues(alpha: 0.1),
            offset: const Offset(0, 2),
            blurRadius: 3.84,
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 20),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  title,
                  style: const TextStyle(
                    fontSize: 12,
                    color: Color(0xFFBDBDBD),
                    fontFamily: 'Poppins',
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            value,
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Colors.white,
              fontFamily: 'Quicksand',
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatusChart(Map<String, dynamic> statusDistribution) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Color(0xFF1a1a1a),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Color(0xFFf5c116).withValues(alpha: 0.1),
            offset: const Offset(0, 2),
            blurRadius: 3.84,
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Status dos Orçamentos',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
              fontFamily: 'Quicksand',
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 16),
          ...statusDistribution.entries.map((entry) {
            final status = entry.key;
            final count = entry.value;
            final total = statusDistribution.values.fold(
              0,
              (a, b) => a + (b as int),
            );
            final percentage = total > 0 ? (count / total) * 100 : 0.0;

            return Padding(
              padding: const EdgeInsets.only(bottom: 12),
              child: Row(
                children: [
                  Expanded(
                    flex: 2,
                    child: Text(
                      _getStatusLabel(status),
                      style: const TextStyle(
                        fontFamily: 'Poppins',
                        fontSize: 14,
                      ),
                    ),
                  ),
                  Expanded(
                    flex: 3,
                    child: LinearProgressIndicator(
                      value: percentage / 100,
                      backgroundColor: const Color(0xFFe5e7eb),
                      valueColor: AlwaysStoppedAnimation<Color>(
                        _getStatusColor(status),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Text(
                    '${count.toString()} (${percentage.toStringAsFixed(1)}%)',
                    style: const TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 12,
                      color: Color(0xFFBDBDBD),
                    ),
                  ),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }

  Widget _buildTopServices(List<dynamic> topServices) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Color(0xFF1a1a1a),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Color(0xFFf5c116).withValues(alpha: 0.1),
            offset: const Offset(0, 2),
            blurRadius: 3.84,
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Serviços Mais Populares',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
              fontFamily: 'Quicksand',
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 16),
          ...topServices.asMap().entries.map((entry) {
            final index = entry.key;
            final service = entry.value;
            final name = service[0] ?? 'N/A';
            final count = service[1] ?? 0;

            return Container(
              margin: const EdgeInsets.only(bottom: 8),
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: const Color(0xFF252525),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(
                children: [
                  Container(
                    width: 24,
                    height: 24,
                    decoration: BoxDecoration(
                      color: _getRankColor(index),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Center(
                      child: Text(
                        '${index + 1}',
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      name,
                      style: const TextStyle(
                        fontFamily: 'Poppins',
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                        color: Colors.white,
                      ),
                    ),
                  ),
                  Text(
                    '$count usos',
                    style: const TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 12,
                      color: Color(0xFFBDBDBD),
                    ),
                  ),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }

  Widget _buildMonthlyTrends(List<dynamic> monthlyTrends) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Color(0xFF1a1a1a),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Color(0xFFf5c116).withValues(alpha: 0.1),
            offset: const Offset(0, 2),
            blurRadius: 3.84,
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Tendências Mensais',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
              fontFamily: 'Quicksand',
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 16),
          ...monthlyTrends.map((trend) {
            final month = trend['month'] ?? '';
            final quotesCount = trend['quotes_count'] ?? 0;
            final revenue = trend['revenue'] ?? 0.0;

            return Container(
              margin: const EdgeInsets.only(bottom: 8),
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: const Color(0xFF252525),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: Text(
                      _formatMonth(month),
                      style: const TextStyle(
                        fontFamily: 'Poppins',
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                        color: Colors.white,
                      ),
                    ),
                  ),
                  Text(
                    '$quotesCount orçamentos',
                    style: const TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 12,
                      color: Color(0xFFBDBDBD),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Text(
                    FormatUtils.formatCurrency(revenue),
                    style: const TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 12,
                      color: Color(0xFFf5c116),
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }

  Widget _buildServicesTab() {
    if (_servicesData == null) {
      return const Center(child: Text('Erro ao carregar dados'));
    }

    final services = _servicesData!['services'] ?? [];
    final totalServices = _servicesData!['total_services'] ?? 0;
    final activeServices = _servicesData!['active_services'] ?? 0;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Resumo
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Color(0xFF1a1a1a),
              borderRadius: BorderRadius.circular(12),
              boxShadow: [
                BoxShadow(
                  color: Color(0xFFf5c116).withValues(alpha: 0.1),
                  offset: const Offset(0, 2),
                  blurRadius: 3.84,
                ),
              ],
            ),
            child: Row(
              children: [
                Expanded(
                  child: _buildStatCard(
                    'Total de Serviços',
                    '$totalServices',
                    Icons.build,
                    const Color(0xFF6366f1),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildStatCard(
                    'Serviços Ativos',
                    '$activeServices',
                    Icons.check_circle,
                    const Color(0xFF10b981),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),

          // Lista de serviços
          ...services.map((service) => _buildServiceCard(service)).toList(),
        ],
      ),
    );
  }

  Widget _buildServiceCard(Map<String, dynamic> service) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Color(0xFF1a1a1a),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Color(0xFFf5c116).withValues(alpha: 0.1),
            offset: const Offset(0, 2),
            blurRadius: 3.84,
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  service['service_name'] ?? 'N/A',
                  style: const TextStyle(
                    fontFamily: 'Quicksand',
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: const Color(0xFFf5c116),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  '${service['times_used'] ?? 0} usos',
                  style: const TextStyle(
                    color: Colors.black,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: _buildServiceStat(
                  'Preço Base',
                  FormatUtils.formatCurrency(service['base_price'] ?? 0.0),
                ),
              ),
              Expanded(
                child: _buildServiceStat(
                  'Preço Médio',
                  FormatUtils.formatCurrency(service['avg_price_used'] ?? 0.0),
                ),
              ),
              Expanded(
                child: _buildServiceStat(
                  'Total Usado',
                  '${service['total_usage'] ?? 0} ${service['unit'] ?? ''}',
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildServiceStat(String label, String value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: const TextStyle(
            fontFamily: 'Poppins',
            fontSize: 12,
            color: Color(0xFFBDBDBD),
          ),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            fontFamily: 'Poppins',
            fontSize: 14,
            fontWeight: FontWeight.w500,
            color: Colors.white,
          ),
        ),
      ],
    );
  }

  Widget _buildClientsTab() {
    if (_clientsData == null) {
      return const Center(child: Text('Erro ao carregar dados'));
    }

    final clients = _clientsData!['clients'] ?? [];
    final totalClients = _clientsData!['total_clients'] ?? 0;
    final activeClients = _clientsData!['active_clients'] ?? 0;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Resumo
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Color(0xFF1a1a1a),
              borderRadius: BorderRadius.circular(12),
              boxShadow: [
                BoxShadow(
                  color: Color(0xFFf5c116).withValues(alpha: 0.1),
                  offset: const Offset(0, 2),
                  blurRadius: 3.84,
                ),
              ],
            ),
            child: Row(
              children: [
                Expanded(
                  child: _buildStatCard(
                    'Total de Clientes',
                    '$totalClients',
                    Icons.people,
                    const Color(0xFF6366f1),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildStatCard(
                    'Clientes Ativos',
                    '$activeClients',
                    Icons.people_alt,
                    const Color(0xFF10b981),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),

          // Lista de clientes
          ...clients.map((client) => _buildClientCard(client)).toList(),
        ],
      ),
    );
  }

  Widget _buildClientCard(Map<String, dynamic> client) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Color(0xFF1a1a1a),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Color(0xFFf5c116).withValues(alpha: 0.1),
            offset: const Offset(0, 2),
            blurRadius: 3.84,
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  client['client_name'] ?? 'N/A',
                  style: const TextStyle(
                    fontFamily: 'Quicksand',
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: const Color(0xFFf5c116),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  '${client['quotes_count'] ?? 0} orçamentos',
                  style: const TextStyle(
                    color: Colors.black,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: _buildServiceStat(
                  'Total Gasto',
                  FormatUtils.formatCurrency(client['total_spent'] ?? 0.0),
                ),
              ),
              Expanded(
                child: _buildServiceStat(
                  'Valor Médio',
                  FormatUtils.formatCurrency(client['avg_quote_value'] ?? 0.0),
                ),
              ),
              Expanded(
                child: _buildServiceStat(
                  'Último Orçamento',
                  _formatDate(client['last_quote_date'] ?? ''),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  String _getStatusLabel(String status) {
    switch (status) {
      case 'draft':
        return 'Rascunho';
      case 'sent':
        return 'Enviado';
      case 'approved':
        return 'Aprovado';
      case 'rejected':
        return 'Rejeitado';
      case 'pendente':
        return 'Pendente';
      default:
        return status;
    }
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'draft':
        return const Color(0xFF6b7280);
      case 'sent':
        return const Color(0xFF3b82f6);
      case 'approved':
        return const Color(0xFF10b981);
      case 'rejected':
        return const Color(0xFFef4444);
      case 'pendente':
        return const Color(0xFFf59e0b);
      default:
        return const Color(0xFF6b7280);
    }
  }

  Color _getRankColor(int index) {
    switch (index) {
      case 0:
        return const Color(0xFFfbbf24); // Gold
      case 1:
        return const Color(0xFF9ca3af); // Silver
      case 2:
        return const Color(0xFFcd7c2f); // Bronze
      default:
        return const Color(0xFF6366f1);
    }
  }

  String _formatMonth(String month) {
    if (month.length >= 7) {
      final year = month.substring(0, 4);
      final monthNum = int.tryParse(month.substring(5, 7)) ?? 1;
      final monthNames = [
        'Jan',
        'Fev',
        'Mar',
        'Abr',
        'Mai',
        'Jun',
        'Jul',
        'Ago',
        'Set',
        'Out',
        'Nov',
        'Dez',
      ];
      return '${monthNames[monthNum - 1]} $year';
    }
    return month;
  }

  String _formatDate(String dateString) {
    if (dateString.isEmpty) return 'N/A';
    try {
      final date = DateTime.parse(dateString);
      return '${date.day.toString().padLeft(2, '0')}/${date.month.toString().padLeft(2, '0')}/${date.year}';
    } catch (e) {
      return 'N/A';
    }
  }
}
