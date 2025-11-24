import 'client.dart';

class QuoteItem {
  final int id;
  final int serviceId;
  final double quantity;
  final double unitPrice;
  final double totalPrice;
  final String serviceName;
  final String serviceUnit;

  QuoteItem({
    required this.id,
    required this.serviceId,
    required this.quantity,
    required this.unitPrice,
    required this.totalPrice,
    required this.serviceName,
    required this.serviceUnit,
  });

  factory QuoteItem.fromJson(Map<String, dynamic> json) {
    return QuoteItem(
      id: json['id'],
      serviceId: json['service_id'],
      quantity: (json['quantity'] as num).toDouble(),
      unitPrice: (json['unit_price'] as num).toDouble(),
      totalPrice: (json['total_price'] as num).toDouble(),
      serviceName: json['service_name'],
      serviceUnit: json['service_unit'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'service_id': serviceId,
      'quantity': quantity,
      'unit_price': unitPrice,
      'total_price': totalPrice,
      'service_name': serviceName,
      'service_unit': serviceUnit,
    };
  }
}

class QuoteItemCreate {
  final int serviceId;
  final double quantity;
  final double unitPrice;

  QuoteItemCreate({
    required this.serviceId,
    required this.quantity,
    required this.unitPrice,
  });

  Map<String, dynamic> toJson() {
    return {
      'service_id': serviceId,
      'quantity': quantity,
      'unit_price': unitPrice,
    };
  }
}

class Quote {
  final int id;
  final String quoteNumber;
  final int clientId;
  final String title;
  final String? description;
  final String status;
  final double total;
  final DateTime createdAt;
  final DateTime updatedAt;
  final Client client;
  final List<QuoteItem> items;

  Quote({
    required this.id,
    required this.quoteNumber,
    required this.clientId,
    required this.title,
    this.description,
    required this.status,
    required this.total,
    required this.createdAt,
    required this.updatedAt,
    required this.client,
    required this.items,
  });

  factory Quote.fromJson(Map<String, dynamic> json) {
    return Quote(
      id: json['id'],
      quoteNumber: json['quote_number'],
      clientId: json['client_id'],
      title: json['title'],
      description: json['description'],
      status: (json['status'] as String).toLowerCase(),
      total: (json['total'] as num).toDouble(),
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
      client: Client.fromJson(json['client']),
      items: (json['items'] as List)
          .map((item) => QuoteItem.fromJson(item))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'quote_number': quoteNumber,
      'client_id': clientId,
      'title': title,
      'description': description,
      'status': status,
      'total': total,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'client': client.toJson(),
      'items': items.map((item) => item.toJson()).toList(),
    };
  }
}

class QuoteCreate {
  final int clientId;
  final String title;
  final String? description;
  final String? status;
  final List<QuoteItemCreate> items;

  QuoteCreate({
    required this.clientId,
    required this.title,
    this.description,
    this.status = "draft",
    this.items = const [],
  });

  Map<String, dynamic> toJson() {
    return {
      'client_id': clientId,
      'title': title,
      'description': description,
      'status': status,
      'items': items.map((item) => item.toJson()).toList(),
    };
  }
}

class QuoteUpdate {
  final String? title;
  final String? description;
  final String? status;
  final List<QuoteItemCreate>? items;

  QuoteUpdate({this.title, this.description, this.status, this.items});

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    if (title != null) json['title'] = title;
    if (description != null) json['description'] = description;
    if (status != null) json['status'] = status;
    if (items != null) {
      json['items'] = items!.map((item) => item.toJson()).toList();
    }
    return json;
  }
}
