class AppConstants {
  // Cores do Logo WorcaFlow
  static const String primaryColor = '#2196F3'; // Azul vibrante (seta superior)
  static const String secondaryColor =
      '#00BCD4'; // Azul turquesa (seta inferior)
  static const String accentColor = '#4CAF50'; // Verde (cifrão)
  static const String logoTextColor =
      '#1976D2'; // Azul escuro (texto WorcaFlow)
  static const String backgroundColor = '#f8f9fa';
  static const String cardColor = '#ffffff';
  static const String textColor = '#333333';
  static const String textSecondaryColor = '#666666';
  static const String borderColor = '#e9ecef';
  static const String shadowColor = '#000000';

  // Status colors
  static const String statusDraft = '#ff9800';
  static const String statusSent = '#2196f3';
  static const String statusApproved = '#4caf50';
  static const String statusRejected = '#f44336';

  // Fonts
  static const String primaryFont = 'Poppins';
  static const String titleFont = 'Quicksand';

  // API
  static const String apiBaseUrl =
      'https://worca-app-263d52d597b9.herokuapp.com/api/v1';
  static const String baseUrl = apiBaseUrl; // Alias para compatibilidade

  // Categorias de serviços
  static const Map<String, List<Map<String, String>>> serviceCategories = {
    'manutencao': [
      {'label': 'Eletricista', 'value': 'eletricista'},
      {'label': 'Encanador', 'value': 'encanador'},
      {'label': 'Pintor', 'value': 'pintor'},
      {'label': 'Pedreiro', 'value': 'pedreiro'},
      {'label': 'Gesseiro/Drywall', 'value': 'gesseiro'},
    ],
    'limpeza': [
      {'label': 'Faxina Residencial', 'value': 'faxina'},
      {'label': 'Jardinagem e Paisagismo', 'value': 'jardinagem'},
      {'label': 'Dedetização', 'value': 'dedetizacao'},
      {'label': 'Limpeza de Caixa d\'Água', 'value': 'caixa_agua'},
      {'label': 'Limpeza de Estofados', 'value': 'estofados'},
    ],
    'instalacoes': [
      {'label': 'Ar-condicionado', 'value': 'ar_condicionado'},
      {'label': 'Eletrodomésticos', 'value': 'eletrodomesticos'},
      {'label': 'Montagem de Móveis', 'value': 'montagem'},
      {'label': 'Câmeras e Alarmes', 'value': 'seguranca'},
      {'label': 'Serralheria e Vidraçaria', 'value': 'serralheria'},
    ],
    'gerais': [
      {'label': 'Chaveiro', 'value': 'chaveiro'},
      {'label': 'Mudanças e Fretes', 'value': 'mudancas'},
      {'label': 'Descarte de Entulho', 'value': 'descarte'},
    ],
  };

  static const List<Map<String, String>> categoryOptions = [
    {'label': '🏠 Manutenção Residencial', 'value': 'manutencao'},
    {'label': '🧹 Limpeza e Conservação', 'value': 'limpeza'},
    {'label': '❄️ Instalações e Equipamentos', 'value': 'instalacoes'},
    {'label': '🔑 Serviços Gerais', 'value': 'gerais'},
  ];

  // Status de orçamento
  static const Map<String, String> quoteStatus = {
    'draft': 'Rascunho',
    'sent': 'Enviado',
    'approved': 'Aprovado',
    'rejected': 'Rejeitado',
  };

  // Ícones por categoria
  static const Map<String, String> categoryIcons = {
    'software': '💻',
    'sistema': '💻',
    'app': '💻',
    'site': '💻',
    'consultoria': '👥',
    'assessoria': '👥',
    'equipamento': '⚙️',
    'máquina': '⚙️',
    'material': '🧱',
    'insumo': '🧱',
    'manutenção': '🔧',
    'reparo': '🔧',
    'projeto': '🏗️',
    'instalação': '🏗️',
    'treinamento': '🎓',
    'curso': '🎓',
    'marketing': '📢',
    'publicidade': '📢',
    'logística': '🚚',
    'transporte': '🚚',
  };
}
