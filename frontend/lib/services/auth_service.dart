import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class AuthService {
  static const String _tokenKey = 'auth_token';
  static const String _userKey = 'user_data';
  static const String baseUrl = 'http://localhost:8000/api/v1';

  // Salva o token de autenticação
  static Future<void> saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, token);
  }

  // Recupera o token de autenticação
  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_tokenKey);
  }

  // Remove o token de autenticação
  static Future<void> removeToken() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
    await prefs.remove(_userKey);
  }

  // Salva dados do usuário
  static Future<void> saveUser(Map<String, dynamic> user) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_userKey, json.encode(user));
  }

  // Recupera dados do usuário
  static Future<Map<String, dynamic>?> getUser() async {
    final prefs = await SharedPreferences.getInstance();
    final userString = prefs.getString(_userKey);
    if (userString != null) {
      return json.decode(userString);
    }
    return null;
  }

  // Verifica se o usuário está logado
  static Future<bool> isLoggedIn() async {
    final token = await getToken();
    return token != null;
  }

  // Login do usuário
  static Future<Map<String, dynamic>> login(
    String username,
    String password,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: {'username': username, 'password': password},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final token = data['access_token'];

      // Salva o token
      await saveToken(token);

      // Busca dados do usuário
      final userResponse = await http.get(
        Uri.parse('$baseUrl/auth/me'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      );

      if (userResponse.statusCode == 200) {
        final userData = json.decode(userResponse.body);
        await saveUser(userData);
        return {'success': true, 'user': userData};
      }

      return {'success': true, 'user': null};
    } else {
      final error = json.decode(response.body);
      return {'success': false, 'error': error['detail'] ?? 'Erro no login'};
    }
  }

  // Registro do usuário
  static Future<Map<String, dynamic>> register(
    String username,
    String email,
    String password,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'username': username,
        'email': email,
        'password': password,
      }),
    );

    if (response.statusCode == 201) {
      final userData = json.decode(response.body);
      return {'success': true, 'user': userData};
    } else {
      final error = json.decode(response.body);
      return {'success': false, 'error': error['detail'] ?? 'Erro no registro'};
    }
  }

  // Logout do usuário
  static Future<void> logout() async {
    await removeToken();
  }

  // Criptografa dados
  static Future<Map<String, dynamic>> encryptData(String data) async {
    final token = await getToken();
    if (token == null) {
      throw Exception('Usuário não autenticado');
    }

    final response = await http.post(
      Uri.parse('$baseUrl/auth/encrypt'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: json.encode({'data': data}),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Erro ao criptografar dados');
    }
  }

  // Descriptografa dados
  static Future<Map<String, dynamic>> decryptData(String encryptedData) async {
    final token = await getToken();
    if (token == null) {
      throw Exception('Usuário não autenticado');
    }

    final response = await http.post(
      Uri.parse('$baseUrl/auth/decrypt'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: json.encode({'encrypted_data': encryptedData}),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Erro ao descriptografar dados');
    }
  }
}
