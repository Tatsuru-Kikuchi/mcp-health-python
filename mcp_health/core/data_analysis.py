#!/usr/bin/env python3
"""
Healthcare Productivity Analyzer for Japanese Medical System

This module provides analysis tools for evaluating the economic impact
of AI implementation in Japan's healthcare system.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import os
from pathlib import Path


class HealthcareProductivityAnalyzer:
    """Analyzer for healthcare productivity and AI impact assessment."""
    
    def __init__(self, data_dir: str = "data/"):
        """Initialize the analyzer.
        
        Args:
            data_dir: Directory containing healthcare data files
        """
        self.data_dir = Path(data_dir)
        self.data = {}
        
        # Default AI improvement factors based on research
        self.ai_improvements = {
            'admin_efficiency_gain': 0.52,  # 52% reduction in admin time
            'processing_speed_gain': 0.75,  # 75% faster processing
            'error_reduction': 0.76,        # 76% error reduction  
            'throughput_increase': 0.24,    # 24% patient throughput increase
            'cost_reduction': 0.071         # 7.1% overall cost reduction
        }
        
        # Japanese healthcare system constants
        self.japan_constants = {
            'aging_population_pct': 0.291,     # 29.1% over 65
            'total_healthcare_cost': 45e12,    # ¥45 trillion annually
            'admin_cost_pct': 0.016,           # 1.6% admin costs
            'average_hourly_wage': 3000,       # ¥3000/hour average
            'patients_per_worker_baseline': 20,
            'error_cost_multiplier': 1.5       # Cost multiplier for errors
        }
    
    def load_data(self) -> Dict[str, pd.DataFrame]:
        """Load healthcare datasets from CSV files.
        
        Returns:
            Dictionary containing loaded datasets
        """
        datasets = {
            'medical_expenditure': 'medical_expenditure.csv',
            'workforce': 'workforce.csv', 
            'administrative_costs': 'administrative_costs.csv',
            'patient_volume': 'patient_volume.csv',
            'ai_costs': 'ai_implementation_costs.csv'
        }
        
        loaded_data = {}
        
        for dataset_name, filename in datasets.items():
            filepath = self.data_dir / filename
            
            try:
                if filepath.exists():
                    loaded_data[dataset_name] = pd.read_csv(filepath)
                else:
                    # Generate sample data if file doesn't exist
                    loaded_data[dataset_name] = self._generate_sample_data(dataset_name)
                    
            except Exception as e:
                print(f"Warning: Could not load {filename}, using sample data: {e}")
                loaded_data[dataset_name] = self._generate_sample_data(dataset_name)
        
        self.data = loaded_data
        return loaded_data
    
    def _generate_sample_data(self, dataset_name: str) -> pd.DataFrame:
        """Generate sample data for missing datasets."""
        np.random.seed(42)  # For reproducible results
        
        if dataset_name == 'medical_expenditure':
            return pd.DataFrame({
                'year': [2023],
                'total_expenditure': [45e12],
                'admin_expenditure': [0.7e12],
                'clinical_expenditure': [35.2e12],
                'error_related_costs': [2.1e12]
            })
            
        elif dataset_name == 'workforce':
            return pd.DataFrame({
                'region_id': range(1, 48),  # 47 prefectures
                'total_workers': np.random.normal(50000, 15000, 47).astype(int),
                'administrative_workers': np.random.normal(8000, 2000, 47).astype(int),
                'clinical_workers': np.random.normal(42000, 13000, 47).astype(int)
            })
            
        elif dataset_name == 'administrative_costs':
            return pd.DataFrame({
                'hospital_id': range(1, 101),
                'admin_percentage': np.random.normal(0.016, 0.003, 100),
                'hours_per_patient': np.random.normal(2.0, 0.5, 100),
                'avg_processing_time': np.random.normal(4.0, 1.0, 100),
                'error_rate': np.random.normal(0.025, 0.005, 100)
            })
            
        elif dataset_name == 'patient_volume':
            return pd.DataFrame({
                'year': [2023] * 47,
                'prefecture_id': range(1, 48),
                'total_patients': np.random.normal(1000000, 300000, 47).astype(int),
                'outpatient_visits': np.random.normal(5000000, 1500000, 47).astype(int)
            })
            
        elif dataset_name == 'ai_costs':
            return pd.DataFrame({
                'implementation_phase': ['Phase 1', 'Phase 2', 'Phase 3'],
                'upfront_cost': [1e12, 1.5e12, 0.5e12],  # ¥3 billion total
                'annual_maintenance': [0.2e12, 0.3e12, 0.1e12],
                'training_cost': [0.1e12, 0.15e12, 0.05e12]
            })
            
        else:
            return pd.DataFrame()  # Empty DataFrame for unknown datasets
    
    def calculate_baseline_metrics(self, data: Optional[Dict[str, pd.DataFrame]] = None) -> Dict[str, float]:
        """Calculate baseline healthcare metrics without AI.
        
        Args:
            data: Healthcare datasets (uses self.data if not provided)
            
        Returns:
            Dictionary of baseline metrics
        """
        if data is None:
            data = self.data
            
        if not data:
            data = self.load_data()
        
        # Calculate baseline metrics
        admin_data = data.get('administrative_costs', pd.DataFrame())
        workforce_data = data.get('workforce', pd.DataFrame())
        patient_data = data.get('patient_volume', pd.DataFrame())
        expenditure_data = data.get('medical_expenditure', pd.DataFrame())
        
        baseline = {}
        
        # Administrative efficiency metrics
        if not admin_data.empty:
            baseline['admin_hours_per_patient'] = admin_data['hours_per_patient'].mean()
            baseline['processing_time_hours'] = admin_data['avg_processing_time'].mean()
            baseline['billing_error_rate'] = admin_data['error_rate'].mean()
        else:
            baseline['admin_hours_per_patient'] = 2.0
            baseline['processing_time_hours'] = 4.0
            baseline['billing_error_rate'] = 0.025
        
        # Workforce productivity
        if not workforce_data.empty and not patient_data.empty:
            total_workers = workforce_data['total_workers'].sum()
            total_patients = patient_data['total_patients'].sum()
            baseline['patients_per_worker'] = total_patients / total_workers if total_workers > 0 else 20
        else:
            baseline['patients_per_worker'] = self.japan_constants['patients_per_worker_baseline']
        
        # Cost metrics
        if not expenditure_data.empty:
            total_cost = expenditure_data['total_expenditure'].iloc[0]
            total_patients = patient_data['total_patients'].sum() if not patient_data.empty else 47000000
            baseline['cost_per_patient'] = total_cost / total_patients
        else:
            baseline['cost_per_patient'] = self.japan_constants['total_healthcare_cost'] / 47000000
        
        return baseline
    
    def calculate_ai_impact_metrics(self, baseline: Dict[str, float]) -> Dict[str, float]:
        """Calculate projected metrics with AI implementation.
        
        Args:
            baseline: Baseline metrics dictionary
            
        Returns:
            Dictionary of AI-improved metrics
        """
        ai_metrics = baseline.copy()
        
        # Apply AI improvements
        ai_metrics['admin_hours_per_patient'] = baseline['admin_hours_per_patient'] * (1 - self.ai_improvements['admin_efficiency_gain'])
        ai_metrics['processing_time_hours'] = baseline['processing_time_hours'] * (1 - self.ai_improvements['processing_speed_gain'])
        ai_metrics['billing_error_rate'] = baseline['billing_error_rate'] * (1 - self.ai_improvements['error_reduction'])
        ai_metrics['patients_per_worker'] = baseline['patients_per_worker'] * (1 + self.ai_improvements['throughput_increase'])
        ai_metrics['cost_per_patient'] = baseline['cost_per_patient'] * (1 - self.ai_improvements['cost_reduction'])
        
        return ai_metrics
    
    def calculate_cost_savings(self, baseline: Dict[str, float], ai_metrics: Dict[str, float]) -> Dict[str, float]:
        """Calculate annual cost savings from AI implementation.
        
        Args:
            baseline: Baseline metrics
            ai_metrics: AI-improved metrics
            
        Returns:
            Dictionary of cost savings by category
        """
        # Assume 47 million patients annually (Japan's population receiving healthcare)
        annual_patients = 47000000
        hourly_wage = self.japan_constants['average_hourly_wage']
        
        savings = {}
        
        # Administrative labor savings
        admin_hours_saved = (baseline['admin_hours_per_patient'] - ai_metrics['admin_hours_per_patient']) * annual_patients
        savings['admin_labor_savings'] = admin_hours_saved * hourly_wage
        
        # Error-related cost savings
        error_reduction = baseline['billing_error_rate'] - ai_metrics['billing_error_rate']
        baseline_error_cost = baseline['cost_per_patient'] * baseline['billing_error_rate'] * self.japan_constants['error_cost_multiplier']
        savings['error_cost_savings'] = error_reduction * baseline_error_cost * annual_patients
        
        # Additional revenue from increased throughput
        additional_patients = annual_patients * (ai_metrics['patients_per_worker'] / baseline['patients_per_worker'] - 1)
        avg_revenue_per_patient = baseline['cost_per_patient'] * 0.7  # Assume 70% is recoverable revenue
        savings['additional_revenue'] = additional_patients * avg_revenue_per_patient
        
        # Processing efficiency savings
        processing_hours_saved = (baseline['processing_time_hours'] - ai_metrics['processing_time_hours']) * annual_patients * 0.1  # 10% of processing involves paid staff time
        savings['processing_efficiency_savings'] = processing_hours_saved * hourly_wage
        
        # Total annual savings
        savings['total_annual_savings'] = sum([
            savings['admin_labor_savings'],
            savings['error_cost_savings'], 
            savings['additional_revenue'],
            savings['processing_efficiency_savings']
        ])
        
        return savings
    
    def calculate_roi_analysis(self, savings: Dict[str, float], years: int = 5) -> Dict[str, Any]:
        """Calculate ROI analysis over specified period.
        
        Args:
            savings: Annual savings dictionary
            years: Analysis period in years
            
        Returns:
            ROI analysis results
        """
        # AI implementation costs
        if 'ai_costs' in self.data and not self.data['ai_costs'].empty:
            upfront_cost = self.data['ai_costs']['upfront_cost'].sum()
            annual_maintenance = self.data['ai_costs']['annual_maintenance'].sum()
        else:
            upfront_cost = 3e12  # ¥3 billion
            annual_maintenance = 0.6e12  # ¥600 million annually
        
        annual_savings = savings['total_annual_savings']
        
        # Calculate year-by-year analysis
        yearly_analysis = []
        cumulative_savings = 0
        cumulative_costs = upfront_cost
        
        for year in range(1, years + 1):
            yearly_savings = annual_savings * (1.05 ** (year - 1))  # 5% annual increase
            yearly_costs = annual_maintenance
            
            net_yearly_benefit = yearly_savings - yearly_costs
            cumulative_savings += net_yearly_benefit
            cumulative_costs += yearly_costs
            
            yearly_analysis.append({
                'year': year,
                'savings': yearly_savings,
                'costs': yearly_costs,
                'net_benefit': net_yearly_benefit,
                'cumulative_net': cumulative_savings,
                'roi_percentage': (cumulative_savings / upfront_cost) * 100 if upfront_cost > 0 else 0
            })
        
        # Calculate payback period
        payback_years = None
        for analysis in yearly_analysis:
            if analysis['cumulative_net'] >= 0 and payback_years is None:
                payback_years = analysis['year']
                break
        
        total_roi = (cumulative_savings / upfront_cost) * 100 if upfront_cost > 0 else 0
        
        return {
            'yearly_analysis': yearly_analysis,
            'total_roi_percentage': total_roi,
            'payback_period_years': payback_years,
            'total_investment': upfront_cost + (annual_maintenance * years),
            'total_savings': cumulative_savings + upfront_cost,
            'net_benefit': cumulative_savings
        }
    
    def generate_analysis_report(self) -> Dict[str, Any]:
        """Generate complete analysis report.
        
        Returns:
            Comprehensive analysis report
        """
        # Load data if not already loaded
        if not self.data:
            self.load_data()
        
        # Calculate all metrics
        baseline = self.calculate_baseline_metrics()
        ai_metrics = self.calculate_ai_impact_metrics(baseline)
        savings = self.calculate_cost_savings(baseline, ai_metrics)
        roi_analysis = self.calculate_roi_analysis(savings)
        
        return {
            'baseline_metrics': baseline,
            'ai_improved_metrics': ai_metrics,
            'annual_savings': savings,
            'roi_analysis': roi_analysis,
            'summary': {
                'total_annual_savings_trillion_yen': savings['total_annual_savings'] / 1e12,
                'five_year_roi_percentage': roi_analysis['total_roi_percentage'],
                'payback_period_years': roi_analysis['payback_period_years'],
                'admin_time_reduction_percentage': self.ai_improvements['admin_efficiency_gain'] * 100,
                'error_reduction_percentage': self.ai_improvements['error_reduction'] * 100,
                'throughput_increase_percentage': self.ai_improvements['throughput_increase'] * 100
            }
        }
