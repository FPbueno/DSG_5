class Cliente {
  final int id;
  final String nome;
  final String email;
  final String? telefone;
  final String? endereco;
  final double avaliacaoMedia;

  Cliente({
    required this.id,
    required this.nome,
    required this.email,
    this.telefone,
    this.endereco,
    this.avaliacaoMedia = 0.0,
  });

  factory Cliente.fromJson(Map<String, dynamic> json) {
    return Cliente(
      id: json['id'],
      nome: json['nome'],
      email: json['email'],
      telefone: json['telefone'],
      endereco: json['endereco'],
      avaliacaoMedia: (json['avaliacao_media'] ?? 0.0).toDouble(),
    );
  }
}

class Prestador {
  final int id;
  final String nome;
  final String email;
  final String? telefone;
  final List<String> categorias;
  final List<String> regioesAtendimento;
  final double avaliacaoMedia;
  final List<Map<String, dynamic>>? portfolio;

  Prestador({
    required this.id,
    required this.nome,
    required this.email,
    this.telefone,
    required this.categorias,
    required this.regioesAtendimento,
    this.avaliacaoMedia = 0.0,
    this.portfolio,
  });

  factory Prestador.fromJson(Map<String, dynamic> json) {
    return Prestador(
      id: json['id'],
      nome: json['nome'],
      email: json['email'],
      telefone: json['telefone'],
      categorias: List<String>.from(json['categorias'] ?? []),
      regioesAtendimento: List<String>.from(json['regioes_atendimento'] ?? []),
      avaliacaoMedia: (json['avaliacao_media'] ?? 0.0).toDouble(),
      portfolio: json['portfolio'] != null
          ? List<Map<String, dynamic>>.from(json['portfolio'])
          : null,
    );
  }
}
