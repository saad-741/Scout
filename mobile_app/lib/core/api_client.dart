import 'package:dio/dio.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiClient {
  static final Dio dio = Dio(
    BaseOptions(
      baseUrl: dotenv.env['API_BASE_URL'] ?? 'http://10.0.2.2:8000/api/v1',
      connectTimeout: const Duration(seconds: 15),
      receiveTimeout: const Duration(seconds: 15),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ),
  );
}