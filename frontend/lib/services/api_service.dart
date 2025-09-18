import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/client.dart';
import '../models/service.dart';
import '../models/quote.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api/v1';

  static final http.Client _client = http.Client();

  // === CLIENTES ===
  static Future<List<Client>> getAllClients() async {
    final response = await _client.get(
      Uri.parse('$baseUrl/clients'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => Client.fromJson(json)).toList();
    } else {
      throw Exception('Falha ao carregar clientes: ${response.statusCode}');
    }
  }

  static Future<Client> createClient(ClientCreate client) async {
    final response = await _client.post(
      Uri.parse('$baseUrl/clients'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(client.toJson()),
    );

    if (response.statusCode == 201) {
      return Client.fromJson(json.decode(response.body));
    } else {
      throw Exception('Falha ao criar cliente: ${response.statusCode}');
    }
  }

  // === SERVIÇOS ===
  static Future<List<Service>> getAllServices() async {
    final response = await _client.get(
      Uri.parse('$baseUrl/services'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => Service.fromJson(json)).toList();
    } else {
      throw Exception('Falha ao carregar serviços: ${response.statusCode}');
    }
  }

  static Future<Service> createService(ServiceCreate service) async {
    final response = await _client.post(
      Uri.parse('$baseUrl/services'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(service.toJson()),
    );

    if (response.statusCode == 201) {
      return Service.fromJson(json.decode(response.body));
    } else {
      throw Exception('Falha ao criar serviço: ${response.statusCode}');
    }
  }

  // === ORÇAMENTOS ===
  static Future<List<Quote>> getAllQuotes() async {
    final response = await _client.get(
      Uri.parse('$baseUrl/quotes'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => Quote.fromJson(json)).toList();
    } else {
      throw Exception('Falha ao carregar orçamentos: ${response.statusCode}');
    }
  }

  static Future<Quote> createQuote(QuoteCreate quote) async {
    final response = await _client.post(
      Uri.parse('$baseUrl/quotes'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(quote.toJson()),
    );

    if (response.statusCode == 201) {
      return Quote.fromJson(json.decode(response.body));
    } else {
      throw Exception('Falha ao criar orçamento: ${response.statusCode}');
    }
  }

  static Future<Quote> updateQuote(int id, QuoteUpdate quote) async {
    final response = await _client.put(
      Uri.parse('$baseUrl/quotes/$id'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(quote.toJson()),
    );

    if (response.statusCode == 200) {
      return Quote.fromJson(json.decode(response.body));
    } else {
      throw Exception('Falha ao atualizar orçamento: ${response.statusCode}');
    }
  }

  static Future<void> deleteQuote(int id) async {
    final response = await _client.delete(
      Uri.parse('$baseUrl/quotes/$id'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode != 204) {
      throw Exception('Falha ao excluir orçamento: ${response.statusCode}');
    }
  }

  // === FUNCIONALIDADES DE MACHINE LEARNING ===
  static Future<Map<String, dynamic>> smartCreateItem(
    String name,
    String? userDescription,
  ) async {
    final response = await _client.post(
      Uri.parse(
        '$baseUrl/ml/smart-create?name=${Uri.encodeComponent(name)}${userDescription != null ? '&user_description=${Uri.encodeComponent(userDescription)}' : ''}',
      ),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Falha ao processar ML: ${response.statusCode}');
    }
  }

  // === PREDIÇÕES DE ML ===
  static Future<Map<String, dynamic>> predictCategory(
    String serviceName,
  ) async {
    final response = await _client.get(
      Uri.parse(
        '$baseUrl/ml/predict-category?name=${Uri.encodeComponent(serviceName)}',
      ),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Falha ao predizer categoria: ${response.statusCode}');
    }
  }

  static Future<Map<String, dynamic>> predictPrice(
    String serviceName, [
    String? category,
  ]) async {
    String url =
        '$baseUrl/ml/predict-price?name=${Uri.encodeComponent(serviceName)}';
    if (category != null) {
      url += '&category=${Uri.encodeComponent(category)}';
    }

    final response = await _client.get(
      Uri.parse(url),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Falha ao predizer preço: ${response.statusCode}');
    }
  }

  static Future<Map<String, dynamic>> retrainMLModels() async {
    final response = await _client.post(
      Uri.parse('$baseUrl/ml/retrain'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Falha ao retreinar modelos: ${response.statusCode}');
    }
  }

  static Future<Map<String, dynamic>> populateTrainingData() async {
    final response = await _client.post(
      Uri.parse('$baseUrl/ml/populate-training-data'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception(
        'Falha ao popular dados de treinamento: ${response.statusCode}',
      );
    }
  }

  // === ANALYTICS ===
  static Future<Map<String, dynamic>> getAnalyticsOverview() async {
    final response = await _client.get(
      Uri.parse('$baseUrl/analytics/overview'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Falha ao carregar analytics: ${response.statusCode}');
    }
  }

  static Future<Map<String, dynamic>> getServicesAnalytics() async {
    final response = await _client.get(
      Uri.parse('$baseUrl/analytics/services'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception(
        'Falha ao carregar analytics de serviços: ${response.statusCode}',
      );
    }
  }

  static Future<Map<String, dynamic>> getClientsAnalytics() async {
    final response = await _client.get(
      Uri.parse('$baseUrl/analytics/clients'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception(
        'Falha ao carregar analytics de clientes: ${response.statusCode}',
      );
    }
  }
}
