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

  // Filter States
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
        const SnackBar(content: Text('Please specify a target job role.')),
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

    // Update Riverpod State & Navigate to Results
    ref.read(searchFilterProvider.notifier).updateFilter(filter);
    context.push('/jobs');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Scout')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'What job are you looking for?',
              style: Theme.of(
                context,
              ).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),

            // Job Role Input
            TextField(
              controller: _roleController,
              decoration: const InputDecoration(
                labelText: 'Job Role *',
                prefixIcon: Icon(Icons.search),
              ),
            ),
            const SizedBox(height: 16),

            // Location Input
            TextField(
              controller: _locationController,
              decoration: const InputDecoration(
                labelText: 'Location',
                prefixIcon: Icon(Icons.location_on_outlined),
              ),
            ),
            const SizedBox(height: 24),

            // Work Type Checkboxes
            const Text(
              'Work Type',
              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 16),
            ),
            const SizedBox(height: 8),
            Row(
              children: ['Remote', 'Hybrid', 'On-site'].map((type) {
                final isSelected = _selectedWorkTypes.contains(type);
                return Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Checkbox(
                      value: isSelected,
                      onChanged: (val) {
                        setState(() {
                          val == true
                              ? _selectedWorkTypes.add(type)
                              : _selectedWorkTypes.remove(type);
                        });
                      },
                    ),
                    Text(type),
                    const SizedBox(width: 8),
                  ],
                );
              }).toList(),
            ),
            const SizedBox(height: 16),

            // Experience Level Dropdown
            const Text(
              'Experience Level',
              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 16),
            ),
            const SizedBox(height: 8),
            DropdownButtonFormField<String>(
              value: _selectedExperience,
              decoration: const InputDecoration(),
              items: _experienceOptions
                  .map((e) => DropdownMenuItem(value: e, child: Text(e)))
                  .toList(),
              onChanged: (val) => setState(() => _selectedExperience = val!),
            ),
            const SizedBox(height: 20),

            // Dynamic Skills Chips
            const Text(
              'Skills',
              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 16),
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                ..._skills.map(
                  (skill) => Chip(
                    label: Text(skill),
                    deleteIcon: const Icon(Icons.close, size: 18),
                    onDeleted: () => _removeSkill(skill),
                  ),
                ),
                SizedBox(
                  width: 140,
                  height: 40,
                  child: TextField(
                    controller: _skillController,
                    decoration: InputDecoration(
                      hintText: 'Add skill...',
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 10,
                      ),
                      suffixIcon: IconButton(
                        icon: const Icon(Icons.add, size: 20),
                        onPressed: _addSkill,
                      ),
                    ),
                    onSubmitted: (_) => _addSkill(),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),

            // Date Posted Dropdown
            const Text(
              'Date Posted',
              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 16),
            ),
            const SizedBox(height: 8),
            DropdownButtonFormField<String>(
              value: _selectedDatePosted,
              decoration: const InputDecoration(),
              items: _dateOptions
                  .map((d) => DropdownMenuItem(value: d, child: Text(d)))
                  .toList(),
              onChanged: (val) => setState(() => _selectedDatePosted = val!),
            ),
            const SizedBox(height: 12),

            // Bypass Cache Switch
            SwitchListTile(
              contentPadding: EdgeInsets.zero,
              title: const Text('Force Live Search Refresh'),
              subtitle: const Text('Bypass Supabase cache & query Gemini AI'),
              value: _forceRefresh,
              onChanged: (val) => setState(() => _forceRefresh = val),
            ),
            const SizedBox(height: 28),

            // Submit Button
            ElevatedButton.icon(
              onPressed: _onSearch,
              icon: const Icon(Icons.search),
              label: const Text('Find Jobs'),
            ),
          ],
        ),
      ),
    );
  }
}
