class SimpleQuote {
  final String clientName;
  final String requestDate;
  final String serviceCategory;
  final String serviceSubcategory;
  final Map<String, dynamic>? aiResponse;

  SimpleQuote({
    required this.clientName,
    required this.requestDate,
    required this.serviceCategory,
    required this.serviceSubcategory,
    this.aiResponse,
  });

  Map<String, dynamic> toJson() {
    return {
      'client_name': clientName,
      'request_date': requestDate,
      'service_category': serviceCategory,
      'service_subcategory': serviceSubcategory,
      'ai_response': aiResponse,
    };
  }

  factory SimpleQuote.fromJson(Map<String, dynamic> json) {
    return SimpleQuote(
      clientName: json['client_name'] ?? '',
      requestDate: json['request_date'] ?? '',
      serviceCategory: json['service_category'] ?? '',
      serviceSubcategory: json['service_subcategory'] ?? '',
      aiResponse: json['ai_response'],
    );
  }
}
