import 'package:go_router/go_router.dart';
import '../features/search/search_screen.dart';
import '../features/jobs/job_list_screen.dart';
import '../features/job_details/job_details_screen.dart';

final appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(path: '/', builder: (context, state) => const SearchScreen()),
    GoRoute(path: '/jobs', builder: (context, state) => const JobListScreen()),
    GoRoute(
      path: '/jobs/:id',
      builder: (context, state) {
        final jobId = state.pathParameters['id']!;
        return JobDetailsScreen(jobId: jobId);
      },
    ),
  ],
);

