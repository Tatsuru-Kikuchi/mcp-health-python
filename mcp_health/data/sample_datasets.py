#!/usr/bin/env python3
"""
Sample Healthcare Datasets

Provides sample datasets for testing and demonstration purposes.
"""

import pandas as pd
import numpy as np
from typing import Dict, List

# Information about available sample datasets
SAMPLE_DATA_INFO = {
    'medical_expenditure': {
        'description': 'Annual medical expenditure data for Japan (2019-2023)',
        'columns': ['year', 'total_expenditure', 'admin_expenditure', 'clinical_expenditure', 'error_related_costs', 'other_costs'],
        'records': 5
    },
    'workforce': {
        'description': 'Healthcare workforce data by prefecture',
        'columns': ['prefecture_id', 'prefecture_name', 'total_workers', 'doctors', 'nurses', 'administrative_workers', 'other_clinical_workers'],
        'records': 47
    },
    'administrative_costs': {
        'description': 'Hospital administrative costs and efficiency metrics',
        'columns': ['hospital_id', 'size_category', 'bed_count', 'admin_percentage', 'hours_per_patient', 'avg_processing_time', 'error_rate'],
        'records': 500
    },
    'patient_volume': {
        'description': 'Patient volume and utilization data by prefecture',
        'columns': ['prefecture_id', 'prefecture_name', 'year', 'total_patients', 'outpatient_visits', 'inpatient_admissions', 'emergency_visits'],
        'records': 47
    },
    'ai_implementation_costs': {
        'description': 'AI implementation cost estimates by phase',
        'columns': ['phase', 'duration_months', 'upfront_cost', 'annual_maintenance', 'training_cost', 'staff_required', 'hospitals_covered'],
        'records': 3
    }
}

def get_sample_data(dataset_name: str = None) -> Dict[str, pd.DataFrame]:
    """Get sample healthcare datasets.
    
    Args:
        dataset_name: Name of specific dataset to load, or None for all datasets
        
    Returns:
        Dictionary containing requested dataset(s)
    """
    np.random.seed(42)  # For reproducible data
    
    datasets = {
        'medical_expenditure': _create_medical_expenditure_data(),
        'workforce': _create_workforce_data(),
        'administrative_costs': _create_administrative_costs_data(),
        'patient_volume': _create_patient_volume_data(),
        'ai_implementation_costs': _create_ai_costs_data()
    }
    
    if dataset_name:
        if dataset_name in datasets:
            return {dataset_name: datasets[dataset_name]}
        else:
            raise ValueError(f"Unknown dataset: {dataset_name}. Available datasets: {list(datasets.keys())}")
    
    return datasets

def _create_medical_expenditure_data() -> pd.DataFrame:
    """Create sample medical expenditure data."""
    years = list(range(2019, 2024))
    data = []
    base_expenditure = 42e12  # Starting from ¥42 trillion in 2019
    
    for i, year in enumerate(years):
        growth_rate = 0.025  # 2.5% annual growth
        total_exp = base_expenditure * ((1 + growth_rate) ** i)
        
        data.append({
            'year': year,
            'total_expenditure': total_exp,
            'admin_expenditure': total_exp * 0.016,
            'clinical_expenditure': total_exp * 0.78,
            'error_related_costs': total_exp * 0.047,
            'other_costs': total_exp * 0.157
        })
    
    return pd.DataFrame(data)

def _create_workforce_data() -> pd.DataFrame:
    """Create sample workforce data."""
    prefectures = [
        'Hokkaido', 'Aomori', 'Iwate', 'Miyagi', 'Akita', 'Yamagata', 'Fukushima',
        'Ibaraki', 'Tochigi', 'Gunma', 'Saitama', 'Chiba', 'Tokyo', 'Kanagawa',
        'Niigata', 'Toyama', 'Ishikawa', 'Fukui', 'Yamanashi', 'Nagano', 'Gifu',
        'Shizuoka', 'Aichi', 'Mie', 'Shiga', 'Kyoto', 'Osaka', 'Hyogo', 'Nara',
        'Wakayama', 'Tottori', 'Shimane', 'Okayama', 'Hiroshima', 'Yamaguchi',
        'Tokushima', 'Kagawa', 'Ehime', 'Kochi', 'Fukuoka', 'Saga', 'Nagasaki',
        'Kumamoto', 'Oita', 'Miyazaki', 'Kagoshima', 'Okinawa'
    ]
    
    # Population weights (roughly proportional to actual prefecture populations)
    population_weights = np.array([
        5.2, 1.3, 1.2, 2.3, 1.0, 1.1, 1.9, 2.9, 2.0, 2.0, 7.3, 6.3, 14.0, 9.2,
        2.3, 1.1, 1.2, 0.8, 0.8, 2.1, 2.0, 3.7, 7.5, 1.8, 1.4, 2.6, 8.8, 5.5, 1.4,
        1.0, 0.6, 0.7, 1.9, 2.8, 1.4, 0.8, 1.0, 1.4, 0.7, 5.1, 0.8, 1.4, 1.8, 1.2,
        1.1, 1.6, 1.5
    ])
    
    data = []
    for i, prefecture in enumerate(prefectures):
        base_workers = int(population_weights[i] * 30000)
        total_workers = int(np.random.normal(base_workers, base_workers * 0.1))
        
        doctors = int(total_workers * 0.15)
        nurses = int(total_workers * 0.45)
        admin_workers = int(total_workers * 0.20)
        other_clinical = total_workers - doctors - nurses - admin_workers
        
        data.append({
            'prefecture_id': i + 1,
            'prefecture_name': prefecture,
            'total_workers': total_workers,
            'doctors': doctors,
            'nurses': nurses,
            'administrative_workers': admin_workers,
            'other_clinical_workers': max(0, other_clinical),
            'workers_per_1000_population': total_workers / (population_weights[i] * 1000)
        })
    
    return pd.DataFrame(data)

