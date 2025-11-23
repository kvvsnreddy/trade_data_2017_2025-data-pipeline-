# src/cleaning/clean_base.py
import pandas as pd

def clean_data(df):
    """Basic data cleaning"""
    df = df.copy()
    
    # Convert date column
    df['date_of_shipment'] = pd.to_datetime(df['Date of Shipment'], format='%d/%m/%Y', errors='coerce')
    
    # Derive year, month, quarter
    df['year'] = df['date_of_shipment'].dt.year
    df['month'] = df['date_of_shipment'].dt.month
    df['quarter'] = df['date_of_shipment'].dt.quarter
    
    # Standardize unit column
    unit_mapping = {
        'PCS': 'PCS', 'PC': 'PCS', 'NOS': 'PCS', 'PIECES': 'PCS', 'PIECE': 'PCS',
        'KG': 'KG', 'KGS': 'KG',
        'MT': 'MT', 'METRIC TON': 'MT',
        'BOX': 'BOX', 'SET': 'SET'
    }
    
    df['unit_standardized'] = df['Unit'].str.upper().map(unit_mapping).fillna(df['Unit'])
    
    # Handle missing values for critical fields
    df = df.dropna(subset=['Total Value (INR)', 'Duty Paid (INR)', 'Quantity'])
    
    return df

# src/feature_engineering/features.py
def add_features(df):
    """Add calculated features"""
    df = df.copy()
    
    # Grand Total calculation
    df['grand_total_inr'] = df['Total Value (INR)'] + df['Duty Paid (INR)']
    
    # Landed Cost Per Unit
    df['landed_cost_per_unit'] = df.apply(
        lambda row: row['grand_total_inr'] / row['Quantity'] if row['Quantity'] > 0 else None,
        axis=1
    )
    
    # Category assignment
    df['category'] = df.apply(assign_category, axis=1)
    df['sub_category'] = df.apply(assign_subcategory, axis=1)
    
    # Duty percentage
    df['duty_percentage'] = df.apply(
        lambda row: (row['Duty Paid (INR)'] / row['Total Value (INR)']) * 100 
        if row['Total Value (INR)'] > 0 else None,
        axis=1
    )
    
    return df

def assign_category(row):
    """Assign main category based on description and HSN"""
    desc = f"{str(row.get('Goods Description', ''))} {str(row.get('HSN Description', ''))}".upper()
    
    if 'GLASS' in desc:
        return 'Glass'
    elif 'WOOD' in desc or 'WOODEN' in desc:
        return 'Wooden'
    elif 'STEEL' in desc or 'SS' in desc or 'STAINLESS' in desc:
        return 'Steel'
    elif 'PLASTIC' in desc:
        return 'Plastic'
    elif 'ELECTRONIC' in desc or 'ELECTRICAL' in desc:
        return 'Electronics'
    else:
        return 'Others'

def assign_subcategory(row):
    """Assign sub-category based on category and description"""
    cat = row['category']
    desc = f"{str(row.get('Goods Description', ''))} {str(row.get('HSN Description', ''))}".upper()
    
    if cat == 'Glass':
        if 'BOROSILICATE' in desc:
            return 'Borosilicate'
        elif 'OPAL' in desc or 'OPALWARE' in desc:
            return 'Opalware'
        else:
            return 'Other Glass'
    elif cat == 'Wooden':
        if 'SPOON' in desc:
            return 'Spoon'
        elif 'FORK' in desc:
            return 'Fork'
        elif 'BOWL' in desc:
            return 'Bowl'
        else:
            return 'Other Wooden'
    elif cat == 'Steel':
        if 'UTENSIL' in desc or 'SPOON' in desc or 'FORK' in desc:
            return 'Utensils'
        else:
            return 'Other Steel'
    elif cat == 'Plastic':
        if 'BOTTLE' in desc:
            return 'Bottles'
        elif 'CONTAINER' in desc:
            return 'Containers'
        else:
            return 'Other Plastic'
    else:
        return 'Others'