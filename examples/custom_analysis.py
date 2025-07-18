#!/usr/bin/env python3
"""
Custom analysis example for MCP-Health package

This script demonstrates how to customize the analysis parameters
and create specialized reports.
"""

from mcp_health import HealthcareProductivityAnalyzer, HealthcareDataGenerator, HealthcareVisualizer
from mcp_health.utils import load_config, DEFAULT_CONFIG
import pandas as pd
import numpy as np

def create_custom_config():
    """Create a custom configuration with modified parameters."""
    config = DEFAULT_CONFIG.copy()
    
    # Modify AI improvement factors for more conservative estimates
    config['ai_improvements']['admin_efficiency_gain'] = 0.40  # 40% instead of 52%
    config['ai_improvements']['processing_speed_gain'] = 0.60  # 60% instead of 75%
    config['ai_improvements']['error_reduction'] = 0.65        # 65% instead of 76%
    config['ai_improvements']['throughput_increase'] = 0.20    # 20% instead of 24%
    
    # Adjust Japanese healthcare constants
    config['japan_constants']['total_healthcare_cost'] = 48e12  # ¥48 trillion (higher estimate)
    config['japan_constants']['average_hourly_wage'] = 3500    # ¥3500/hour (higher wage)
    
    return config

def create_scenario_analysis():
    """Create multiple scenario analyses with different assumptions."""
    print("🎯 Multi-Scenario Analysis")
    print("=" * 50)
    
    # Scenario definitions
    scenarios = {
        'conservative': {
            'name': 'Conservative Scenario',
            'admin_efficiency_gain': 0.30,
            'processing_speed_gain': 0.50,
            'error_reduction': 0.50,
            'throughput_increase': 0.15
        },
        'moderate': {
            'name': 'Moderate Scenario',
            'admin_efficiency_gain': 0.40,
            'processing_speed_gain': 0.60,
            'error_reduction': 0.65,
            'throughput_increase': 0.20
        },
        'optimistic': {
            'name': 'Optimistic Scenario',
            'admin_efficiency_gain': 0.52,
            'processing_speed_gain': 0.75,
            'error_reduction': 0.76,
            'throughput_increase': 0.24
        },
        'aggressive': {
            'name': 'Aggressive Scenario',
            'admin_efficiency_gain': 0.65,
            'processing_speed_gain': 0.85,
            'error_reduction': 0.85,
            'throughput_increase': 0.30
        }
    }
    
    # Generate base data once
    generator = HealthcareDataGenerator(random_seed=42)
    datasets = generator.generate_all_datasets(save_to_disk=False)
    
    scenario_results = {}
    
    for scenario_key, scenario_config in scenarios.items():
        print(f"\n📊 Running {scenario_config['name']}...")
        
        # Create analyzer with custom improvements
        analyzer = HealthcareProductivityAnalyzer()
        analyzer.data = datasets
        
        # Apply scenario-specific improvements
        analyzer.ai_improvements.update({
            'admin_efficiency_gain': scenario_config['admin_efficiency_gain'],
            'processing_speed_gain': scenario_config['processing_speed_gain'],
            'error_reduction': scenario_config['error_reduction'],
            'throughput_increase': scenario_config['throughput_increase']
        })
        
        # Run analysis
        report = analyzer.generate_analysis_report()
        scenario_results[scenario_key] = report
        
        # Print key metrics
        summary = report['summary']
        print(f"   Annual Savings: ¥{summary['total_annual_savings_trillion_yen']:.2f}T")
        print(f"   5-Year ROI: {summary['five_year_roi_percentage']:.1f}%")
        print(f"   Payback: {summary['payback_period_years']} years")
    
    return scenario_results

