import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../models/job_model.dart';
import '../../providers/job_provider.dart';

class JobListScreen extends ConsumerWidget {
  const JobListScreen({super.key});
 
  Future<void> _handleRefresh(WidgetRef ref) async {
  ref.invalidate(jobSearchProvider);
  
  await ref.read(jobSearchProvider.future);
}

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final jobsAsync = ref.watch(jobSearchProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Available Opportunities'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh',
            onPressed: () => _handleRefresh(ref),
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () => _handleRefresh(ref),
        child: jobsAsync.when(
          data: (jobs) {
            if (jobs.isEmpty) {
              return SingleChildScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                child: SizedBox(
                  height: MediaQuery.of(context).size.height * 0.75,
                  child: Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.search_off_rounded,
                            size: 64,
                            color: Colors.grey.shade400,
                          ),
                          const SizedBox(height: 16),
                          const Text(
                            'No jobs found',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Try adjusting your search query, location, or filter preferences.',
                            textAlign: TextAlign.center,
                            style: TextStyle(color: Colors.grey.shade600),
                          ),
                          const SizedBox(height: 20),
                          OutlinedButton(
                            onPressed: () => context.pop(),
                            child: const Text('Adjust Search Criteria'),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              );
            }

            return ListView.separated(
              physics: const AlwaysScrollableScrollPhysics(),
              padding: const EdgeInsets.all(16),
              itemCount: jobs.length,
              separatorBuilder: (_, __) => const SizedBox(height: 12),
              itemBuilder: (context, index) {
                final job = jobs[index];
                return JobCard(
                  job: job,
                  onTap: () => context.push('/jobs/${job.id}'),
                );
              },
            );
          },
          loading: () => const _LoadingState(),
          error: (err, stackTrace) => SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            child: SizedBox(
              height: MediaQuery.of(context).size.height * 0.75,
              child: Center(
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(
                        Icons.error_outline_rounded,
                        size: 56,
                        color: Colors.redAccent,
                      ),
                      const SizedBox(height: 16),
                      const Text(
                        'Failed to load job listings',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        err.toString().replaceAll('Exception: ', ''),
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 13,
                          color: Colors.grey.shade700,
                        ),
                      ),
                      const SizedBox(height: 24),
                      ElevatedButton.icon(
                        icon: const Icon(Icons.refresh),
                        label: const Text('Retry Search'),
                        onPressed: () => _handleRefresh(ref),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

// Custom Detailed Job Card Component
class JobCard extends StatelessWidget {
  final JobModel job;
  final VoidCallback onTap;

  const JobCard({super.key, required this.job, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header Row: Title & Arrow
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: Text(
                      job.title,
                      style: const TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.w700,
                        color: Color(0xFF0F172A),
                      ),
                    ),
                  ),
                  const Icon(
                    Icons.arrow_forward_ios_rounded,
                    size: 16,
                    color: Color(0xFF94A3B8),
                  ),
                ],
              ),
              const SizedBox(height: 4),

              // Company Name
              Text(
                job.company,
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                  color: Color(0xFF475569),
                ),
              ),
              const SizedBox(height: 12),

              // Metadata Icons Row (Location, Work Type, Employment Type, Date)
              Wrap(
                spacing: 12,
                runSpacing: 6,
                children: [
                  _IconBadge(
                    icon: Icons.location_on_outlined,
                    label: job.location,
                  ),
                  _IconBadge(
                    icon: Icons.home_work_outlined,
                    label: job.workType,
                  ),
                  _IconBadge(
                    icon: Icons.work_outline,
                    label: job.employmentType,
                  ),
                  if (job.postedDate != null)
                    _IconBadge(icon: Icons.access_time, label: job.postedDate!),
                ],
              ),
              const SizedBox(height: 12),

              // Salary & Experience Badges
              Row(
                children: [
                  if (job.salaryRange != null &&
                      job.salaryRange!.isNotEmpty) ...[
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 4,
                      ),
                      decoration: BoxDecoration(
                        color: const Color(0xFFDCFCE7), 
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text(
                        job.salaryRange!,
                        style: const TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                          color: Color(0xFF166534),
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                  ],
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF1F5F9),  
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Text(
                      job.experienceLevel,
                      style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w500,
                        color: Color(0xFF475569),
                      ),
                    ),
                  ),
                ],
              ),

              // Skills Wrap
              if (job.requiredSkills.isNotEmpty) ...[
                const SizedBox(height: 12),
                Wrap(
                  spacing: 6,
                  runSpacing: 6,
                  children: job.requiredSkills.take(5).map((skill) {
                    return Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 3,
                      ),
                      decoration: BoxDecoration(
                        color: const Color(0xFFEFF6FF),  
                        borderRadius: BorderRadius.circular(6),
                        border: Border.all(color: const Color(0xFFBFDBFE)),
                      ),
                      child: Text(
                        skill,
                        style: const TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w500,
                          color: Color(0xFF1D4ED8),
                        ),
                      ),
                    );
                  }).toList(),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

class _IconBadge extends StatelessWidget {
  final IconData icon;
  final String label;

  const _IconBadge({required this.icon, required this.label});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, size: 14, color: const Color(0xFF64748B)),
        const SizedBox(width: 4),
        Text(
          label,
          style: const TextStyle(fontSize: 12, color: Color(0xFF64748B)),
        ),
      ],
    );
  }
}

class _LoadingState extends StatelessWidget {
  const _LoadingState();

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const CircularProgressIndicator(),
            const SizedBox(height: 20),
            const Text(
              'Scouting & Analyzing Jobs with AI...',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 8),
            Text(
              'Querying live intelligence sources and applying filters',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 13, color: Colors.grey.shade600),
            ),
          ],
        ),
      ),
    );
  }
}
 