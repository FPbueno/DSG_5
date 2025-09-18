import 'package:intl/intl.dart';
import '../constants/app_constants.dart';

class FormatUtils {
  static String formatCurrency(double value) {
    final formatter = NumberFormat.currency(
      locale: 'pt_BR',
      symbol: 'R\$',
      decimalDigits: 2,
    );
    return formatter.format(value);
  }

  static String formatDate(DateTime date) {
    return DateFormat('dd/MM/yyyy').format(date);
  }

  static String formatDateTime(DateTime date) {
    return DateFormat('dd/MM/yyyy HH:mm').format(date);
  }

  static String formatDateInput(String value) {
    // Remove tudo que não é número
    final numbers = value.replaceAll(RegExp(r'[^0-9]'), '');

    // Aplica máscara DD/MM/AAAA
    if (numbers.length <= 2) {
      return numbers;
    } else if (numbers.length <= 4) {
      return '${numbers.substring(0, 2)}/${numbers.substring(2)}';
    } else {
      return '${numbers.substring(0, 2)}/${numbers.substring(2, 4)}/${numbers.substring(4, 8)}';
    }
  }

  static DateTime? parseBRDate(String dateString) {
    if (dateString.isEmpty) return null;

    try {
      final parts = dateString.split('/');
      if (parts.length == 3) {
        final day = int.parse(parts[0]);
        final month = int.parse(parts[1]);
        final year = int.parse(parts[2]);
        return DateTime(year, month, day);
      }
    } catch (e) {
      return null;
    }
    return null;
  }

  static String convertBRDateToISO(String brDate) {
    if (brDate.isEmpty) return '';

    final parts = brDate.split('/');
    if (parts.length == 3) {
      final day = parts[0].padLeft(2, '0');
      final month = parts[1].padLeft(2, '0');
      final year = parts[2];
      return '$year-$month-$day';
    }
    return brDate;
  }

  static String getCategoryIcon(String productName) {
    final name = productName.toLowerCase();

    for (final entry in AppConstants.categoryIcons.entries) {
      if (name.contains(entry.key)) {
        return entry.value;
      }
    }

    return '📋'; // Ícone padrão
  }

  static String getStatusLabel(String status) {
    return AppConstants.quoteStatus[status] ?? status;
  }

  static String getStatusColor(String status) {
    switch (status) {
      case 'draft':
        return AppConstants.statusDraft;
      case 'sent':
        return AppConstants.statusSent;
      case 'approved':
        return AppConstants.statusApproved;
      case 'rejected':
        return AppConstants.statusRejected;
      default:
        return AppConstants.textSecondaryColor;
    }
  }
}
