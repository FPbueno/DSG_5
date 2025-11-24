import 'package:flutter/material.dart';

class AppColors {
  // Cores principais
  static const Color primary = Color(0xFFf5c116); // Amarelo
  static const Color background = Colors.black;
  static const Color cardDark = Color(0xFF1a1a1a);
  static const Color cardDarker = Color(0xFF121212);

  // Cores de status
  static const Color aguardando = Color(0xFFf5c116);
  static const Color aceito = Colors.blue;
  static const Color recusado = Colors.red;
  static const Color realizado = Colors.green;
  static const Color cancelado = Colors.red;
}

class StatusColors {
  // Cores para Status de Orçamento
  static Color getOrcamentoColor(String status) {
    switch (status) {
      case 'aguardando':
        return AppColors.aguardando;
      case 'aceito':
        return AppColors.aceito;
      case 'recusado':
        return AppColors.recusado;
      case 'realizado':
        return AppColors.realizado;
      default:
        return Colors.grey;
    }
  }

  // Cores para Status de Solicitação
  static Color getSolicitacaoColor(String status) {
    switch (status) {
      case 'aguardando_orcamentos':
        return AppColors.aguardando;
      case 'com_orcamentos':
        return AppColors.aceito;
      case 'fechada':
        return AppColors.realizado;
      case 'cancelada':
        return AppColors.cancelado;
      default:
        return Colors.grey;
    }
  }
}
