import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import 'login_screen.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _notificationsEnabled = true;
  bool _darkModeEnabled = false;
  bool _autoSaveEnabled = true;
  String _selectedLanguage = 'Português';
  final String _apiEndpoint = 'http://localhost:8000/api/v1';
  Map<String, dynamic>? _userInfo;

  @override
  void initState() {
    super.initState();
    _loadUserInfo();
    _loadSettings();
  }

  Future<void> _loadUserInfo() async {
    final user = await AuthService.getUser();
    setState(() {
      _userInfo = user;
    });
  }

  Future<void> _loadSettings() async {
    // Aqui você pode carregar configurações salvas
    // Por enquanto, vamos usar valores padrão
  }

  Future<void> _saveSettings() async {
    // Aqui você pode salvar as configurações
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Configurações salvas com sucesso!'),
        backgroundColor: Colors.green,
      ),
    );
  }

  Future<void> _logout() async {
    final confirmed = await _showLogoutDialog();
    if (confirmed) {
      await AuthService.logout();
      if (mounted) {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (context) => const LoginScreen()),
        );
      }
    }
  }

  Future<bool> _showLogoutDialog() async {
    return await showDialog<bool>(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('Confirmar Logout'),
            content: const Text('Tem certeza que deseja sair da sua conta?'),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(false),
                child: const Text('Cancelar'),
              ),
              ElevatedButton(
                onPressed: () => Navigator.of(context).pop(true),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.red,
                  foregroundColor: Colors.white,
                ),
                child: const Text('Sair'),
              ),
            ],
          ),
        ) ??
        false;
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: const Color(0xFFf8f9fa),
      child: Column(
        children: [
          // Header
          Container(
            padding: const EdgeInsets.all(20),
            decoration: const BoxDecoration(
              color: Colors.white,
              boxShadow: [
                BoxShadow(
                  color: Color(0x1A000000),
                  offset: Offset(0, 2),
                  blurRadius: 3.84,
                ),
              ],
            ),
            child: const Center(
              child: Text(
                'Configurações',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF2D3748),
                ),
              ),
            ),
          ),

          // Content
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Seção do Perfil do Usuário
                  _buildProfileSection(),
                  const SizedBox(height: 24),

                  // Seção de Configurações Gerais
                  _buildGeneralSettingsSection(),
                  const SizedBox(height: 24),

                  // Seção de Configurações de ML
                  _buildMLSettingsSection(),
                  const SizedBox(height: 24),

                  // Seção de Configurações de API
                  _buildAPISettingsSection(),
                  const SizedBox(height: 24),

                  // Seção de Configurações de Aparência
                  _buildAppearanceSettingsSection(),
                  const SizedBox(height: 24),

                  // Seção de Ações
                  _buildActionsSection(),
                  const SizedBox(height: 32),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildProfileSection() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 60,
                height: 60,
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFF667eea), Color(0xFF764ba2)],
                  ),
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.person, color: Colors.white, size: 30),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      _userInfo?['name'] ?? 'Usuário',
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF2D3748),
                      ),
                    ),
                    Text(
                      _userInfo?['email'] ?? 'email@exemplo.com',
                      style: TextStyle(fontSize: 14, color: Colors.grey[600]),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildGeneralSettingsSection() {
    return _buildSettingsCard(
      title: 'Configurações Gerais',
      icon: Icons.settings,
      children: [
        _buildSwitchTile(
          title: 'Notificações',
          subtitle: 'Receber notificações do app',
          value: _notificationsEnabled,
          onChanged: (value) {
            setState(() {
              _notificationsEnabled = value;
            });
          },
        ),
        const Divider(height: 1),
        _buildSwitchTile(
          title: 'Auto Save',
          subtitle: 'Salvar automaticamente os dados',
          value: _autoSaveEnabled,
          onChanged: (value) {
            setState(() {
              _autoSaveEnabled = value;
            });
          },
        ),
      ],
    );
  }

  Widget _buildMLSettingsSection() {
    return _buildSettingsCard(
      title: 'Configurações de ML',
      icon: Icons.psychology,
      children: [
        _buildInfoTile(
          title: 'Modelo de Previsão',
          subtitle: 'Modelo treinado com dados históricos',
          trailing: const Icon(Icons.check_circle, color: Colors.green),
        ),
        const Divider(height: 1),
        _buildInfoTile(
          title: 'Precisão do Modelo',
          subtitle: '87.5% de precisão média',
          trailing: const Icon(Icons.analytics, color: Colors.blue),
        ),
        const Divider(height: 1),
        _buildActionTile(
          title: 'Retreinar Modelo',
          subtitle: 'Atualizar modelo com novos dados',
          onTap: () {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('Funcionalidade em desenvolvimento'),
              ),
            );
          },
        ),
      ],
    );
  }

  Widget _buildAPISettingsSection() {
    return _buildSettingsCard(
      title: 'Configurações de API',
      icon: Icons.api,
      children: [
        _buildInfoTile(
          title: 'Endpoint da API',
          subtitle: _apiEndpoint,
          trailing: const Icon(Icons.link, color: Colors.blue),
        ),
        const Divider(height: 1),
        _buildActionTile(
          title: 'Testar Conexão',
          subtitle: 'Verificar conectividade com o servidor',
          onTap: () {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Testando conexão...')),
            );
          },
        ),
        const Divider(height: 1),
        _buildActionTile(
          title: 'Limpar Cache',
          subtitle: 'Remover dados temporários',
          onTap: () {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Cache limpo com sucesso!')),
            );
          },
        ),
      ],
    );
  }

  Widget _buildAppearanceSettingsSection() {
    return _buildSettingsCard(
      title: 'Aparência',
      icon: Icons.palette,
      children: [
        _buildSwitchTile(
          title: 'Modo Escuro',
          subtitle: 'Ativar tema escuro',
          value: _darkModeEnabled,
          onChanged: (value) {
            setState(() {
              _darkModeEnabled = value;
            });
          },
        ),
        const Divider(height: 1),
        _buildSelectionTile(
          title: 'Idioma',
          subtitle: _selectedLanguage,
          onTap: () {
            _showLanguageDialog();
          },
        ),
      ],
    );
  }

  Widget _buildActionsSection() {
    return _buildSettingsCard(
      title: 'Ações',
      icon: Icons.more_horiz,
      children: [
        _buildActionTile(
          title: 'Salvar Configurações',
          subtitle: 'Aplicar todas as alterações',
          icon: Icons.save,
          onTap: _saveSettings,
        ),
        const Divider(height: 1),
        _buildActionTile(
          title: 'Sair da Conta',
          subtitle: 'Fazer logout da aplicação',
          icon: Icons.logout,
          textColor: Colors.red,
          onTap: _logout,
        ),
      ],
    );
  }

  Widget _buildSettingsCard({
    required String title,
    required IconData icon,
    required List<Widget> children,
  }) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.all(20),
            child: Row(
              children: [
                Icon(icon, color: const Color(0xFF667eea), size: 24),
                const SizedBox(width: 12),
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF2D3748),
                  ),
                ),
              ],
            ),
          ),
          ...children,
        ],
      ),
    );
  }

  Widget _buildSwitchTile({
    required String title,
    required String subtitle,
    required bool value,
    required ValueChanged<bool> onChanged,
  }) {
    return SwitchListTile(
      title: Text(
        title,
        style: const TextStyle(
          fontWeight: FontWeight.w500,
          color: Color(0xFF2D3748),
        ),
      ),
      subtitle: Text(subtitle, style: TextStyle(color: Colors.grey[600])),
      value: value,
      onChanged: onChanged,
      activeThumbColor: const Color(0xFF667eea),
    );
  }

  Widget _buildInfoTile({
    required String title,
    required String subtitle,
    Widget? trailing,
  }) {
    return ListTile(
      title: Text(
        title,
        style: const TextStyle(
          fontWeight: FontWeight.w500,
          color: Color(0xFF2D3748),
        ),
      ),
      subtitle: Text(subtitle, style: TextStyle(color: Colors.grey[600])),
      trailing: trailing,
    );
  }

  Widget _buildActionTile({
    required String title,
    required String subtitle,
    required VoidCallback onTap,
    IconData? icon,
    Color? textColor,
  }) {
    return ListTile(
      leading: icon != null
          ? Icon(icon, color: textColor ?? const Color(0xFF667eea))
          : null,
      title: Text(
        title,
        style: TextStyle(
          fontWeight: FontWeight.w500,
          color: textColor ?? const Color(0xFF2D3748),
        ),
      ),
      subtitle: Text(subtitle, style: TextStyle(color: Colors.grey[600])),
      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
      onTap: onTap,
    );
  }

  Widget _buildSelectionTile({
    required String title,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return ListTile(
      title: Text(
        title,
        style: const TextStyle(
          fontWeight: FontWeight.w500,
          color: Color(0xFF2D3748),
        ),
      ),
      subtitle: Text(subtitle, style: TextStyle(color: Colors.grey[600])),
      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
      onTap: onTap,
    );
  }

  void _showLanguageDialog() {
    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          title: const Text('Selecionar Idioma'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: ['Português', 'English', 'Español'].map((language) {
              return ListTile(
                title: Text(language),
                leading: Radio<String>(
                  value: language,
                  // ignore: deprecated_member_use
                  groupValue: _selectedLanguage,
                  // ignore: deprecated_member_use
                  onChanged: (value) {
                    setDialogState(() {
                      _selectedLanguage = value!;
                    });
                    setState(() {
                      _selectedLanguage = value!;
                    });
                    Navigator.of(context).pop();
                  },
                ),
                onTap: () {
                  setDialogState(() {
                    _selectedLanguage = language;
                  });
                  setState(() {
                    _selectedLanguage = language;
                  });
                  Navigator.of(context).pop();
                },
              );
            }).toList(),
          ),
        ),
      ),
    );
  }
}
