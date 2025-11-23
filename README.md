
This project implements a comprehensive data pipeline for analyzing international trade data from 2017 to August 2025. The solution transforms raw, unstructured trade data into clean, structured tables and provides interactive dashboards for business intelligence.

## Project Context

Siddharth Associates receives raw trade data from subscription providers (Seair/Eximpedia) and currently performs manual Excel analysis. This project automates the analysis workflow using Python for data processing, SQL for structured storage and analysis, and Power BI for interactive visualization.

## Features

- **Advanced Text Parsing**: Extracts structured information from unstructured "Goods Description" field
- **Data Cleaning**: Standardizes units, handles missing values, and validates data integrity
- **Feature Engineering**: Calculates grand totals, landed costs, and hierarchical categories
- **SQL Analytics**: Performs YoY growth analysis, Pareto analysis, and supplier segmentation
- **Interactive Dashboard**: Power BI visualization for trend analysis and business insights

## Technical Requirements

### Software Stack
- **Python 3.9+** with packages: pandas, numpy, sqlalchemy, psycopg2-binary, regex
- **Database**: PostgreSQL (recommended) or MySQL
- **BI Tool**: Power BI Desktop
- **Development**: Jupyter Notebook, VS Code, or similar IDE

### Hardware Requirements
- Minimum 8GB RAM (16GB recommended)
- Sufficient disk space for raw data, processed data, and database storage

## Project Structure

```
siddharth_trade_pipeline/
├── data/
│   ├── raw/
│   │   └── Sample Data 2.xlsx          # Input dataset
│   └── processed/
│       └── trade_cleaned.csv           # Processed output
├── notebooks/
│   ├── 01_data_inspection.ipynb       # Initial data exploration
│   ├── 02_parsing_and_cleaning.ipynb  # Text parsing and cleaning
│   └── 03_feature_engineering.ipynb   # Feature creation
├── src/
│   ├── parsing/
│   │   └── parse_goods_description.py # Text parsing functions
│   ├── cleaning/
│   │   └── clean_base.py              # Data cleaning functions
│   ├── feature_engineering/
│   │   └── features.py                # Feature engineering functions
│   └── db/
│       └── load_to_db.py              # Database loading functions
├── sql/
│   ├── schema.sql                     # Database schema
│   ├── macro_trends.sql               # YoY growth queries
│   ├── pareto_hsn.sql                 # HSN code analysis
│   └── supplier_analysis.sql          # Supplier segmentation
├── dashboards/
│   └── trade_dashboard.pbix           # Power BI dashboard
└── README.md                          # This file
```

## Setup Instructions

### 1. Environment Setup

```bash
# Create and activate virtual environment
conda create -n trade_env python=3.11
conda activate trade_env

# Install required packages
pip install pandas numpy sqlalchemy psycopg2-binary python-dotenv regex openpyxl
```

### 2. Database Setup

```sql
-- Create database (PostgreSQL example)
CREATE DATABASE trade_analysis;
```

### 3. Data Preparation

1. Place the `Sample Data 2.xlsx` file in the `data/raw/` directory
2. Ensure the file contains the required columns as specified in the assignment

## Usage Instructions

### 1. Data Inspection
```bash
jupyter notebook notebooks/01_data_inspection.ipynb
```

### 2. Run Complete Pipeline
```python
# Run main_pipeline.py
python main_pipeline.py
```

### 3. Database Analysis
Execute SQL queries from the `sql/` directory to generate analytical views

### 4. Dashboard Creation
- Open `dashboards/trade_dashboard.pbix` in Power BI Desktop
- Connect to the database or import the processed CSV
- Update visualizations as needed

## Key Components

### Text Parsing Functions
- Extracts model name/number from goods descriptions
- Parses capacity specifications and material types
- Identifies unit prices in USD
- Extracts embedded quantities

### Feature Engineering
- Calculates Grand Total = Total Value (INR) + Duty Paid (INR)
- Computes Landed Cost Per Unit
- Assigns Category and Sub-Category hierarchies
- Calculates duty percentages

### SQL Analytics
- Year-over-Year growth trends
- Pareto analysis (Top 25 HSN codes)
- Supplier status classification (Active/Churned)
- Unit economics analysis

## Dashboard Views

### Macro Trends
- Line charts showing Total Value, Duty Paid, and Grand Total over time
- YoY growth heatmaps
- Annual summary cards

### Category Analysis
- Interactive sunburst/treemap for category drill-down
- Category performance by year
- Market share visualization

### Supplier Analysis
- Top suppliers by value
- Active vs. churned supplier analysis
- Supplier concentration metrics

### Unit Economics
- Scatter plots of capacity vs. landed cost
- Model-level price analysis
- Anomaly detection for duty structures

## Data Dictionary

| Field | Description |
|-------|-------------|
| Date of Shipment | Shipment date (DD/MM/YYYY) |
| HSN Code | Harmonized System Nomenclature code |
| Goods Description | Unstructured product description |
| Quantity | Shipment quantity |
| Unit | Unit of measurement (pcs, kg, mt, etc.) |
| Total Value (INR) | Assessable value in Indian Rupees |
| Duty Paid (INR) | Customs duty and taxes |
| Supplier Name | Origin supplier name |
| HSN Description | Standard HSN code description |
| model_name | Extracted model name |
| capacity_spec | Product capacity/specifications |
| material_type | Product material type |
| grand_total_inr | Total cost (Value + Duty) |
| category | Auto-assigned product category |
| sub_category | Auto-assigned sub-category |

## Assumptions

- The sample data file contains all required columns
- Data spans from January 2017 to August 2025
- Goods Description contains structured information that can be parsed using regex
- Database credentials are configured separately

## Performance Considerations

- For large datasets (>1M records), implement chunking and parallel processing
- Use database indexing for analytical queries
- Optimize regex patterns for parsing efficiency
- Consider data partitioning for time-series analysis

## Security & Privacy

- Store database credentials in environment variables or secure configuration files
- Do not commit sensitive data or credentials to version control
- Follow organizational data handling policies

## Maintenance

- Regular validation of parsing rules as new data patterns emerge
- Periodic review of category assignment logic
- Database performance optimization for growing datasets
- Dashboard refresh automation for regular reporting

