#!/usr/bin/env python3
"""
Healthcare Data Generator

Generates representative sample datasets for Japanese healthcare system analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Optional
import os


class HealthcareDataGenerator:
    """Generator for sample healthcare datasets."""
    
    def __init__(self, output_dir: str = "data/", random_seed: int = 42):
        """Initialize the data generator.
        
        Args:
            output_dir: Directory to save generated datasets
            random_seed: Random seed for reproducible data generation
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        np.random.seed(random_seed)
        
        # Japan-specific healthcare constants
        self.japan_data = {
            'prefectures': 47,
            'total_population': 125000000,
            'aging_population_pct': 0.291,
            'total_healthcare_expenditure': 45e12,  # ¥45 trillion
            'hospitals_count': 8200,
            'clinics_count': 102000
        }
    
    def generate_medical_expenditure_data(self) -> pd.DataFrame:
        """Generate medical expenditure data."""
        years = list(range(2019, 2024))
        
        data = []
        base_expenditure = 42e12  # Starting from ¥42 trillion in 2019
        
        for i, year in enumerate(years):
            # 2-3% annual growth in healthcare costs
            growth_rate = np.random.normal(0.025, 0.005)
            total_exp = base_expenditure * ((1 + growth_rate) ** i)
            
            # Administrative costs (1.6% of total)
            admin_exp = total_exp * 0.016
            
            # Clinical operations (78% of total)
            clinical_exp = total_exp * 0.78
            
            # Error-related costs (estimated 4.7% of total)
            error_costs = total_exp * 0.047
            
            # Other costs
            other_costs = total_exp - admin_exp - clinical_exp - error_costs
            
            data.append({
                'year': year,
                'total_expenditure': total_exp,
                'admin_expenditure': admin_exp,
                'clinical_expenditure': clinical_exp,
                'error_related_costs': error_costs,
                'other_costs': other_costs
            })
        
        return pd.DataFrame(data)
    
    def generate_workforce_data(self) -> pd.DataFrame:
        """Generate healthcare workforce data by prefecture."""
        prefectures = [
            'Hokkaido', 'Aomori', 'Iwate', 'Miyagi', 'Akita', 'Yamagata', 'Fukushima',
            'Ibaraki', 'Tochigi', 'Gunma', 'Saitama', 'Chiba', 'Tokyo', 'Kanagawa',
            'Niigata', 'Toyama', 'Ishikawa', 'Fukui', 'Yamanashi', 'Nagano', 'Gifu',
            'Shizuoka', 'Aichi', 'Mie', 'Shiga', 'Kyoto', 'Osaka', 'Hyogo', 'Nara',
            'Wakayama', 'Tottori', 'Shimane', 'Okayama', 'Hiroshima', 'Yamaguchi',
            'Tokushima', 'Kagawa', 'Ehime', 'Kochi', 'Fukuoka', 'Saga', 'Nagasaki',
            'Kumamoto', 'Oita', 'Miyazaki', 'Kagoshima', 'Okinawa'
        ]
        
        # Population data (roughly proportional to actual prefecture populations)
        population_weights = np.array([
            5.2, 1.3, 1.2, 2.3, 1.0, 1.1, 1.9, 2.9, 2.0, 2.0, 7.3, 6.3, 14.0, 9.2,
            2.3, 1.1, 1.2, 0.8, 0.8, 2.1, 2.0, 3.7, 7.5, 1.8, 1.4, 2.6, 8.8, 5.5, 1.4,
            1.0, 0.6, 0.7, 1.9, 2.8, 1.4, 0.8, 1.0, 1.4, 0.7, 5.1, 0.8, 1.4, 1.8, 1.2,
            1.1, 1.6, 1.5
        ])
        
        data = []
        for i, prefecture in enumerate(prefectures):
            # Scale workforce based on population
            base_workers = int(population_weights[i] * 30000)  # Base workers per prefecture
            
            # Add some random variation
            total_workers = int(np.random.normal(base_workers, base_workers * 0.15))
            
            # Distribution of worker types
            doctors = int(total_workers * np.random.normal(0.15, 0.02))  # ~15% doctors
            nurses = int(total_workers * np.random.normal(0.45, 0.05))   # ~45% nurses
            admin_workers = int(total_workers * np.random.normal(0.20, 0.03))  # ~20% admin
            other_clinical = total_workers - doctors - nurses - admin_workers
            
            data.append({
                'prefecture_id': i + 1,
                'prefecture_name': prefecture,
                'total_workers': total_workers,
                'doctors': max(doctors, 0),
                'nurses': max(nurses, 0),
                'administrative_workers': max(admin_workers, 0),
                'other_clinical_workers': max(other_clinical, 0),
                'workers_per_1000_population': total_workers / (population_weights[i] * 1000)
            })
        
        return pd.DataFrame(data)
    
    def generate_administrative_costs_data(self) -> pd.DataFrame:
        """Generate hospital administrative costs data."""
        n_hospitals = 500  # Sample of hospitals
        
        data = []
        for hospital_id in range(1, n_hospitals + 1):
            # Hospital size categories (affects admin percentage)
            size_category = np.random.choice(['small', 'medium', 'large'], p=[0.6, 0.3, 0.1])
            
            if size_category == 'small':
                beds = np.random.randint(20, 200)
                admin_pct = np.random.normal(0.018, 0.004)  # Slightly higher admin % for small hospitals
                hours_per_patient = np.random.normal(2.2, 0.6)
                processing_time = np.random.normal(4.5, 1.2)
                error_rate = np.random.normal(0.028, 0.008)
            elif size_category == 'medium':
                beds = np.random.randint(200, 500)
                admin_pct = np.random.normal(0.016, 0.003)
                hours_per_patient = np.random.normal(2.0, 0.5)
                processing_time = np.random.normal(4.0, 1.0)
                error_rate = np.random.normal(0.025, 0.006)
            else:  # large
                beds = np.random.randint(500, 1000)
                admin_pct = np.random.normal(0.014, 0.002)  # Better efficiency in large hospitals
                hours_per_patient = np.random.normal(1.8, 0.4)
                processing_time = np.random.normal(3.5, 0.8)
                error_rate = np.random.normal(0.022, 0.005)
            
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
    
    def generate_patient_volume_data(self) -> pd.DataFrame:
        """Generate patient volume data by prefecture."""
        # Use the same prefecture data as workforce
        workforce_df = self.generate_workforce_data()
        
        data = []
        for _, row in workforce_df.iterrows():
            prefecture_id = row['prefecture_id']
            prefecture_name = row['prefecture_name']
            
            # Estimate patient volume based on workers and population
            base_patients = row['total_workers'] * 25  # Rough ratio
            
            # Add seasonal and random variation
            annual_patients = int(np.random.normal(base_patients, base_patients * 0.1))
            outpatient_visits = int(annual_patients * np.random.normal(6.5, 1.0))  # ~6.5 visits per patient per year
            inpatient_admissions = int(annual_patients * np.random.normal(0.12, 0.02))  # ~12% admission rate
            emergency_visits = int(annual_patients * np.random.normal(0.08, 0.015))  # ~8% emergency rate
            
            data.append({
                'prefecture_id': prefecture_id,
                'prefecture_name': prefecture_name,
                'year': 2023,
                'total_patients': annual_patients,
                'outpatient_visits': outpatient_visits,
                'inpatient_admissions': inpatient_admissions,
                'emergency_visits': emergency_visits,
                'average_length_of_stay': np.random.normal(16.5, 3.0),  # Days
                'bed_occupancy_rate': np.random.normal(0.75, 0.08)  # 75% average
            })
        
        return pd.DataFrame(data)
    
    def generate_ai_implementation_costs(self) -> pd.DataFrame:
        """Generate AI implementation cost estimates."""
        phases = [
            {
                'phase': 'Phase 1 - Pilot Implementation',
                'duration_months': 6,
                'upfront_cost': 1.0e12,  # ¥1 billion
                'annual_maintenance': 0.2e12,  # ¥200 million
                'training_cost': 0.1e12,  # ¥100 million
                'staff_required': 50,
                'hospitals_covered': 100,
                'scope': 'Administrative automation in major hospitals'
            },
            {
                'phase': 'Phase 2 - Regional Expansion', 
                'duration_months': 18,
                'upfront_cost': 1.5e12,  # ¥1.5 billion
                'annual_maintenance': 0.3e12,  # ¥300 million
                'training_cost': 0.15e12,  # ¥150 million
                'staff_required': 120,
                'hospitals_covered': 500,
                'scope': 'Clinical decision support and expanded admin automation'
            },
            {
                'phase': 'Phase 3 - National Deployment',
                'duration_months': 24,
                'upfront_cost': 0.5e12,  # ¥500 million
                'annual_maintenance': 0.1e12,  # ¥100 million
                'training_cost': 0.05e12,  # ¥50 million
                'staff_required': 200,
                'hospitals_covered': 2000,
                'scope': 'Full AI integration with predictive analytics'
            }
        ]
        
        return pd.DataFrame(phases)
    
    def generate_all_datasets(self, save_to_disk: bool = True) -> Dict[str, pd.DataFrame]:
        """Generate all healthcare datasets.
        
        Args:
            save_to_disk: Whether to save datasets to CSV files
            
        Returns:
            Dictionary containing all generated datasets
        """
        datasets = {
            'medical_expenditure': self.generate_medical_expenditure_data(),
            'workforce': self.generate_workforce_data(),
            'administrative_costs': self.generate_administrative_costs_data(),
            'patient_volume': self.generate_patient_volume_data(),
            'ai_implementation_costs': self.generate_ai_implementation_costs()
        }
        
        if save_to_disk:
            for name, df in datasets.items():
                filepath = self.output_dir / f"{name}.csv"
                df.to_csv(filepath, index=False)
                print(f"Saved {name} data to {filepath}")
        
        return datasets
    
    def create_sample_analysis(self, output_file: Optional[str] = None) -> Dict:
        """Create a sample analysis using generated data.
        
        Args:
            output_file: Optional file to save analysis results
            
        Returns:
            Sample analysis results
        """
        from .data_analysis import HealthcareProductivityAnalyzer
        
        # Generate datasets
        datasets = self.generate_all_datasets(save_to_disk=True)
        
        # Run analysis
        analyzer = HealthcareProductivityAnalyzer(data_dir=str(self.output_dir))
        analyzer.data = datasets  # Use generated data directly
        
        report = analyzer.generate_analysis_report()
        
        if output_file:
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                # Convert numpy types to Python types for JSON serialization
                json_report = self._convert_numpy_types(report)
                json.dump(json_report, f, indent=2, ensure_ascii=False)
            print(f"Analysis report saved to {output_file}")
        
        return report
    
    def _convert_numpy_types(self, obj):
        """Convert numpy types to Python types for JSON serialization."""
        if isinstance(obj, dict):
            return {key: self._convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_numpy_types(item) for item in obj]
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
