import 'package:dio/dio.dart';
import '../core/api_client.dart';
import '../models/job_model.dart';
import '../models/search_filter.dart';

class JobApiService {
  final Dio _dio = ApiClient.dio;

  /// Fetch jobs using POST /jobs/search with dynamic filters
  Future<List<JobModel>> searchJobs(SearchFilter filter) async {
    try {
      final response = await _dio.post(
        '/jobs/search',
        data: filter.toJson(),
      );

      final dynamic rawData = response.data;
      final List<dynamic> data = (rawData is Map && rawData.containsKey('data'))
          ? rawData['data']
          : rawData;

      return data.map((item) => JobModel.fromJson(item)).toList();
    } catch (e) {
      throw Exception('Failed to fetch jobs from API: $e');
    }
  }

  /// Fetch all jobs using GET /jobs
  Future<List<JobModel>> getJobs() async {
    try {
      final response = await _dio.get('/jobs');

      final dynamic rawData = response.data;
      final List<dynamic> data = (rawData is Map && rawData.containsKey('data'))
          ? rawData['data']
          : rawData;

      return data.map((item) => JobModel.fromJson(item)).toList();
    } catch (e) {
      throw Exception('Failed to fetch jobs: $e');
    }
  }

  /// Fetch a single job details using GET /jobs/{id}
  Future<JobModel> getJobDetails(String jobId) async {
    try {
      final response = await _dio.get('/jobs/$jobId');
      
      final dynamic rawData = response.data;
      final Map<String, dynamic> data = (rawData is Map && rawData.containsKey('data'))
          ? rawData['data']
          : rawData;

      return JobModel.fromJson(data);
    } catch (e) {
      throw Exception('Failed to fetch job details for ID $jobId: $e');
    }
  }
}
 