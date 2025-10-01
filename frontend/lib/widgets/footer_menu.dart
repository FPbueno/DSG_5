// ignore_for_file: deprecated_member_use

import 'package:flutter/material.dart';

class FooterMenu extends StatelessWidget {
  final String currentScreen;
  final VoidCallback onNavigateToHome;
  final VoidCallback onNavigateToHistory;
  final VoidCallback onNavigateToDashboard;
  final VoidCallback onNavigateToSettings;

  const FooterMenu({
    super.key,
    required this.currentScreen,
    required this.onNavigateToHome,
    required this.onNavigateToHistory,
    required this.onNavigateToDashboard,
    required this.onNavigateToSettings,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.black,
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(20),
          topRight: Radius.circular(20),
        ),
        boxShadow: [
          BoxShadow(
            color: Color(0xFFf5c116).withValues(alpha: 0.2),
            offset: const Offset(0, -4),
            blurRadius: 12,
            spreadRadius: 0,
          ),
        ],
      ),
      child: SafeArea(
        child: Container(
          height: 65,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _buildMenuItem(
                icon: Icons.home_outlined,
                activeIcon: Icons.home,
                label: 'Home',
                isActive: currentScreen == 'Home',
                onTap: onNavigateToHome,
              ),
              _buildMenuItem(
                icon: Icons.history_outlined,
                activeIcon: Icons.history,
                label: 'Histórico',
                isActive: currentScreen == 'History',
                onTap: onNavigateToHistory,
              ),
              _buildMenuItem(
                icon: Icons.analytics_outlined,
                activeIcon: Icons.analytics,
                label: 'Analytics',
                isActive: currentScreen == 'Dashboard',
                onTap: onNavigateToDashboard,
              ),
              _buildMenuItem(
                icon: Icons.settings_outlined,
                activeIcon: Icons.settings,
                label: 'Config',
                isActive: currentScreen == 'Settings',
                onTap: onNavigateToSettings,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMenuItem({
    required IconData icon,
    required IconData activeIcon,
    required String label,
    required bool isActive,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        curve: Curves.easeInOut,
        padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 10),
        decoration: BoxDecoration(
          color: isActive ? const Color(0xFFf5c116) : Colors.transparent,
          borderRadius: BorderRadius.circular(12),
          boxShadow: isActive
              ? [
                  BoxShadow(
                    color: const Color(0xFFf5c116).withValues(alpha: 0.3),
                    offset: const Offset(0, 2),
                    blurRadius: 8,
                    spreadRadius: 0,
                  ),
                ]
              : null,
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            AnimatedSwitcher(
              duration: const Duration(milliseconds: 200),
              child: Icon(
                isActive ? activeIcon : icon,
                key: ValueKey(isActive),
                size: 20,
                color: isActive ? Colors.black : const Color(0xFFf5c116),
              ),
            ),
            const SizedBox(height: 3),
            Text(
              label,
              style: TextStyle(
                fontSize: 10,
                fontWeight: isActive ? FontWeight.w700 : FontWeight.w600,
                color: isActive ? Colors.black : Colors.grey[400],
                letterSpacing: 0.1,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
