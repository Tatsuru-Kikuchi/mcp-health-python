#!/usr/bin/env python3
"""
Basic usage example for MCP-Health package

This script demonstrates how to use the main features of the MCP-Health package
for healthcare productivity analysis in Japan.
"""

from mcp_health import HealthcareProductivityAnalyzer, HealthcareDataGenerator, HealthcareVisualizer
import json

def main():
    """Run basic analysis example."""
    print("🏥 MCP-Health: AI Productivity Analysis for Medical Fees in Japan")
    print("=" * 70)
    
    # Step 1: Generate sample data
    print("\n📊 Step 1: Generating sample healthcare datasets...")
    generator = HealthcareDataGenerator(output_dir="data/", random_seed=42)
    datasets = generator.generate_all_datasets(save_to_disk=True)
    
    print(f"✅ Generated {len(datasets)} datasets:")
    for name, df in datasets.items():
        print(f"   - {name}: {len(df)} records")
    
    # Step 2: Run healthcare productivity analysis
    print("\n🔬 Step 2: Running healthcare productivity analysis...")
    analyzer = HealthcareProductivityAnalyzer(data_dir="data/")
    analyzer.data = datasets  # Use the generated data
    
    # Generate comprehensive analysis report
    report = analyzer.generate_analysis_report()
    
    # Step 3: Display key results
    print("\n📈 Step 3: Analysis Results")
    print("-" * 40)
    
    summary = report['summary']
    
    print(f"💰 Annual Savings: ¥{summary['total_annual_savings_trillion_yen']:.2f} Trillion")
    print(f"📊 5-Year ROI: {summary['five_year_roi_percentage']:.1f}%")
    print(f"⏱️  Payback Period: {summary['payback_period_years']} years")
    print(f"🏢 Admin Time Reduction: {summary['admin_time_reduction_percentage']:.1f}%")
    print(f"❌ Error Rate Reduction: {summary['error_reduction_percentage']:.1f}%")
    print(f"👥 Patient Throughput Increase: {summary['throughput_increase_percentage']:.1f}%")
    
    # Step 4: Detailed metrics comparison
    print("\n📋 Step 4: Detailed Metrics Comparison")
    print("-" * 40)
    
    baseline = report['baseline_metrics']
    ai_metrics = report['ai_improved_metrics']
    
    print("\nBASELINE vs AI-ENHANCED METRICS:")
    print(f"Admin Hours per Patient: {baseline['admin_hours_per_patient']:.2f} → {ai_metrics['admin_hours_per_patient']:.2f}")
    print(f"Processing Time (hours): {baseline['processing_time_hours']:.2f} → {ai_metrics['processing_time_hours']:.2f}")
    print(f"Error Rate: {baseline['billing_error_rate']*100:.2f}% → {ai_metrics['billing_error_rate']*100:.2f}%")
    print(f"Patients per Worker: {baseline['patients_per_worker']:.1f} → {ai_metrics['patients_per_worker']:.1f}")
    print(f"Cost per Patient: ¥{baseline['cost_per_patient']:,.0f} → ¥{ai_metrics['cost_per_patient']:,.0f}")
    
    # Step 5: Savings breakdown
    print("\n💵 Step 5: Annual Savings Breakdown")
    print("-" * 40)
    
    savings = report['annual_savings']
    
    print(f"Administrative Labor Savings: ¥{savings['admin_labor_savings']/1e12:.2f} Trillion")
    print(f"Error Cost Reduction: ¥{savings['error_cost_savings']/1e12:.2f} Trillion")
    print(f"Additional Revenue: ¥{savings['additional_revenue']/1e12:.2f} Trillion")
    print(f"Processing Efficiency: ¥{savings.get('processing_efficiency_savings', 0)/1e12:.2f} Trillion")
    print(f"\n🎯 TOTAL ANNUAL SAVINGS: ¥{savings['total_annual_savings']/1e12:.2f} Trillion")
    
    # Step 6: ROI Analysis
    print("\n📊 Step 6: 5-Year ROI Analysis")
    print("-" * 40)
    
    roi = report['roi_analysis']
    
    print(f"Total Investment: ¥{roi['total_investment']/1e12:.2f} Trillion")
    print(f"Total Net Benefit: ¥{roi['net_benefit']/1e12:.2f} Trillion")
    print(f"ROI Percentage: {roi['total_roi_percentage']:.1f}%")
    print(f"Payback Period: {roi['payback_period_years']} years")
    
    print("\nYear-by-Year ROI:")
    for year_data in roi['yearly_analysis']:
        print(f"  Year {year_data['year']}: {year_data['roi_percentage']:.1f}% ROI")
    
    # Step 7: Generate visualizations
    print("\n🎨 Step 7: Generating visualizations...")
    visualizer = HealthcareVisualizer(output_dir="results/")
    
    # Export all charts
    chart_paths = visualizer.export_analysis_charts(report)
    
    print("✅ Generated charts:")
    for chart_name, path in chart_paths.items():
        print(f"   - {chart_name}: {path}")
    
    # Step 8: Save complete report
    print("\n💾 Step 8: Saving analysis report...")
    
    # Convert numpy types for JSON serialization
    def convert_numpy_types(obj):
        if isinstance(obj, dict):
            return {key: convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(item) for item in obj]
        elif hasattr(obj, 'dtype'):  # numpy types
            return obj.item() if hasattr(obj, 'item') else float(obj)
        else:
            return obj
    
    json_report = convert_numpy_types(report)
    
    with open('healthcare_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(json_report, f, indent=2, ensure_ascii=False)
    
    print("✅ Complete analysis report saved to: healthcare_analysis_report.json")
    
    # Summary
    print("\n🎉 Analysis Complete!")
    print("=" * 70)
    print("\n🌟 KEY TAKEAWAYS:")
    print(f"   • AI implementation could save Japan ¥{summary['total_annual_savings_trillion_yen']:.1f} trillion annually")
    print(f"   • {summary['five_year_roi_percentage']:.0f}% ROI over 5 years with {summary['payback_period_years']}-year payback")
    print(f"   • {summary['admin_time_reduction_percentage']:.0f}% reduction in administrative workload")
    print(f"   • {summary['error_reduction_percentage']:.0f}% reduction in medical errors")
    print(f"   • {summary['throughput_increase_percentage']:.0f}% increase in patient care capacity")
    
    print("\n📁 Files created:")
    print("   • data/ - Sample healthcare datasets")
    print("   • results/ - Analysis charts and visualizations")
    print("   • healthcare_analysis_report.json - Complete analysis results")
    
    print("\n🔗 For more information, visit:")
    print("   • Original Dashboard: https://tatsuru-kikuchi.github.io/MCP-health/")
    print("   • Package Repository: https://github.com/Tatsuru-Kikuchi/mcp-health-python")

if __name__ == "__main__":
    main()