def _create_administrative_costs_data() -> pd.DataFrame:
    """Create sample administrative costs data."""
    n_hospitals = 500
    data = []
    
    for hospital_id in range(1, n_hospitals + 1):
        size_category = np.random.choice(['small', 'medium', 'large'], p=[0.6, 0.3, 0.1])
        
        if size_category == 'small':
            beds = np.random.randint(20, 200)
            admin_pct = np.random.normal(0.018, 0.003)
            hours_per_patient = np.random.normal(2.2, 0.5)
            processing_time = np.random.normal(4.5, 1.0)
            error_rate = np.random.normal(0.028, 0.006)
        elif size_category == 'medium':
            beds = np.random.randint(200, 500)
            admin_pct = np.random.normal(0.016, 0.002)
            hours_per_patient = np.random.normal(2.0, 0.4)
            processing_time = np.random.normal(4.0, 0.8)
            error_rate = np.random.normal(0.025, 0.005)
        else:  # large
            beds = np.random.randint(500, 1000)
            admin_pct = np.random.normal(0.014, 0.002)
            hours_per_patient = np.random.normal(1.8, 0.3)
            processing_time = np.random.normal(3.5, 0.6)
            error_rate = np.random.normal(0.022, 0.004)
        
        # Ensure realistic bounds
        admin_pct = max(0.008, min(0.030, admin_pct))
        hours_per_patient = max(0.5, min(5.0, hours_per_patient))
        processing_time = max(1.0, min(8.0, processing_time))
        error_rate = max(0.005, min(0.050, error_rate))
        
        data.append({
            'hospital_id': hospital_id,
            'size_category': size_category,
            'bed_count': beds,
            'admin_percentage': admin_pct,
            'hours_per_patient': hours_per_patient,
            'avg_processing_time': processing_time,
            'error_rate': error_rate,
            'monthly_patients': np.random.randint(1000, 10000),
            'administrative_staff_count': max(5, int(beds * 0.15))
        })
    
    return pd.DataFrame(data)

def _create_patient_volume_data() -> pd.DataFrame:
    """Create sample patient volume data."""
    workforce_df = _create_workforce_data()
    
    data = []
    for _, row in workforce_df.iterrows():
        base_patients = row['total_workers'] * 25
        annual_patients = int(np.random.normal(base_patients, base_patients * 0.1))
        
        data.append({
            'prefecture_id': row['prefecture_id'],
            'prefecture_name': row['prefecture_name'],
            'year': 2023,
            'total_patients': annual_patients,
            'outpatient_visits': int(annual_patients * 6.5),
            'inpatient_admissions': int(annual_patients * 0.12),
            'emergency_visits': int(annual_patients * 0.08),
            'average_length_of_stay': np.random.normal(16.5, 2.0),
            'bed_occupancy_rate': np.random.normal(0.75, 0.05)
        })
    
    return pd.DataFrame(data)

def _create_ai_costs_data() -> pd.DataFrame:
    """Create sample AI implementation costs data."""
    phases = [
        {
            'phase': 'Phase 1 - Pilot Implementation',
            'duration_months': 6,
            'upfront_cost': 1.0e12,
            'annual_maintenance': 0.2e12,
            'training_cost': 0.1e12,
            'staff_required': 50,
            'hospitals_covered': 100,
            'scope': 'Administrative automation in major hospitals'
        },
        {
            'phase': 'Phase 2 - Regional Expansion',
            'duration_months': 18,
            'upfront_cost': 1.5e12,
            'annual_maintenance': 0.3e12,
            'training_cost': 0.15e12,
            'staff_required': 120,
            'hospitals_covered': 500,
            'scope': 'Clinical decision support and expanded admin automation'
        },
        {
            'phase': 'Phase 3 - National Deployment',
            'duration_months': 24,
            'upfront_cost': 0.5e12,
            'annual_maintenance': 0.1e12,
            'training_cost': 0.05e12,
            'staff_required': 200,
            'hospitals_covered': 2000,
            'scope': 'Full AI integration with predictive analytics'
        }
    ]
    
    return pd.DataFrame(phases)
