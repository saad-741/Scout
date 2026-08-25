class JobModel {
  final String id;
  final String title;
  final String company;
  final String location;
  final String workType;
  final String employmentType;
  final String experienceLevel;
  final List<String> requiredSkills;
  final List<String> niceToHaveSkills;
  final String? summary;
  final String rawDescription;
  final String? salaryCurrency;
  final double? salaryMin;
  final double? salaryMax;
  final String? salaryPeriod;
  final String source;
  final String sourceUrl;
  final DateTime postedAt;

  JobModel({
    required this.id,
    required this.title,
    required this.company,
    required this.location,
    required this.workType,
    required this.employmentType,
    required this.experienceLevel,
    required this.requiredSkills,
    required this.niceToHaveSkills,
    this.summary,
    required this.rawDescription,
    this.salaryCurrency,
    this.salaryMin,
    this.salaryMax,
    this.salaryPeriod,
    required this.source,
    required this.sourceUrl,
    required this.postedAt,
  });
 

  String? get salaryRange {
    if (salaryMin == null && salaryMax == null) return null;

    final curr = salaryCurrency ?? '\$';
    final period = salaryPeriod != null ? ' / ${salaryPeriod!}' : '';
    String formatNum(double val) {
      if (val >= 1000) {
        final kVal = val / 1000;
        return '${curr}${kVal.toStringAsFixed(kVal.truncateToDouble() == kVal ? 0 : 1)}k';
      }

      return '$curr${val.toStringAsFixed(0)}';
    }

    if (salaryMin != null && salaryMax != null) {
      return '${formatNum(salaryMin!)} - ${formatNum(salaryMax!)}$period';
    } else if (salaryMin != null) {
      return 'From ${formatNum(salaryMin!)}$period';
    } else {
      return 'Up to ${formatNum(salaryMax!)}$period';
    }
  }

  // Returns a relative date string (e.g., "2d ago")

  String? get postedDate {
    final difference = DateTime.now().difference(postedAt);

    if (difference.inDays > 0) {
      return '${difference.inDays}d ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours}h ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes}m ago';
    }

    return 'Just now';
  }

  factory JobModel.fromJson(Map<String, dynamic> json) {
    return JobModel(
      id: json['id'] ?? '',
      title: json['title'] ?? '',
      company: json['company'] ?? '',
      location: json['location'] ?? '',
      workType: json['work_type'] ?? 'On-site',
      employmentType: json['employment_type'] ?? 'Full-time',
      experienceLevel: json['experience_level'] ?? 'Not Specified',
      requiredSkills: List<String>.from(json['required_skills'] ?? []),
      niceToHaveSkills: List<String>.from(json['nice_to_have_skills'] ?? []),
      summary: json['summary'],
      rawDescription: json['raw_description'] ?? '',
      salaryCurrency: json['salary_currency'],
      salaryMin: (json['salary_min'] as num?)?.toDouble(),
      salaryMax: (json['salary_max'] as num?)?.toDouble(),
      salaryPeriod: json['salary_period'],
      source: json['source'] ?? '',
      sourceUrl: json['source_url'] ?? '',
      postedAt: json['posted_at'] != null
          ? DateTime.parse(json['posted_at'])
          : DateTime.now(),
    );
  }
}
 