class Client {
  final int id;
  final String name;
  final DateTime createdAt;
  final DateTime updatedAt;

  Client({
    required this.id,
    required this.name,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Client.fromJson(Map<String, dynamic> json) {
    return Client(
      id: json['id'],
      name: json['name'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

class ClientCreate {
  final String name;

  ClientCreate({required this.name});

  Map<String, dynamic> toJson() {
    return {'name': name};
  }
}

class ClientUpdate {
  final String? name;

  ClientUpdate({this.name});

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    if (name != null) json['name'] = name;
    return json;
  }
}
