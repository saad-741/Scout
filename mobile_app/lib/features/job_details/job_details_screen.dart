import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../providers/job_provider.dart';

class JobDetailsScreen extends ConsumerWidget {
  final String jobId;

  const JobDetailsScreen({super.key, required this.jobId});

  Future<void> _launchSourceUrl(BuildContext context, String url) async {
    final uri = Uri.parse(url);
    if (!await launchUrl(uri, mode: LaunchMode.externalApplication)) {
      if (context.mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Could not open link: $url')));
      }
    }
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final jobAsync = ref.watch(jobDetailsProvider(jobId));

    return Scaffold(
      appBar: AppBar(title: const Text('Job Detail Analysis')),
      body: jobAsync.when(
        data: (job) {
          return Column(
            children: [
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // --- Header ---
                      Text(
                        job.title,
                        style: Theme.of(context).textTheme.headlineSmall
                            ?.copyWith(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        '${job.company} • ${job.location}',
                        style: Theme.of(context).textTheme.titleMedium
                            ?.copyWith(
                              color: Colors.grey[700],
                              fontWeight: FontWeight.w500,
                            ),
                      ),
                      const SizedBox(height: 12),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: [
                          Chip(
                            label: Text(job.workType),
                            avatar: const Icon(
                              Icons.business_center_outlined,
                              size: 16,
                            ),
                          ),
                          Chip(
                            label: Text(job.employmentType),
                            avatar: const Icon(Icons.access_time, size: 16),
                          ),
                          Chip(
                            label: Text(job.experienceLevel),
                            avatar: const Icon(Icons.bar_chart, size: 16),
                          ),
                          if (job.postedDate != null)
                            Chip(
                              label: Text(job.postedDate!),
                              avatar: const Icon(
                                Icons.calendar_today,
                                size: 16,
                              ),
                            ),
                        ],
                      ),
                      const Divider(height: 32),

                      // --- AI Summary ---
                      if (job.summary != null && job.summary!.isNotEmpty) ...[
                        Row(
                          children: [
                            const Icon(
                              Icons.auto_awesome,
                              color: Colors.blue,
                              size: 20,
                            ),
                            const SizedBox(width: 8),
                            Text(
                              'AI Summary',
                              style: Theme.of(context).textTheme.titleMedium
                                  ?.copyWith(fontWeight: FontWeight.bold),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Container(
                          width: double.infinity,
                          padding: const EdgeInsets.all(14),
                          decoration: BoxDecoration(
                            color: Colors.blue.shade50,
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(color: Colors.blue.shade100),
                          ),
                          child: Text(
                            job.summary!,
                            style: TextStyle(
                              color: Colors.blue.shade900,
                              height: 1.4,
                            ),
                          ),
                        ),
                        const SizedBox(height: 24),
                      ],

                      // --- Required Skills ---
                      if (job.requiredSkills.isNotEmpty) ...[
                        Text(
                          'Required Skills',
                          style: Theme.of(context).textTheme.titleMedium
                              ?.copyWith(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        Wrap(
                          spacing: 6,
                          runSpacing: 6,
                          children: job.requiredSkills
                              .map(
                                (skill) => Chip(
                                  label: Text(skill),
                                  backgroundColor: Colors.blue.shade100,
                                  side: BorderSide.none,
                                ),
                              )
                              .toList(),
                        ),
                        const SizedBox(height: 24),
                      ],

                      // --- Nice to Have Skills ---
                      if (job.niceToHaveSkills.isNotEmpty) ...[
                        Text(
                          'Nice to Have',
                          style: Theme.of(context).textTheme.titleMedium
                              ?.copyWith(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        Wrap(
                          spacing: 6,
                          runSpacing: 6,
                          children: job.niceToHaveSkills
                              .map(
                                (skill) => Chip(
                                  label: Text(skill),
                                  backgroundColor: Colors.grey.shade200,
                                  side: BorderSide.none,
                                ),
                              )
                              .toList(),
                        ),
                        const SizedBox(height: 24),
                      ],

                      // --- Salary ---
                      if (job.salaryRange != null) ...[
                        Text(
                          'Salary',
                          style: Theme.of(context).textTheme.titleMedium
                              ?.copyWith(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 6),
                        Text(
                          job.salaryRange!,
                          style: Theme.of(context).textTheme.titleMedium
                              ?.copyWith(
                                color: Colors.green.shade700,
                                fontWeight: FontWeight.w600,
                              ),
                        ),
                        const SizedBox(height: 24),
                      ],

                      // --- Description ---
                      Text(
                        'Description',
                        style: Theme.of(context).textTheme.titleMedium
                            ?.copyWith(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        job.rawDescription,
                        style: const TextStyle(
                          height: 1.5,
                          color: Colors.black87,
                        ),
                      ),
                      const SizedBox(height: 24),
                    ],
                  ),
                ),
              ),

              // --- Sticky Bottom Action ---
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Theme.of(context).scaffoldBackgroundColor,
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.05),
                      blurRadius: 10,
                      offset: const Offset(0, -4),
                    ),
                  ],
                ),
                child: SafeArea(
                  child: SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      icon: const Icon(Icons.link),
                      label: Text('View Original Job (${job.source})'),
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        textStyle: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      onPressed: () => _launchSourceUrl(context, job.sourceUrl),
                    ),
                  ),
                ),
              ),
            ],
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stackTrace) => Center(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.error_outline, size: 48, color: Colors.red),
                const SizedBox(height: 16),
                Text(
                  'Error loading job details:\n$err',
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: Colors.red),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

 