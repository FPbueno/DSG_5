import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:encrypt/encrypt.dart';
import '../constants/app_constants.dart';

class RSAService {
  static String? _cachedPublicKey;

  static Future<String> getPublicKey() async {
    if (_cachedPublicKey != null) {
      return _cachedPublicKey!;
    }

    try {
      final response = await http.get(
        Uri.parse('${AppConstants.baseUrl}/public-key'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _cachedPublicKey = data['public_key'] as String;
        return _cachedPublicKey!;
      } else {
        throw Exception('Erro ao buscar chave pública');
      }
    } catch (e) {
      throw Exception('Erro ao conectar com servidor: $e');
    }
  }

  static Future<String> encryptPassword(String password) async {
    try {
      final publicKeyPem = await getPublicKey();

      final publicKey = RSAKeyParser().parse(publicKeyPem);

      final encrypter = Encrypter(RSA(publicKey: publicKey as dynamic));

      final encrypted = encrypter.encrypt(password);

      return encrypted.base64;
    } catch (e) {
      throw Exception('Erro ao criptografar senha: $e');
    }
  }

  static void clearCache() {
    _cachedPublicKey = null;
  }
}
