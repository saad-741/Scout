class SearchFilter {
  final String? role;
  final String? location;
  final List<String> workTypes;
  final String? experienceLevel;
  final List<String> skills;
  final String datePosted;
  final bool forceRefresh;

  SearchFilter({
    required this.role,
    required this.location,
    this.workTypes = const [],
    this.experienceLevel = 'Any',
    this.skills = const [],
    this.datePosted = 'any',
    this.forceRefresh = false,
  });

  Map<String, dynamic> toJson() {
    // 1. Date posted mapping
    String formattedDatePosted = 'any';
    final lowerDate = datePosted.toLowerCase();
    if (lowerDate.contains('24')) {
      formattedDatePosted = '24h';
    } else if (lowerDate.contains('week')) {
      formattedDatePosted = 'week';
    } else if (lowerDate.contains('month')) {
      formattedDatePosted = 'month';
    }

    final Map<String, dynamic> data = {
      'role': role ?? '',
      'location': location ?? '',
      'date_posted': formattedDatePosted,
      'force_refresh': forceRefresh,
    };

    // 2. Keep exact work types 'Remote', 'Hybrid', 'On-site'
    if (workTypes.isNotEmpty) {
      data['work_types'] = workTypes;
    }
 
    if (experienceLevel != null && experienceLevel != 'Any') {
      String mappedExp = experienceLevel!;
      if (experienceLevel == 'Mid Level') {
        mappedExp = 'Mid-Senior';
      } else if (experienceLevel == 'Senior Level') {
        mappedExp = 'Mid-Senior';
      }

      data['experience_levels'] = [mappedExp];
    }

    if (skills.isNotEmpty) {
      data['skills'] = skills;
    }

    return data;
  }
}
 