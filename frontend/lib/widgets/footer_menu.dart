// ignore_for_file: deprecated_member_use

import 'package:flutter/material.dart';

class FooterMenu extends StatelessWidget {
  final String currentScreen;
  final VoidCallback onNavigateToHome;
  final VoidCallback onNavigateToHistory;
  final VoidCallback onNavigateToDashboard;

  const FooterMenu({
    super.key,
    required this.currentScreen,
    required this.onNavigateToHome,
    required this.onNavigateToHistory,
    required this.onNavigateToDashboard,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(20),
          topRight: Radius.circular(20),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.08),
            offset: const Offset(0, -4),
            blurRadius: 12,
            spreadRadius: 0,
          ),
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            offset: const Offset(0, -1),
            blurRadius: 4,
            spreadRadius: 0,
          ),
        ],
      ),
      child: SafeArea(
        child: Container(
          height: 70,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
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
        padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 12),
        decoration: BoxDecoration(
          color: isActive ? const Color(0xFF6366f1) : Colors.transparent,
          borderRadius: BorderRadius.circular(12),
          boxShadow: isActive
              ? [
                  BoxShadow(
                    color: const Color(0xFF6366f1).withOpacity(0.3),
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
                size: 22,
                color: isActive ? Colors.white : const Color(0xFF64748b),
              ),
            ),
            const SizedBox(height: 4),
            Text(
              label,
              style: TextStyle(
                fontSize: 11,
                fontWeight: isActive ? FontWeight.w700 : FontWeight.w600,
                color: isActive ? Colors.white : const Color(0xFF64748b),
                letterSpacing: 0.2,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
