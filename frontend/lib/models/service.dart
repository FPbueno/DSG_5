class Service {
  final int id;
  final String name;
  final double unitPrice;
  final String unit;
  final DateTime createdAt;
  final DateTime updatedAt;

  Service({
    required this.id,
    required this.name,
    required this.unitPrice,
    required this.unit,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Service.fromJson(Map<String, dynamic> json) {
    return Service(
      id: json['id'],
      name: json['name'],
      unitPrice: (json['unit_price'] as num).toDouble(),
      unit: json['unit'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'unit_price': unitPrice,
      'unit': unit,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

class ServiceCreate {
  final String name;
  final double unitPrice;
  final String unit;

  ServiceCreate({required this.name, required this.unitPrice, this.unit = "h"});

  Map<String, dynamic> toJson() {
    return {'name': name, 'unit_price': unitPrice, 'unit': unit};
  }
}

class ServiceUpdate {
  final String? name;
  final double? unitPrice;
  final String? unit;

  ServiceUpdate({this.name, this.unitPrice, this.unit});

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    if (name != null) json['name'] = name;
    if (unitPrice != null) json['unit_price'] = unitPrice;
    if (unit != null) json['unit'] = unit;
    return json;
  }
}
