#!/usr/bin/env python3
"""
Healthcare Visualization Module

Provides visualization tools for healthcare productivity analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style for professional plots
plt.style.use('default')
sns.set_palette("husl")


class HealthcareVisualizer:
    """Visualization tools for healthcare analysis."""
    
    def __init__(self, output_dir: str = "results/", figsize: Tuple[int, int] = (12, 8)):
        """Initialize the visualizer.
        
        Args:
            output_dir: Directory to save plots
            figsize: Default figure size for plots
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.figsize = figsize
        
        # Color scheme for consistent visualizations
        self.colors = {
            'baseline': '#E74C3C',     # Red
            'ai_improved': '#2ECC71',  # Green
            'savings': '#3498DB',      # Blue
            'costs': '#F39C12',       # Orange
            'neutral': '#95A5A6',      # Gray
            'accent': '#9B59B6'       # Purple
        }
    
    def plot_cost_comparison(self, baseline: Dict[str, float], ai_metrics: Dict[str, float], 
                           save_path: Optional[str] = None) -> plt.Figure:
        """Create cost comparison visualization."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Healthcare Cost Analysis: Baseline vs AI Implementation', fontsize=16, fontweight='bold')
        
        # 1. Key metrics comparison
        categories = ['Admin Hours\nper Patient', 'Processing Time\n(Hours)', 'Error Rate\n(%)', 'Cost per\nPatient (¥)']
        baseline_values = [
            baseline['admin_hours_per_patient'],
            baseline['processing_time_hours'],
            baseline['billing_error_rate'] * 100,
            baseline['cost_per_patient']
        ]
        ai_values = [
            ai_metrics['admin_hours_per_patient'],
            ai_metrics['processing_time_hours'],
            ai_metrics['billing_error_rate'] * 100,
            ai_metrics['cost_per_patient']
        ]
        
        x = np.arange(len(categories))
        width = 0.35
        
        ax1.bar(x - width/2, baseline_values, width, label='Baseline', color=self.colors['baseline'], alpha=0.8)
        ax1.bar(x + width/2, ai_values, width, label='With AI', color=self.colors['ai_improved'], alpha=0.8)
        ax1.set_title('Key Performance Metrics Comparison')
        ax1.set_ylabel('Value')
        ax1.set_xticks(x)
        ax1.set_xticklabels(categories)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Percentage improvements
        improvements = [
            (1 - ai_values[0]/baseline_values[0]) * 100,
            (1 - ai_values[1]/baseline_values[1]) * 100,
            (1 - ai_values[2]/baseline_values[2]) * 100,
            (1 - ai_values[3]/baseline_values[3]) * 100
        ]
        
        bars = ax2.bar(categories, improvements, color=self.colors['savings'], alpha=0.8)
        ax2.set_title('Percentage Improvements with AI')
        ax2.set_ylabel('Improvement (%)')
        ax2.set_ylim(0, max(improvements) * 1.1)
        
        # Add value labels on bars
        for bar, value in zip(bars, improvements):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + max(improvements)*0.01,
                    f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # 3. Patient throughput comparison
        throughput_data = {
            'Baseline': baseline['patients_per_worker'],
            'With AI': ai_metrics['patients_per_worker']
        }
        
        colors_throughput = [self.colors['baseline'], self.colors['ai_improved']]
        wedges, texts, autotexts = ax3.pie(throughput_data.values(), labels=throughput_data.keys(), 
                                          autopct='%1.1f', colors=colors_throughput, startangle=90)
        ax3.set_title('Patients per Worker Comparison')
        
        # 4. Cost distribution
        saving_categories = ['Admin Labor', 'Error Reduction', 'Increased Throughput', 'Processing Efficiency']
        saving_values = [25, 35, 30, 10]  # Placeholder percentages
        
        ax4.bar(saving_categories, saving_values, color=self.colors['accent'], alpha=0.8)
        ax4.set_title('Cost Savings Distribution (%)')
        ax4.set_ylabel('Contribution to Total Savings (%)')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Cost comparison plot saved to {save_path}")
        
        return fig
    
    def plot_roi_analysis(self, roi_data: Dict[str, Any], save_path: Optional[str] = None) -> plt.Figure:
        """Create ROI analysis visualization."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Return on Investment (ROI) Analysis - 5 Year Projection', fontsize=16, fontweight='bold')
        
        yearly_data = pd.DataFrame(roi_data['yearly_analysis'])
        
        # 1. Cumulative savings over time
        ax1.plot(yearly_data['year'], yearly_data['cumulative_net'] / 1e12, 
                marker='o', linewidth=3, markersize=8, color=self.colors['savings'])
        ax1.fill_between(yearly_data['year'], 0, yearly_data['cumulative_net'] / 1e12, 
                        alpha=0.3, color=self.colors['savings'])
        ax1.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax1.set_title('Cumulative Net Benefit Over Time')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Cumulative Net Benefit (Trillion ¥)')
        ax1.grid(True, alpha=0.3)
        
        # Add breakeven point annotation
        if roi_data['payback_period_years']:
            ax1.axvline(x=roi_data['payback_period_years'], color='red', linestyle=':', alpha=0.7)
            ax1.text(roi_data['payback_period_years'], ax1.get_ylim()[1]*0.8, 
                    f'Breakeven\nYear {roi_data["payback_period_years"]}', 
                    ha='center', va='center', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # 2. Annual ROI percentage
        ax2.bar(yearly_data['year'], yearly_data['roi_percentage'], 
               color=self.colors['ai_improved'], alpha=0.8)
        ax2.set_title('ROI Percentage by Year')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('ROI (%)')
        ax2.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for i, v in enumerate(yearly_data['roi_percentage']):
            ax2.text(i+1, v + max(yearly_data['roi_percentage'])*0.02, f'{v:.0f}%', 
                    ha='center', va='bottom', fontweight='bold')
        
        # 3. Savings vs Costs comparison
        ax3.bar(yearly_data['year'] - 0.2, yearly_data['savings'] / 1e12, width=0.4, 
               label='Annual Savings', color=self.colors['savings'], alpha=0.8)
        ax3.bar(yearly_data['year'] + 0.2, yearly_data['costs'] / 1e12, width=0.4, 
               label='Annual Costs', color=self.colors['costs'], alpha=0.8)
        ax3.set_title('Annual Savings vs Costs')
        ax3.set_xlabel('Year')
        ax3.set_ylabel('Amount (Trillion ¥)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Investment summary (donut chart)
        investment_data = {
            'Initial Investment': roi_data['total_investment'] - (yearly_data['costs'].sum()),
            'Maintenance Costs': yearly_data['costs'].sum(),
            'Net Benefit': roi_data['net_benefit']
        }
        
        colors_investment = [self.colors['costs'], self.colors['neutral'], self.colors['savings']]
        wedges, texts, autotexts = ax4.pie(investment_data.values(), labels=investment_data.keys(), 
                                          autopct=lambda pct: f'¥{pct*sum(investment_data.values())/100/1e12:.1f}T',
                                          colors=colors_investment, startangle=90)
        
        # Create donut chart
        centre_circle = plt.Circle((0,0), 0.50, fc='white')
        ax4.add_artist(centre_circle)
        ax4.text(0, 0, f'Total ROI\n{roi_data["total_roi_percentage"]:.0f}%', 
                ha='center', va='center', fontsize=14, fontweight='bold')
        ax4.set_title('5-Year Investment Breakdown')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"ROI analysis plot saved to {save_path}")
        
        return fig
    
    def create_summary_dashboard(self, analysis_report: Dict[str, Any], save_path: Optional[str] = None) -> plt.Figure:
        """Create a comprehensive summary dashboard."""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('MCP-Health: AI Impact Analysis Summary Dashboard', fontsize=16, fontweight='bold')
        
        # Flatten axes for easier indexing
        axes = axes.flatten()
        
        # Extract data
        baseline = analysis_report['baseline_metrics']
        ai_metrics = analysis_report['ai_improved_metrics']
        savings = analysis_report['annual_savings']
        summary = analysis_report['summary']
        
        # 1. Key metrics comparison
        metrics = ['Admin Hours', 'Processing Time', 'Error Rate', 'Cost/Patient']
        baseline_vals = [baseline['admin_hours_per_patient'], baseline['processing_time_hours'], 
                        baseline['billing_error_rate']*100, baseline['cost_per_patient']/1000]
        ai_vals = [ai_metrics['admin_hours_per_patient'], ai_metrics['processing_time_hours'],
                  ai_metrics['billing_error_rate']*100, ai_metrics['cost_per_patient']/1000]
        
        x = np.arange(len(metrics))
        width = 0.35
        axes[0].bar(x - width/2, baseline_vals, width, label='Baseline', color=self.colors['baseline'], alpha=0.8)
        axes[0].bar(x + width/2, ai_vals, width, label='With AI', color=self.colors['ai_improved'], alpha=0.8)
        axes[0].set_title('Performance Metrics')
        axes[0].set_xticks(x)
        axes[0].set_xticklabels(metrics, rotation=45)
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # 2. Savings breakdown
        savings_labels = ['Admin Labor', 'Error Reduction', 'Additional Revenue', 'Processing']
        savings_values = [savings['admin_labor_savings']/1e12, savings['error_cost_savings']/1e12,
                         savings['additional_revenue']/1e12, savings.get('processing_efficiency_savings', 0)/1e12]
        
        axes[1].pie(savings_values, labels=savings_labels, autopct='%1.1f%%', startangle=90,
                   colors=[self.colors['baseline'], self.colors['ai_improved'], self.colors['savings'], self.colors['accent']])
        axes[1].set_title('Annual Savings Breakdown')
        
        # 3. ROI progression
        if 'roi_analysis' in analysis_report:
            roi_data = pd.DataFrame(analysis_report['roi_analysis']['yearly_analysis'])
            axes[2].plot(roi_data['year'], roi_data['roi_percentage'], marker='o', linewidth=3, 
                        color=self.colors['savings'])
            axes[2].set_title('ROI Progression (%)')
            axes[2].set_xlabel('Year')
            axes[2].set_ylabel('ROI %')
            axes[2].grid(True, alpha=0.3)
        
        # 4. Improvement percentages
        improvements = ['Admin Efficiency', 'Error Reduction', 'Throughput']
        improvement_values = [summary['admin_time_reduction_percentage'], 
                            summary['error_reduction_percentage'],
                            summary['throughput_increase_percentage']]
        
        bars = axes[3].bar(improvements, improvement_values, color=self.colors['ai_improved'], alpha=0.8)
        axes[3].set_title('AI Improvement Percentages')
        axes[3].set_ylabel('Improvement (%)')
        
        # Add value labels
        for bar, value in zip(bars, improvement_values):
            height = bar.get_height()
            axes[3].text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{value:.0f}%', ha='center', va='bottom', fontweight='bold')
        axes[3].grid(True, alpha=0.3)
        
        # 5. Cost comparison
        cost_categories = ['Baseline Total', 'AI Implementation', 'Net Savings']
        cost_values = [baseline['cost_per_patient']*47000000/1e12,  # Total for 47M patients
                      ai_metrics['cost_per_patient']*47000000/1e12,
                      savings['total_annual_savings']/1e12]
        
        axes[4].bar(cost_categories, cost_values, 
                   color=[self.colors['baseline'], self.colors['ai_improved'], self.colors['savings']], alpha=0.8)
        axes[4].set_title('Annual Cost Impact (Trillion ¥)')
        axes[4].set_ylabel('Amount (Trillion ¥)')
        axes[4].tick_params(axis='x', rotation=45)
        axes[4].grid(True, alpha=0.3)
        
        # 6. Summary text
        axes[5].axis('off')
        summary_text = f"""
        📊 EXECUTIVE SUMMARY
        
        💰 Annual Savings: ¥{summary['total_annual_savings_trillion_yen']:.1f} Trillion
        📈 5-Year ROI: {summary['five_year_roi_percentage']:.0f}%
        ⏱️ Payback Period: {summary['payback_period_years']} Years
        
        🏥 EFFICIENCY GAINS
        • Admin Time: -{summary['admin_time_reduction_percentage']:.0f}%
        • Error Rate: -{summary['error_reduction_percentage']:.0f}%
        • Patient Throughput: +{summary['throughput_increase_percentage']:.0f}%
        
        🇯🇵 IMPACT ON JAPAN
        • Aging Society Support: Enhanced
        • Healthcare Accessibility: Improved
        • Economic Burden: Reduced
        """
        
        axes[5].text(0.1, 0.9, summary_text, transform=axes[5].transAxes, fontsize=11,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Summary dashboard saved to {save_path}")
        
        return fig
    
    def export_analysis_charts(self, analysis_report: Dict[str, Any]) -> Dict[str, str]:
        """Export all analysis charts to files.
        
        Returns:
            Dictionary of chart names and file paths
        """
        chart_paths = {}
        
        # Cost comparison chart
        fig1 = self.plot_cost_comparison(
            analysis_report['baseline_metrics'], 
            analysis_report['ai_improved_metrics']
        )
        cost_path = self.output_dir / "cost_comparison.png"
        fig1.savefig(cost_path, dpi=300, bbox_inches='tight')
        chart_paths['cost_comparison'] = str(cost_path)
        plt.close(fig1)
        
        # ROI analysis chart
        if 'roi_analysis' in analysis_report:
            fig2 = self.plot_roi_analysis(analysis_report['roi_analysis'])
            roi_path = self.output_dir / "roi_analysis.png"
            fig2.savefig(roi_path, dpi=300, bbox_inches='tight')
            chart_paths['roi_analysis'] = str(roi_path)
            plt.close(fig2)
        
        # Summary dashboard
        fig3 = self.create_summary_dashboard(analysis_report)
        summary_path = self.output_dir / "summary_dashboard.png"
        fig3.savefig(summary_path, dpi=300, bbox_inches='tight')
        chart_paths['summary_dashboard'] = str(summary_path)
        plt.close(fig3)
        
        return chart_paths