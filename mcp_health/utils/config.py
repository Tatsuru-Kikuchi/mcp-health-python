#!/usr/bin/env python3
"""
Configuration settings for MCP-Health package.
"""

from typing import Dict, Any
import json
from pathlib import Path

# Default configuration for healthcare productivity analysis
DEFAULT_CONFIG = {
    # AI improvement factors (based on research literature)
    'ai_improvements': {
        'admin_efficiency_gain': 0.52,  # 52% reduction in admin time
        'processing_speed_gain': 0.75,  # 75% faster processing
        'error_reduction': 0.76,        # 76% error reduction
        'throughput_increase': 0.24,    # 24% patient throughput increase
        'cost_reduction': 0.071         # 7.1% overall cost reduction
    },
    
    # Japanese healthcare system constants
    'japan_constants': {
        'aging_population_pct': 0.291,      # 29.1% over 65
        'total_healthcare_cost': 45e12,     # ¥45 trillion annually
        'admin_cost_pct': 0.016,            # 1.6% admin costs
        'average_hourly_wage': 3000,        # ¥3000/hour average
        'patients_per_worker_baseline': 20,
        'error_cost_multiplier': 1.5,       # Cost multiplier for errors
        'total_population': 125000000,      # Japan population
        'healthcare_recipients': 47000000   # Estimated annual healthcare recipients
    },
    
    # Analysis parameters
    'analysis_params': {
        'roi_analysis_years': 5,           # Default ROI analysis period
        'inflation_rate': 0.02,            # 2% annual inflation
        'healthcare_cost_growth': 0.025,   # 2.5% annual healthcare cost growth
        'ai_savings_growth': 0.05,         # 5% annual improvement in AI savings
        'discount_rate': 0.03              # 3% discount rate for NPV calculations
    },
    
    # Visualization settings
    'visualization': {
        'default_figsize': [12, 8],
        'dpi': 300,
        'color_scheme': {
            'baseline': '#E74C3C',
            'ai_improved': '#2ECC71',
            'savings': '#3498DB',
            'costs': '#F39C12',
            'neutral': '#95A5A6',
            'accent': '#9B59B6'
        },
        'export_formats': ['png', 'pdf', 'svg']
    },
    
    # Data generation settings
    'data_generation': {
        'random_seed': 42,
        'sample_size': {
            'hospitals': 500,
            'prefectures': 47,
            'years': 5
        },
        'variation_factors': {
            'workforce_variation': 0.15,    # 15% variation in workforce sizes
            'cost_variation': 0.10,         # 10% variation in cost metrics
            'efficiency_variation': 0.20    # 20% variation in efficiency metrics
        }
    },
    
    # Output settings
    'output': {
        'data_dir': 'data/',
        'results_dir': 'results/',
        'reports_dir': 'reports/',
        'charts_dir': 'charts/',
        'default_formats': {
            'data': 'csv',
            'reports': 'json',
            'charts': 'png'
        }
    }
}

def load_config(config_path: str = None) -> Dict[str, Any]:
    """Load configuration from file or return default config.
    
    Args:
        config_path: Path to configuration JSON file
        
    Returns:
        Configuration dictionary
    """
    if config_path is None:
        return DEFAULT_CONFIG.copy()
    
    config_file = Path(config_path)
    
    if not config_file.exists():
        print(f"Config file {config_path} not found, using default configuration")
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
        
        # Merge user config with defaults
        config = DEFAULT_CONFIG.copy()
        config.update(user_config)
        
        return config
        
    except Exception as e:
        print(f"Error loading config file {config_path}: {e}")
        print("Using default configuration")
        return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any], config_path: str) -> bool:
    """Save configuration to file.
    
    Args:
        config: Configuration dictionary to save
        config_path: Path where to save the configuration
        
    Returns:
        True if successful, False otherwise
    """
    try:
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f"Error saving config to {config_path}: {e}")
        return False