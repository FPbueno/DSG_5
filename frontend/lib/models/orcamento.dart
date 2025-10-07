class Orcamento {
  final int id;
  final int solicitacaoId;
  final int prestadorId;
  final double? valorMlMinimo;
  final double? valorMlSugerido;
  final double? valorMlMaximo;
  final double valorProposto;
  final String prazoExecucao;
  final String? observacoes;
  final String? condicoes;
  final String status;
  final DateTime createdAt;
  final String? prestadorNome;
  final double? prestadorAvaliacao;
  final String? categoria;
  final String? descricao;

  Orcamento({
    required this.id,
    required this.solicitacaoId,
    required this.prestadorId,
    this.valorMlMinimo,
    this.valorMlSugerido,
    this.valorMlMaximo,
    required this.valorProposto,
    required this.prazoExecucao,
    this.observacoes,
    this.condicoes,
    required this.status,
    required this.createdAt,
    this.prestadorNome,
    this.prestadorAvaliacao,
    this.categoria,
    this.descricao,
  });

  factory Orcamento.fromJson(Map<String, dynamic> json) {
    return Orcamento(
      id: json['id'],
      solicitacaoId: json['solicitacao_id'],
      prestadorId: json['prestador_id'],
      valorMlMinimo: json['valor_ml_minimo']?.toDouble(),
      valorMlSugerido: json['valor_ml_sugerido']?.toDouble(),
      valorMlMaximo: json['valor_ml_maximo']?.toDouble(),
      valorProposto: json['valor_proposto'].toDouble(),
      prazoExecucao: json['prazo_execucao'],
      observacoes: json['observacoes'],
      condicoes: json['condicoes'],
      status: (json['status'] as String).toLowerCase(),
      createdAt: DateTime.parse(json['created_at']),
      prestadorNome: json['prestador_nome'],
      prestadorAvaliacao: json['prestador_avaliacao']?.toDouble(),
      categoria: json['categoria'],
      descricao: json['descricao'],
    );
  }

  String get statusFormatado {
    switch (status) {
      case 'aguardando':
        return 'Aguardando';
      case 'aceito':
        return 'Aceito';
      case 'recusado':
        return 'Recusado';
      case 'realizado':
        return 'Realizado';
      default:
        return status;
    }
  }
}

class LimitesPreco {
  final double valorMinimo;
  final double valorSugerido;
  final double valorMaximo;
  final String? categoriaPredita;

  LimitesPreco({
    required this.valorMinimo,
    required this.valorSugerido,
    required this.valorMaximo,
    this.categoriaPredita,
  });

  factory LimitesPreco.fromJson(Map<String, dynamic> json) {
    return LimitesPreco(
      valorMinimo: json['valor_minimo'].toDouble(),
      valorSugerido: json['valor_sugerido'].toDouble(),
      valorMaximo: json['valor_maximo'].toDouble(),
      categoriaPredita: json['categoria_predita'],
    );
  }
}
