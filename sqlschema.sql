-- sql/schema.sql
CREATE TABLE shipments (
    id SERIAL PRIMARY KEY,
    date_of_shipment DATE,
    year INTEGER,
    month INTEGER,
    quarter INTEGER,
    hsn_code VARCHAR(20),
    goods_description TEXT,
    quantity INTEGER,
    unit VARCHAR(20),
    unit_standardized VARCHAR(20),
    unit_price_inr DECIMAL(15,2),
    total_value_inr DECIMAL(15,2),
    duty_paid_inr DECIMAL(15,2),
    supplier_name TEXT,
    supplier_address TEXT,
    hsn_description TEXT,
    model_name VARCHAR(100),
    model_number VARCHAR(100),
    capacity_spec VARCHAR(50),
    material_type VARCHAR(50),
    unit_price_usd DECIMAL(10,2),
    embedded_quantity INTEGER,
    grand_total_inr DECIMAL(15,2),
    landed_cost_per_unit DECIMAL(10,2),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    duty_percentage DECIMAL(5,2)
);

-- sql/macro_trends.sql
-- Year-over-Year Growth Analysis
WITH yearly_totals AS (
    SELECT
        year,
        SUM(total_value_inr) as total_value,
        SUM(duty_paid_inr) as total_duty,
        SUM(grand_total_inr) as grand_total
    FROM shipments
    GROUP BY year
    ORDER BY year
),
yearly_growth AS (
    SELECT
        year,
        total_value,
        total_duty,
        grand_total,
        LAG(total_value) OVER (ORDER BY year) as prev_total_value,
        LAG(total_duty) OVER (ORDER BY year) as prev_total_duty,
        LAG(grand_total) OVER (ORDER BY year) as prev_grand_total
    FROM yearly_totals
)
SELECT
    year,
    total_value,
    total_duty,
    grand_total,
    ROUND(
        CASE 
            WHEN prev_total_value IS NOT NULL AND prev_total_value > 0 
            THEN ((total_value - prev_total_value) / prev_total_value) * 100 
            ELSE NULL 
        END, 2
    ) as yoy_total_value_growth_pct,
    ROUND(
        CASE 
            WHEN prev_total_duty IS NOT NULL AND prev_total_duty > 0 
            THEN ((total_duty - prev_total_duty) / prev_total_duty) * 100 
            ELSE NULL 
        END, 2
    ) as yoy_duty_growth_pct,
    ROUND(
        CASE 
            WHEN prev_grand_total IS NOT NULL AND prev_grand_total > 0 
            THEN ((grand_total - prev_grand_total) / prev_grand_total) * 100 
            ELSE NULL 
        END, 2
    ) as yoy_grand_total_growth_pct
FROM yearly_growth
ORDER BY year;

-- sql/pareto_hsn.sql
-- Top 25 HSN Codes Analysis
WITH hsn_totals AS (
    SELECT
        hsn_code,
        SUM(total_value_inr) as total_value,
        COUNT(*) as shipment_count
    FROM shipments
    GROUP BY hsn_code
),
ranked_hsn AS (
    SELECT
        hsn_code,
        total_value,
        shipment_count,
        ROW_NUMBER() OVER (ORDER BY total_value DESC) as rank
    FROM hsn_totals
),
top_25_hsn AS (
    SELECT * FROM ranked_hsn WHERE rank <= 25
),
others AS (
    SELECT
        'OTHERS' as hsn_code,
        SUM(total_value) as total_value,
        SUM(shipment_count) as shipment_count
    FROM ranked_hsn
    WHERE rank > 25
),
all_categories AS (
    SELECT hsn_code, total_value, shipment_count FROM top_25_hsn
    UNION ALL
    SELECT hsn_code, total_value, shipment_count FROM others
),
total_value_calc AS (
    SELECT SUM(total_value) as grand_total FROM all_categories
)
SELECT
    ac.hsn_code,
    ac.total_value,
    ac.shipment_count,
    ROUND((ac.total_value / tvc.grand_total) * 100, 2) as percentage_of_total
FROM all_categories ac
CROSS JOIN total_value_calc tvc
ORDER BY ac.total_value DESC;

-- sql/supplier_analysis.sql
-- Supplier Status Analysis (Active vs Churned in 2025)
WITH supplier_activity AS (
    SELECT
        supplier_name,
        MIN(year) as first_year,
        MAX(year) as last_year,
        COUNT(DISTINCT year) as active_years,
        SUM(grand_total_inr) as total_business
    FROM shipments
    GROUP BY supplier_name
)
SELECT
    supplier_name,
    first_year,
    last_year,
    active_years,
    total_business,
    CASE
        WHEN last_year = 2025 THEN 'ACTIVE_2025'
        WHEN last_year < 2025 THEN 'CHURNED'
        ELSE 'OTHER'
    END as supplier_status
FROM supplier_activity
ORDER BY total_business DESC;