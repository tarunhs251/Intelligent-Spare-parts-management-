"""
Demand Pattern Classification Module
Classifies demand patterns into 4 categories: Smooth, Erratic, Intermittent, Lumpy
Based on CV (Coefficient of Variation) and ADI (Average Demand Interval)
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
import json
from datetime import datetime

# Configuration
PROCESSED_DATA_DIR = Path("processed_data")
INPUT_FILE = PROCESSED_DATA_DIR / "encoded_dataset_model_ready.csv"
OUTPUT_FILE = PROCESSED_DATA_DIR / "classified_demand_dataset.csv"
REPORT_FILE = PROCESSED_DATA_DIR / "demand_classification_report.txt"

# Classification thresholds
CV_THRESHOLD = 0.5
ADI_THRESHOLD = 1.32


def calculate_cv(demand_series):
    """
    Calculate Coefficient of Variation (CV)
    CV = Standard Deviation / Mean
    """
    if len(demand_series) == 0 or demand_series.sum() == 0:
        return np.nan
    
    mean_demand = demand_series.mean()
    if mean_demand == 0:
        return np.nan
    
    std_demand = demand_series.std()
    cv = std_demand / mean_demand if mean_demand > 0 else np.nan
    return cv


def calculate_adi(demand_series, date_series):
    """
    Calculate Average Demand Interval (ADI)
    ADI = Number of periods / Number of periods with demand > 0
    """
    if len(demand_series) == 0:
        return np.nan
    
    # Count periods with positive demand
    periods_with_demand = (demand_series > 0).sum()
    
    if periods_with_demand == 0:
        return np.nan
    
    total_periods = len(demand_series)
    adi = total_periods / periods_with_demand if periods_with_demand > 0 else np.nan
    return adi


def classify_demand_pattern(cv, adi):
    """
    Classify demand pattern based on CV and ADI thresholds
    
    Categories:
    - Smooth: CV < 0.5, ADI < 1.32
    - Erratic: CV >= 0.5, ADI < 1.32
    - Intermittent: CV < 0.5, ADI >= 1.32
    - Lumpy: CV >= 0.5, ADI >= 1.32
    """
    if pd.isna(cv) or pd.isna(adi):
        return "Unknown"
    
    if cv < CV_THRESHOLD and adi < ADI_THRESHOLD:
        return "Smooth"
    elif cv >= CV_THRESHOLD and adi < ADI_THRESHOLD:
        return "Erratic"
    elif cv < CV_THRESHOLD and adi >= ADI_THRESHOLD:
        return "Intermittent"
    else:  # cv >= 0.5 and adi >= 1.32
        return "Lumpy"


def classify_demand_patterns(df):
    """
    Main function to classify demand patterns per SKU-Location
    """
    print("=" * 80)
    print("DEMAND PATTERN CLASSIFICATION")
    print("=" * 80)
    
    # Ensure date column is datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Reconstruct location_id from one-hot encoded columns
    location_cols = [col for col in df.columns if col.startswith('location_id_LOC_')]
    if location_cols and 'location_id' not in df.columns:
        print(f"Reconstructing location_id from {len(location_cols)} one-hot encoded columns...")
        # Find which location column is 1 for each row
        location_values = []
        for idx, row in df.iterrows():
            location = None
            for loc_col in location_cols:
                if row[loc_col] == 1:
                    # Extract location ID from column name (e.g., 'location_id_LOC_002' -> 'LOC_002')
                    location = loc_col.replace('location_id_', '')
                    break
            # If no location found, default to first location or create a default
            if location is None:
                # Check if all are 0, might be LOC_001 (baseline)
                if all(row[loc_col] == 0 for loc_col in location_cols):
                    location = 'LOC_001'  # Assuming first location is baseline
                else:
                    location = 'LOC_001'  # Default fallback
            location_values.append(location)
        df['location_id'] = location_values
        print(f"Reconstructed location_id. Unique locations: {df['location_id'].nunique()}")
    
    # Sort by SKU, Location, and Date
    df = df.sort_values(['part_sku', 'location_id', 'date']).reset_index(drop=True)
    
    # Group by SKU-Location and calculate metrics
    classification_results = []
    
    for (sku, location), group in df.groupby(['part_sku', 'location_id']):
        # Get demand series (quantity_sold)
        demand_series = group['quantity_sold'].values
        date_series = group['date'].values
        
        # Calculate CV and ADI
        cv = calculate_cv(demand_series)
        adi = calculate_adi(demand_series, date_series)
        
        # Classify pattern
        pattern = classify_demand_pattern(cv, adi)
        
        # Calculate additional statistics
        total_demand = demand_series.sum()
        mean_demand = demand_series.mean()
        std_demand = demand_series.std()
        periods_with_demand = (demand_series > 0).sum()
        total_periods = len(demand_series)
        zero_demand_ratio = 1 - (periods_with_demand / total_periods) if total_periods > 0 else 0
        
        classification_results.append({
            'part_sku': sku,
            'location_id': location,
            'cv': cv,
            'adi': adi,
            'demand_pattern': pattern,
            'total_demand': total_demand,
            'mean_demand': mean_demand,
            'std_demand': std_demand,
            'periods_with_demand': periods_with_demand,
            'total_periods': total_periods,
            'zero_demand_ratio': zero_demand_ratio
        })
    
    classification_df = pd.DataFrame(classification_results)
    
    # Merge classification back to original dataset
    df_classified = df.merge(
        classification_df[['part_sku', 'location_id', 'demand_pattern', 'cv', 'adi']],
        on=['part_sku', 'location_id'],
        how='left'
    )
    
    return df_classified, classification_df


def generate_classification_report(classification_df, df_classified):
    """
    Generate detailed classification distribution report
    """
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("DEMAND PATTERN CLASSIFICATION REPORT")
    report_lines.append("=" * 80)
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    # Overall distribution
    report_lines.append("CLASSIFICATION DISTRIBUTION")
    report_lines.append("-" * 80)
    pattern_counts = classification_df['demand_pattern'].value_counts()
    pattern_pct = classification_df['demand_pattern'].value_counts(normalize=True) * 100
    
    for pattern in ['Smooth', 'Erratic', 'Intermittent', 'Lumpy', 'Unknown']:
        count = pattern_counts.get(pattern, 0)
        pct = pattern_pct.get(pattern, 0)
        report_lines.append(f"{pattern:15s}: {count:5d} SKU-Locations ({pct:5.2f}%)")
    
    report_lines.append("")
    report_lines.append(f"Total SKU-Locations: {len(classification_df)}")
    report_lines.append("")
    
    # Statistics by pattern
    report_lines.append("STATISTICS BY DEMAND PATTERN")
    report_lines.append("-" * 80)
    
    for pattern in ['Smooth', 'Erratic', 'Intermittent', 'Lumpy']:
        pattern_data = classification_df[classification_df['demand_pattern'] == pattern]
        if len(pattern_data) > 0:
            report_lines.append(f"\n{pattern} Demand:")
            report_lines.append(f"  Count: {len(pattern_data)}")
            report_lines.append(f"  Mean CV: {pattern_data['cv'].mean():.4f}")
            report_lines.append(f"  Mean ADI: {pattern_data['adi'].mean():.4f}")
            report_lines.append(f"  Mean Total Demand: {pattern_data['total_demand'].mean():.2f}")
            report_lines.append(f"  Mean Zero Demand Ratio: {pattern_data['zero_demand_ratio'].mean():.4f}")
    
    # Dataset-level statistics
    report_lines.append("")
    report_lines.append("DATASET-LEVEL STATISTICS")
    report_lines.append("-" * 80)
    report_lines.append(f"Total records: {len(df_classified):,}")
    report_lines.append(f"Unique SKUs: {df_classified['part_sku'].nunique()}")
    report_lines.append(f"Unique Locations: {df_classified['location_id'].nunique()}")
    report_lines.append(f"Unique SKU-Location combinations: {len(classification_df)}")
    
    # Pattern distribution in records
    report_lines.append("")
    report_lines.append("RECORD-LEVEL PATTERN DISTRIBUTION")
    report_lines.append("-" * 80)
    record_pattern_counts = df_classified['demand_pattern'].value_counts()
    record_pattern_pct = df_classified['demand_pattern'].value_counts(normalize=True) * 100
    
    for pattern in ['Smooth', 'Erratic', 'Intermittent', 'Lumpy', 'Unknown']:
        count = record_pattern_counts.get(pattern, 0)
        pct = record_pattern_pct.get(pattern, 0)
        report_lines.append(f"{pattern:15s}: {count:8,d} records ({pct:5.2f}%)")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    
    return "\n".join(report_lines)


def main():
    """
    Main execution function
    """
    print("Loading dataset...")
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df):,} records")
    print(f"Columns: {len(df.columns)}")
    
    # Classify demand patterns
    print("\nClassifying demand patterns...")
    df_classified, classification_df = classify_demand_patterns(df)
    
    # Save classified dataset
    print(f"\nSaving classified dataset to {OUTPUT_FILE}...")
    df_classified.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(df_classified):,} records")
    
    # Generate and save report
    print("\nGenerating classification report...")
    report = generate_classification_report(classification_df, df_classified)
    
    with open(REPORT_FILE, 'w') as f:
        f.write(report)
    
    print(f"Report saved to {REPORT_FILE}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("CLASSIFICATION SUMMARY")
    print("=" * 80)
    print(classification_df['demand_pattern'].value_counts())
    print("\nClassification complete!")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Report file: {REPORT_FILE}")


if __name__ == "__main__":
    main()

