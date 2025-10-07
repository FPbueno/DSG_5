// Categorias e subcategorias compartilhadas entre Cliente e Prestador

class Categorias {
  static const Map<String, List<String>> categoriasComSubcategorias = {
    'Manutenção': ['Pintura', 'Elétrica', 'Hidráulica', 'Pedreiro', 'Gesso'],
    'Limpeza': ['Faxina', 'Jardinagem', 'Dedetização', 'Limpeza de Estofados'],
    'Instalações': [
      'Ar-condicionado',
      'Eletrodomésticos',
      'Montagem de Móveis',
    ],
    'Outros': ['Marcenaria', 'Vidraçaria', 'Serralheria'],
  };

  static List<String> get todasSubcategorias {
    final List<String> todas = [];
    categoriasComSubcategorias.forEach((_, subcategorias) {
      todas.addAll(subcategorias);
    });
    return todas;
  }
}
