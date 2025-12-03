"""
Módulo para gerar gráficos e visualizações dos resultados de treinamento ML
"""
import os
import matplotlib
matplotlib.use('Agg')  # Backend não-interativo para servidores
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.metrics import (
    accuracy_score, 
    confusion_matrix, 
    classification_report,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Configuração de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class TrainingVisualizer:
    """Gera gráficos e visualizações dos resultados de treinamento"""
    
    def __init__(self, output_dir):
        """
        Inicializa o visualizador
        
        Args:
            output_dir: Diretório onde salvar os gráficos
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def plot_category_confusion_matrix(self, y_true, y_pred, categories, model_name="category_model"):
        """Plota matriz de confusão para modelo de categoria"""
        cm = confusion_matrix(y_true, y_pred, labels=categories)
        
        plt.figure(figsize=(14, 12))
        sns.heatmap(
            cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=categories,
            yticklabels=categories,
            cbar_kws={'label': 'Quantidade'}
        )
        plt.title(f'Matriz de Confusão - Modelo de Categoria\n{model_name}', fontsize=14, fontweight='bold')
        plt.ylabel('Categoria Real', fontsize=12)
        plt.xlabel('Categoria Predita', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        filename = os.path.join(self.output_dir, f'{self.timestamp}_confusion_matrix_category.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def plot_category_accuracy_by_class(self, y_true, y_pred, categories):
        """Plota acurácia por classe"""
        report = classification_report(y_true, y_pred, labels=categories, output_dict=True)
        
        # Extrai precisão, recall e f1-score por classe
        classes = []
        precision = []
        recall = []
        f1 = []
        
        for cat in categories:
            if cat in report:
                classes.append(cat)
                precision.append(report[cat]['precision'])
                recall.append(report[cat]['recall'])
                f1.append(report[cat]['f1-score'])
        
        # Cria DataFrame
        df = pd.DataFrame({
            'Categoria': classes,
            'Precisão': precision,
            'Recall': recall,
            'F1-Score': f1
        })
        
        # Plota
        fig, ax = plt.subplots(figsize=(14, 8))
        x = np.arange(len(classes))
        width = 0.25
        
        ax.bar(x - width, precision, width, label='Precisão', alpha=0.8)
        ax.bar(x, recall, width, label='Recall', alpha=0.8)
        ax.bar(x + width, f1, width, label='F1-Score', alpha=0.8)
        
        ax.set_xlabel('Categoria', fontsize=12)
        ax.set_ylabel('Score', fontsize=12)
        ax.set_title('Métricas por Categoria - Modelo de Classificação', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(classes, rotation=45, ha='right')
        ax.legend()
        ax.set_ylim([0, 1.1])
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        filename = os.path.join(self.output_dir, f'{self.timestamp}_metrics_by_category.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def plot_price_prediction_scatter(self, y_true, y_pred, model_name="price_model"):
        """Plota gráfico de dispersão: valores reais vs preditos (preço)"""
        plt.figure(figsize=(10, 8))
        
        # Scatter plot
        plt.scatter(y_true, y_pred, alpha=0.5, s=50)
        
        # Linha perfeita (y=x)
        min_val = min(min(y_true), min(y_pred))
        max_val = max(max(y_true), max(y_pred))
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Predição Perfeita')
        
        # Calcula métricas
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        
        plt.xlabel('Preço Real (R$)', fontsize=12)
        plt.ylabel('Preço Predito (R$)', fontsize=12)
        plt.title(
            f'Valores Reais vs Preditos - Modelo de Preço\n'
            f'MAE: R$ {mae:.2f} | RMSE: R$ {rmse:.2f} | R²: {r2:.4f}',
            fontsize=14, 
            fontweight='bold'
        )
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        filename = os.path.join(self.output_dir, f'{self.timestamp}_scatter_price.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def plot_price_error_distribution(self, y_true, y_pred):
        """Plota distribuição dos erros de predição de preço"""
        errors = y_pred - y_true
        errors_percent = (errors / y_true) * 100
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Distribuição de erros absolutos
        axes[0].hist(errors, bins=50, edgecolor='black', alpha=0.7)
        axes[0].axvline(0, color='r', linestyle='--', linewidth=2, label='Erro Zero')
        axes[0].set_xlabel('Erro (R$)', fontsize=11)
        axes[0].set_ylabel('Frequência', fontsize=11)
        axes[0].set_title('Distribuição dos Erros Absolutos', fontsize=12, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Distribuição de erros percentuais
        axes[1].hist(errors_percent, bins=50, edgecolor='black', alpha=0.7, color='orange')
        axes[1].axvline(0, color='r', linestyle='--', linewidth=2, label='Erro Zero')
        axes[1].set_xlabel('Erro Percentual (%)', fontsize=11)
        axes[1].set_ylabel('Frequência', fontsize=11)
        axes[1].set_title('Distribuição dos Erros Percentuais', fontsize=12, fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        filename = os.path.join(self.output_dir, f'{self.timestamp}_error_distribution_price.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def plot_price_by_category(self, dados, y_pred, y_true=None):
        """Plota distribuição de preços por categoria"""
        df = pd.DataFrame({
            'category': dados['categories'],
            'price_true': dados['prices'] if y_true is None else y_true,
            'price_pred': y_pred
        })
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Box plot de preços reais por categoria
        categories_order = df['category'].unique()
        df_melted = df.melt(
            id_vars='category',
            value_vars=['price_true', 'price_pred'],
            var_name='Tipo',
            value_name='Preço'
        )
        
        sns.boxplot(data=df, x='category', y='price_true', ax=axes[0], order=categories_order)
        axes[0].set_title('Distribuição de Preços Reais por Categoria', fontsize=12, fontweight='bold')
        axes[0].set_xlabel('Categoria', fontsize=11)
        axes[0].set_ylabel('Preço (R$)', fontsize=11)
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].grid(True, alpha=0.3)
        
        sns.boxplot(data=df, x='category', y='price_pred', ax=axes[1], order=categories_order)
        axes[1].set_title('Distribuição de Preços Preditos por Categoria', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Categoria', fontsize=11)
        axes[1].set_ylabel('Preço (R$)', fontsize=11)
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        filename = os.path.join(self.output_dir, f'{self.timestamp}_price_by_category.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def plot_training_summary(self, metrics):
        """Plota resumo visual das métricas de treinamento"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Métricas de Categoria
        if 'category_accuracy' in metrics:
            ax = axes[0, 0]
            ax.barh(['Acurácia'], [metrics['category_accuracy']], color='steelblue', alpha=0.8)
            ax.set_xlim([0, 1])
            ax.set_xlabel('Score', fontsize=11)
            ax.set_title(f'Acurácia - Categoria\n{metrics["category_accuracy"]:.4f}', 
                        fontsize=12, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            # Adiciona linha de threshold
            if metrics['category_accuracy'] >= 0.6:
                ax.axvline(0.6, color='green', linestyle='--', linewidth=2, label='Threshold (60%)')
            else:
                ax.axvline(0.6, color='red', linestyle='--', linewidth=2, label='Threshold (60%)')
            ax.legend()
        
        # 2. Métricas de Preço - MAE
        if 'price_mae' in metrics:
            ax = axes[0, 1]
            ax.barh(['MAE'], [metrics['price_mae']], color='coral', alpha=0.8)
            ax.set_xlabel('Erro Médio (R$)', fontsize=11)
            ax.set_title(f'MAE - Preço\nR$ {metrics["price_mae"]:.2f}', 
                        fontsize=12, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            # Adiciona linha de threshold
            if metrics['price_mae'] <= 200:
                ax.axvline(200, color='green', linestyle='--', linewidth=2, label='Threshold (R$ 200)')
            else:
                ax.axvline(200, color='red', linestyle='--', linewidth=2, label='Threshold (R$ 200)')
            ax.legend()
        
        # 3. Métricas de Preço - R²
        if 'price_r2' in metrics:
            ax = axes[1, 0]
            ax.barh(['R²'], [metrics['price_r2']], color='mediumseagreen', alpha=0.8)
            ax.set_xlim([0, 1])
            ax.set_xlabel('Score', fontsize=11)
            ax.set_title(f'R² - Preço\n{metrics["price_r2"]:.4f}', 
                        fontsize=12, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            # Adiciona linha de threshold
            if metrics['price_r2'] >= 0.4:
                ax.axvline(0.4, color='green', linestyle='--', linewidth=2, label='Threshold (0.40)')
            else:
                ax.axvline(0.4, color='red', linestyle='--', linewidth=2, label='Threshold (0.40)')
            ax.legend()
        
        # 4. Métricas de Preço - RMSE
        if 'price_rmse' in metrics:
            ax = axes[1, 1]
            ax.barh(['RMSE'], [metrics['price_rmse']], color='indianred', alpha=0.8)
            ax.set_xlabel('Erro (R$)', fontsize=11)
            ax.set_title(f'RMSE - Preço\nR$ {metrics["price_rmse"]:.2f}', 
                        fontsize=12, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            # Adiciona linha de threshold
            if metrics['price_rmse'] <= 300:
                ax.axvline(300, color='green', linestyle='--', linewidth=2, label='Threshold (R$ 300)')
            else:
                ax.axvline(300, color='red', linestyle='--', linewidth=2, label='Threshold (R$ 300)')
            ax.legend()
        
        plt.suptitle('Resumo das Métricas de Treinamento', fontsize=16, fontweight='bold', y=0.995)
        plt.tight_layout()
        filename = os.path.join(self.output_dir, f'{self.timestamp}_training_summary.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def generate_report(self, metrics, model_info, output_file=None):
        """Gera relatório em texto dos resultados"""
        if output_file is None:
            output_file = os.path.join(self.output_dir, f'{self.timestamp}_training_report.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("RELATÓRIO DE TREINAMENTO - MODELOS DE MACHINE LEARNING\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Data/Hora do Treinamento: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("INFORMAÇÕES DOS MODELOS\n")
            f.write("-" * 70 + "\n")
            for key, value in model_info.items():
                f.write(f"{key}: {value}\n")
            f.write("\n")
            
            f.write("MÉTRICAS DE PERFORMANCE\n")
            f.write("-" * 70 + "\n")
            
            if 'category_accuracy' in metrics:
                f.write(f"\nMODELO DE CATEGORIA:\n")
                f.write(f"  - Acurácia: {metrics['category_accuracy']:.4f} ({metrics['category_accuracy']*100:.2f}%)\n")
                status = "✓ APROVADO" if metrics['category_accuracy'] >= 0.6 else "✗ REPROVADO"
                f.write(f"  - Status: {status} (Threshold: 60%)\n")
            
            if any(k.startswith('price_') for k in metrics.keys()):
                f.write(f"\nMODELO DE PREÇO:\n")
                if 'price_mae' in metrics:
                    f.write(f"  - MAE (Mean Absolute Error): R$ {metrics['price_mae']:.2f}\n")
                    status = "✓ APROVADO" if metrics['price_mae'] <= 200 else "✗ REPROVADO"
                    f.write(f"    Status: {status} (Threshold: R$ 200.00)\n")
                
                if 'price_rmse' in metrics:
                    f.write(f"  - RMSE (Root Mean Squared Error): R$ {metrics['price_rmse']:.2f}\n")
                    status = "✓ APROVADO" if metrics['price_rmse'] <= 300 else "✗ REPROVADO"
                    f.write(f"    Status: {status} (Threshold: R$ 300.00)\n")
                
                if 'price_r2' in metrics:
                    f.write(f"  - R² (Coeficiente de Determinação): {metrics['price_r2']:.4f}\n")
                    status = "✓ APROVADO" if metrics['price_r2'] >= 0.4 else "✗ REPROVADO"
                    f.write(f"    Status: {status} (Threshold: 0.40)\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("ARQUIVOS GERADOS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Diretório de resultados: {self.output_dir}\n")
            f.write(f"Timestamp: {self.timestamp}\n")
            f.write("\n")
            f.write("Gráficos gerados:\n")
            f.write("  - Matriz de confusão (categoria)\n")
            f.write("  - Métricas por categoria\n")
            f.write("  - Scatter plot (preço)\n")
            f.write("  - Distribuição de erros (preço)\n")
            f.write("  - Resumo das métricas\n")
            
        return output_file

