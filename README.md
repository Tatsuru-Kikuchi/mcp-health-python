# MCP-Health Python Package

![PyPI Version](https://img.shields.io/pypi/v/mcp-health?style=for-the-badge)
![Python Versions](https://img.shields.io/pypi/pyversions/mcp-health?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Healthcare](https://img.shields.io/badge/Focus-Healthcare%20AI-blue?style=for-the-badge)

**AI Productivity Analysis for Medical Fees in Japan**

A comprehensive Python package for analyzing the economic impact of AI implementation in Japan's healthcare system, focusing on administrative efficiency and clinical productivity improvements.

## 🌟 Features

- **📊 Healthcare Productivity Analysis**: Calculate baseline metrics and AI impact projections
- **💰 Economic Impact Assessment**: ROI analysis and cost savings calculations
- **📈 Advanced Visualizations**: Professional charts and dashboards
- **🏥 Japanese Healthcare Focus**: Specialized for Japan's aging society challenges
- **🤖 AI Implementation Modeling**: Evidence-based improvement factors
- **📋 Sample Datasets**: Representative Japanese healthcare data for testing

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install mcp-health

# Install with optional dependencies
pip install mcp-health[interactive]  # Jupyter + Plotly support
pip install mcp-health[all]          # All optional dependencies
```

### Basic Usage

```python
from mcp_health import HealthcareProductivityAnalyzer, HealthcareDataGenerator

# Generate sample data
generator = HealthcareDataGenerator()
datasets = generator.generate_all_datasets()

# Run analysis
analyzer = HealthcareProductivityAnalyzer()
analyzer.data = datasets
report = analyzer.generate_analysis_report()

# Print key results
summary = report['summary']
print(f"Annual Savings: ¥{summary['total_annual_savings_trillion_yen']:.1f} Trillion")
print(f"5-Year ROI: {summary['five_year_roi_percentage']:.0f}%")
print(f"Payback Period: {summary['payback_period_years']} years")
```

### Create Visualizations

```python
from mcp_health import HealthcareVisualizer

# Create visualizer
visualizer = HealthcareVisualizer()

# Generate comprehensive dashboard
dashboard = visualizer.create_summary_dashboard(report)
dashboard.show()

# Export all charts
chart_paths = visualizer.export_analysis_charts(report)
print("Charts saved:", chart_paths)
```

## 📊 Analysis Results

The package provides comprehensive analysis of AI impact on Japanese healthcare:

### 🎯 **Key Findings**
- **Annual Savings**: ¥3.2 Trillion potential savings
- **ROI**: 245% five-year return on investment  
- **Efficiency**: 52% reduction in administrative time
- **Throughput**: 24% increase in patient capacity

### 📈 **Improvement Areas**
- Administrative automation and error reduction
- Clinical decision support systems
- Predictive analytics for patient care
- Workforce optimization and training

## 🏗️ Package Structure

```
mcp_health/
├── core/
│   ├── data_analysis.py      # Main analyzer class
│   ├── data_generator.py     # Sample data generation
│   └── visualization.py      # Charts and dashboards
├── data/
│   └── sample_datasets.py    # Japanese healthcare samples
└── utils/
    └── config.py            # Configuration management
```

## 📚 Documentation

### Core Classes

#### `HealthcareProductivityAnalyzer`
Main analysis engine for healthcare productivity assessment.

```python
analyzer = HealthcareProductivityAnalyzer(data_dir="data/")

# Load data and run analysis
data = analyzer.load_data()
baseline = analyzer.calculate_baseline_metrics(data)
ai_metrics = analyzer.calculate_ai_impact_metrics(baseline)
savings = analyzer.calculate_cost_savings(baseline, ai_metrics)
roi = analyzer.calculate_roi_analysis(savings)

# Generate comprehensive report
report = analyzer.generate_analysis_report()
```

#### `HealthcareDataGenerator`
Generate representative sample datasets for testing and demonstration.

```python
generator = HealthcareDataGenerator(output_dir="data/")

# Generate all datasets
datasets = generator.generate_all_datasets(save_to_disk=True)

# Create sample analysis
sample_report = generator.create_sample_analysis("sample_report.json")
```

#### `HealthcareVisualizer`
Create professional visualizations and dashboards.

```python
visualizer = HealthcareVisualizer(output_dir="results/")

# Create specific charts
cost_chart = visualizer.plot_cost_comparison(baseline, ai_metrics)
roi_chart = visualizer.plot_roi_analysis(roi_data)

# Generate summary dashboard
dashboard = visualizer.create_summary_dashboard(analysis_report)
```

## 🔧 Configuration

Customize analysis parameters using the configuration system:

```python
from mcp_health.utils import load_config, DEFAULT_CONFIG

# Load default configuration
config = load_config()

# Modify AI improvement factors
config['ai_improvements']['admin_efficiency_gain'] = 0.60  # 60% improvement

# Update Japanese healthcare constants
config['japan_constants']['total_healthcare_cost'] = 48e12  # ¥48 trillion

# Use custom configuration
analyzer = HealthcareProductivityAnalyzer()
analyzer.ai_improvements = config['ai_improvements']
analyzer.japan_constants = config['japan_constants']
```

## 🌏 Japanese Healthcare Context

This package is specifically designed for Japan's unique healthcare challenges:

- **Aging Society**: 29.1% of population over 65 years
- **Healthcare Costs**: ¥45 trillion annual expenditure
- **Administrative Efficiency**: Currently 1.6% of total costs
- **Workforce Shortage**: 500K additional workers needed by 2025

## 📈 Use Cases

### 🏛️ **Policy Makers**
- Evidence-based AI investment decisions
- Healthcare budget planning and optimization
- Long-term strategic planning for aging society

### 🏥 **Hospital Administrators**  
- ROI justification for AI implementation
- Operational efficiency assessment
- Staff productivity optimization

### 💼 **Technology Vendors**
- Market opportunity analysis
- Solution positioning and pricing
- Implementation planning and phasing

### 🔬 **Researchers**
- Healthcare AI impact studies
- Economic modeling and validation
- Comparative international analysis

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/Tatsuru-Kikuchi/mcp-health-python.git
cd mcp-health-python

# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Format code
black mcp_health/
isort mcp_health/

# Type checking
mypy mcp_health/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mcp_health --cov-report=html

# Run specific test file
pytest tests/test_data_analysis.py
```

## 📊 Sample Analysis Output

```json
{
  "summary": {
    "total_annual_savings_trillion_yen": 3.2,
    "five_year_roi_percentage": 245,
    "payback_period_years": 2,
    "admin_time_reduction_percentage": 52,
    "error_reduction_percentage": 76,
    "throughput_increase_percentage": 24
  },
  "baseline_metrics": {
    "admin_hours_per_patient": 2.0,
    "processing_time_hours": 4.0,
    "billing_error_rate": 0.025,
    "patients_per_worker": 20,
    "cost_per_patient": 250000
  },
  "ai_improved_metrics": {
    "admin_hours_per_patient": 0.96,
    "processing_time_hours": 1.0,
    "billing_error_rate": 0.006,
    "patients_per_worker": 24.8,
    "cost_per_patient": 232250
  }
}
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Make your changes and add tests
4. Ensure all tests pass (`pytest`)
5. Format your code (`black` and `isort`)
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- **[Original MCP-Health Dashboard](https://tatsuru-kikuchi.github.io/MCP-health/)**: Interactive web dashboard
- **[MCP-Health Repository](https://github.com/Tatsuru-Kikuchi/MCP-health)**: Original research project

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Tatsuru-Kikuchi/mcp-health-python/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Tatsuru-Kikuchi/mcp-health-python/discussions)
- **Email**: tatsuru.kikuchi@example.com

## 🙏 Acknowledgments

- Ministry of Health, Labour and Welfare (Japan) for healthcare statistics
- International healthcare AI research community
- Open source contributors and maintainers

---

<div align="center">

**⭐ Star this repository if you find it useful for healthcare AI research!**

[![GitHub stars](https://img.shields.io/github/stars/Tatsuru-Kikuchi/mcp-health-python?style=social)](https://github.com/Tatsuru-Kikuchi/mcp-health-python/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Tatsuru-Kikuchi/mcp-health-python?style=social)](https://github.com/Tatsuru-Kikuchi/mcp-health-python/network/members)

</div>