def create_sensitivity_analysis():
    """Perform sensitivity analysis on key parameters."""
    print("\n🔬 Sensitivity Analysis")
    print("=" * 50)
    
    # Generate base data
    generator = HealthcareDataGenerator(random_seed=42)
    datasets = generator.generate_all_datasets(save_to_disk=False)
    
    # Parameter ranges for sensitivity analysis
    admin_efficiency_range = np.arange(0.20, 0.71, 0.10)  # 20% to 70%
    cost_multiplier_range = np.arange(1.0, 2.1, 0.2)      # 1.0x to 2.0x
    
    sensitivity_results = []
    
    for admin_eff in admin_efficiency_range:
        for cost_mult in cost_multiplier_range:
            analyzer = HealthcareProductivityAnalyzer()
            analyzer.data = datasets
            
            # Modify parameters
            analyzer.ai_improvements['admin_efficiency_gain'] = admin_eff
            analyzer.japan_constants['error_cost_multiplier'] = cost_mult
            
            # Run analysis
            report = analyzer.generate_analysis_report()
            
            sensitivity_results.append({
                'admin_efficiency': admin_eff,
                'cost_multiplier': cost_mult,
                'annual_savings_trillion': report['summary']['total_annual_savings_trillion_yen'],
                'roi_percentage': report['summary']['five_year_roi_percentage'],
                'payback_years': report['summary']['payback_period_years']
            })
    
    # Convert to DataFrame for analysis
    sensitivity_df = pd.DataFrame(sensitivity_results)
    
    print("\n📊 Sensitivity Analysis Results:")
    print(f"Annual Savings Range: ¥{sensitivity_df['annual_savings_trillion'].min():.2f}T - ¥{sensitivity_df['annual_savings_trillion'].max():.2f}T")
    print(f"ROI Range: {sensitivity_df['roi_percentage'].min():.1f}% - {sensitivity_df['roi_percentage'].max():.1f}%")
    print(f"Payback Range: {sensitivity_df['payback_years'].min():.0f} - {sensitivity_df['payback_years'].max():.0f} years")
    
    return sensitivity_df

def create_custom_visualizations(scenario_results):
    """Create custom visualizations for scenario comparison."""
    print("\n🎨 Creating Custom Visualizations...")
    
    import matplotlib.pyplot as plt
    
    # Extract data for comparison chart
    scenarios = list(scenario_results.keys())
    savings_data = [scenario_results[s]['summary']['total_annual_savings_trillion_yen'] for s in scenarios]
    roi_data = [scenario_results[s]['summary']['five_year_roi_percentage'] for s in scenarios]
    
    # Create comparison chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Annual savings comparison
    bars1 = ax1.bar(scenarios, savings_data, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    ax1.set_title('Annual Savings by Scenario', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Annual Savings (Trillion ¥)')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, value in zip(bars1, savings_data):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'¥{value:.2f}T', ha='center', va='bottom', fontweight='bold')
    
    # ROI comparison
    bars2 = ax2.bar(scenarios, roi_data, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    ax2.set_title('5-Year ROI by Scenario', fontsize=14, fontweight='bold')
    ax2.set_ylabel('ROI (%)')
    ax2.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, value in zip(bars2, roi_data):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{value:.0f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('scenario_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Scenario comparison chart saved as: scenario_comparison.png")

def main():
    """Run custom analysis example."""
    print("🔧 MCP-Health: Custom Analysis Example")
    print("=" * 70)
    
    # 1. Multi-scenario analysis
    scenario_results = create_scenario_analysis()
    
    # 2. Sensitivity analysis
    sensitivity_df = create_sensitivity_analysis()
    
    # 3. Custom visualizations
    create_custom_visualizations(scenario_results)
    
    # 4. Save detailed results
    print("\n💾 Saving detailed analysis results...")
    
    # Save scenario comparison
    scenario_summary = {}
    for scenario_key, report in scenario_results.items():
        scenario_summary[scenario_key] = {
            'annual_savings_trillion_yen': report['summary']['total_annual_savings_trillion_yen'],
            'five_year_roi_percentage': report['summary']['five_year_roi_percentage'],
            'payback_period_years': report['summary']['payback_period_years'],
            'admin_time_reduction': report['summary']['admin_time_reduction_percentage'],
            'error_reduction': report['summary']['error_reduction_percentage'],
            'throughput_increase': report['summary']['throughput_increase_percentage']
        }
    
    import json
    with open('scenario_analysis_results.json', 'w') as f:
        json.dump(scenario_summary, f, indent=2)
    
    # Save sensitivity analysis
    sensitivity_df.to_csv('sensitivity_analysis.csv', index=False)
    
    print("✅ Results saved:")
    print("   • scenario_analysis_results.json")
    print("   • sensitivity_analysis.csv")
    print("   • scenario_comparison.png")
    
    # Summary
    print("\n🎉 Custom Analysis Complete!")
    print("\n💡 This example demonstrates:")
    print("   • Multi-scenario analysis with different AI effectiveness assumptions")
    print("   • Sensitivity analysis for key parameters")
    print("   • Custom visualization creation")
    print("   • Detailed results export for further analysis")

if __name__ == "__main__":
    main()