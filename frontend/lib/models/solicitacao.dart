class Solicitacao {
  final int id;
  final int clienteId;
  final String categoria;
  final String descricao;
  final String localizacao;
  final String? prazoDesejado;
  final String? informacoesAdicionais;
  final String status;
  final DateTime createdAt;
  final String? clienteNome;
  final double? clienteAvaliacao;
  final int? quantidadeOrcamentos;

  Solicitacao({
    required this.id,
    required this.clienteId,
    required this.categoria,
    required this.descricao,
    required this.localizacao,
    this.prazoDesejado,
    this.informacoesAdicionais,
    required this.status,
    required this.createdAt,
    this.clienteNome,
    this.clienteAvaliacao,
    this.quantidadeOrcamentos,
  });

  factory Solicitacao.fromJson(Map<String, dynamic> json) {
    return Solicitacao(
      id: json['id'] ?? 0,
      clienteId: json['cliente_id'] ?? 0,
      categoria: json['categoria'] ?? '',
      descricao: json['descricao'] ?? '',
      localizacao: json['localizacao'] ?? '',
      prazoDesejado: json['prazo_desejado'],
      informacoesAdicionais: json['informacoes_adicionais'],
      status: (json['status'] as String? ?? 'aguardando_orcamentos')
          .toLowerCase(),
      createdAt: DateTime.tryParse(json['created_at'] ?? '') ?? DateTime.now(),
      clienteNome: json['cliente_nome'],
      clienteAvaliacao: json['cliente_avaliacao']?.toDouble(),
      quantidadeOrcamentos: json['quantidade_orcamentos'],
    );
  }

  String get statusFormatado {
    switch (status) {
      case 'aguardando_orcamentos':
        return 'Aguardando';
      case 'com_orcamentos':
        return 'Aceito';
      case 'fechada':
        return 'Realizado';
      case 'cancelada':
        return 'Cancelada';
      default:
        return status;
    }
  }
}
