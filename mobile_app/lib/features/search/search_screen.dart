import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../models/search_filter.dart';
import '../../providers/job_provider.dart';

class SearchScreen extends ConsumerStatefulWidget {
  const SearchScreen({super.key});

  @override
  ConsumerState<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends ConsumerState<SearchScreen> {
  final _roleController = TextEditingController(text: 'Backend Developer');
  final _locationController = TextEditingController(text: 'Lahore');
  final _skillController = TextEditingController();

  final Set<String> _selectedWorkTypes = {'Remote', 'Hybrid'};
  String _selectedExperience = 'Entry Level';
  String _selectedDatePosted = 'Past Week';
  final List<String> _skills = ['Python', 'Django'];
  bool _forceRefresh = false;

  final List<String> _experienceOptions = [
    'Any',
    'Internship',
    'Entry Level',
    'Associate',
    'Mid-Senior',
    'Director',
    'Executive',
  ];

  final List<String> _dateOptions = [
    'Any Time',
    'Past 24 Hours',
    'Past Week',
    'Past Month',
  ];

  void _addSkill() {
    final skill = _skillController.text.trim();
    if (skill.isNotEmpty && !_skills.contains(skill)) {
      setState(() {
        _skills.add(skill);
        _skillController.clear();
      });
    }
  }

  void _removeSkill(String skill) {
    setState(() => _skills.remove(skill));
  }

  void _onSearch() {
    final roleText = _roleController.text.trim();
    if (roleText.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(10),
          ),
          content: const Text('Please specify a target job role.'),
        ),
      );
      return;
    }

    final filter = SearchFilter(
      role: roleText,
      location: _locationController.text.trim(),
      workTypes: _selectedWorkTypes.toList(),
      experienceLevel: _selectedExperience,
      skills: _skills,
      datePosted: _selectedDatePosted,
      forceRefresh: _forceRefresh,
    );

    ref.read(searchFilterProvider.notifier).updateFilter(filter);
    context.push('/jobs');
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Scout Intelligence')),
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: 18.0, vertical: 16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Find your next role',
                style: theme.textTheme.headlineMedium?.copyWith(
                  fontWeight: FontWeight.w800,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                'Specify preferences to aggregate live job listings.',
                style: theme.textTheme.bodyMedium?.copyWith(
                  color: theme.textTheme.bodyMedium?.color?.withOpacity(0.7),
                ),
              ),
              const SizedBox(height: 20),

              // Main Form Container Card
              Card(
                elevation: 0,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                  side: BorderSide(
                    color: theme.colorScheme.surfaceContainerHighest,
                  ),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Role Field
                      _buildSectionTitle('Job Role *', theme),
                      TextField(
                        controller: _roleController,
                        decoration: const InputDecoration(
                          hintText: 'e.g. Flutter Developer',
                          prefixIcon: Icon(Icons.search_rounded),
                        ),
                      ),
                      const SizedBox(height: 16),

                      // Location Field
                      _buildSectionTitle('Location', theme),
                      TextField(
                        controller: _locationController,
                        decoration: const InputDecoration(
                          hintText: 'e.g. Remote or City',
                          prefixIcon: Icon(Icons.location_on_outlined),
                        ),
                      ),
                      const SizedBox(height: 20),

                      // Work Type Chips
                      _buildSectionTitle('Work Type', theme),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: ['Remote', 'Hybrid', 'On-site'].map((type) {
                          final isSelected = _selectedWorkTypes.contains(type);
                          return FilterChip(
                            label: Text(type),
                            selected: isSelected,
                            onSelected: (selected) {
                              setState(() {
                                selected
                                    ? _selectedWorkTypes.add(type)
                                    : _selectedWorkTypes.remove(type);
                              });
                            },
                            selectedColor: theme.colorScheme.primaryContainer,
                            checkmarkColor: theme.colorScheme.primary,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(10),
                            ),
                          );
                        }).toList(),
                      ),
                      const SizedBox(height: 20),

                      // Experience Level
                      _buildSectionTitle('Experience Level', theme),
                      DropdownButtonFormField<String>(
                        value: _selectedExperience,
                        borderRadius: BorderRadius.circular(12),
                        decoration: const InputDecoration(
                          prefixIcon: Icon(Icons.work_outline_rounded),
                        ),
                        items: _experienceOptions
                            .map(
                              (e) => DropdownMenuItem(value: e, child: Text(e)),
                            )
                            .toList(),
                        onChanged: (val) =>
                            setState(() => _selectedExperience = val!),
                      ),
                      const SizedBox(height: 20),

                      // Required Skills
                      _buildSectionTitle('Required Skills', theme),
                      if (_skills.isNotEmpty) ...[
                        Wrap(
                          spacing: 8,
                          runSpacing: 8,
                          children: _skills
                              .map(
                                (skill) => Chip(
                                  label: Text(skill),
                                  deleteIcon: const Icon(Icons.close, size: 16),
                                  onDeleted: () => _removeSkill(skill),
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                ),
                              )
                              .toList(),
                        ),
                        const SizedBox(height: 10),
                      ],
                      TextField(
                        controller: _skillController,
                        decoration: InputDecoration(
                          hintText: 'Type a skill & press enter...',
                          prefixIcon: const Icon(Icons.code_rounded),
                          suffixIcon: IconButton(
                            icon: const Icon(Icons.add_circle_outline),
                            onPressed: _addSkill,
                          ),
                        ),
                        onSubmitted: (_) => _addSkill(),
                      ),
                      const SizedBox(height: 20),

                      // Date Posted
                      _buildSectionTitle('Date Posted', theme),
                      DropdownButtonFormField<String>(
                        value: _selectedDatePosted,
                        borderRadius: BorderRadius.circular(12),
                        decoration: const InputDecoration(
                          prefixIcon: Icon(Icons.calendar_today_outlined),
                        ),
                        items: _dateOptions
                            .map(
                              (d) => DropdownMenuItem(value: d, child: Text(d)),
                            )
                            .toList(),
                        onChanged: (val) =>
                            setState(() => _selectedDatePosted = val!),
                      ),
                      const SizedBox(height: 12),

                      // Cache Switch
                      SwitchListTile(
                        contentPadding: EdgeInsets.zero,
                        title: const Text(
                          'Force Live Search Refresh',
                          style: TextStyle(
                            fontWeight: FontWeight.w600,
                            fontSize: 14,
                          ),
                        ),
                        subtitle: const Text(
                          'Bypass cache and query fresh web sources',
                          style: TextStyle(fontSize: 12),
                        ),
                        value: _forceRefresh,
                        onChanged: (val) => setState(() => _forceRefresh = val),
                      ),
                      const SizedBox(height: 24),

                      // Search Button
                      ElevatedButton.icon(
                        onPressed: _onSearch,
                        icon: const Icon(Icons.search_rounded),
                        label: const Text('Search Jobs'),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionTitle(String title, ThemeData theme) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8.0),
      child: Text(
        title,
        style: theme.textTheme.titleSmall?.copyWith(
          fontWeight: FontWeight.w700,
        ),
      ),
    );
  }
}
