import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/job_model.dart';
import '../models/search_filter.dart';
import '../services/job_api_service.dart';

// 1. Service Provider
final jobApiServiceProvider = Provider<JobApiService>((ref) => JobApiService());

// 2. Search Filter Notifier
class SearchFilterNotifier extends Notifier<SearchFilter?> {
  @override
  SearchFilter? build() => null;

  void updateFilter(SearchFilter filter) {
    state = filter;
  }

  void clearFilter() {
    state = null;
  }
}

final searchFilterProvider =
    NotifierProvider<SearchFilterNotifier, SearchFilter?>(
  SearchFilterNotifier.new,
);

// 3. Dynamic Hybrid Jobs Provider (Handles both GET /jobs and POST /jobs/search)
final jobSearchProvider = FutureProvider<List<JobModel>>((ref) async {
  final apiService = ref.watch(jobApiServiceProvider);
  final filter = ref.watch(searchFilterProvider);

  // If a filter is applied, run the search API; otherwise, get all jobs
  if (filter != null) {
    return await apiService.searchJobs(filter);
  } else {
    return await apiService.getJobs();
  }
});

// 4. Single Job Details 
final jobDetailsProvider =
    FutureProvider.family<JobModel, String>((ref, jobId) async {
  final apiService = ref.watch(jobApiServiceProvider);
  return await apiService.getJobDetails(jobId);
});


 