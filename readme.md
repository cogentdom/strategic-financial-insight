# Strategic Financial Insight: Municipal Crime & Finance Analysis

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Overview

A comprehensive data science project completed for the **Idaho Policy Institute (IPI)** that delivers actionable insights into the relationship between municipal government financial decisions and crime rates. This analysis enables data-driven resource allocation strategies to effectively reduce crime across Idaho communities.

**Key Achievement:** Identified long-term outstanding debt as the most statistically significant predictor of crime rates, providing government bodies with evidence-based guidance that optimizes resource allocation and potentially saves thousands of taxpayer dollars.

### Project Context

- **Client:** Idaho Policy Institute, Boise State University
- **Duration:** 3-month service learning project
- **Objective:** Analyze municipal financial data to understand how government expenditure correlates with crime rates and develop predictive models for resource optimization

---

## Key Findings

### Primary Insight
Through OLS time-fixed effects regression modeling, **long-term outstanding debt** emerged as the most statistically significant feature (by a substantial margin) in predicting crime rates. This finding provides invaluable insight for policy makers:

- Cities with higher long-term debt consistently show higher crime rates
- This relationship holds even when controlling for population and general expenditure
- Understanding this correlation enables targeted intervention strategies

### Analytical Challenges Solved

1. **Temporal Data Imbalance:** Identified and leveraged a pattern of consistent data collection every five years across a 20-year period
2. **High Dimensionality:** Developed an automated feature selection pipeline to identify relevant variables from hundreds of potential features
3. **Data Quality Issues:** Successfully addressed missing values, temporal imbalance, and sparsity through strategic interpolation and cleaning

---

## Technical Approach

### Methodology

1. **Data Integration:** Merged multiple data sources (IPI financial data, BLS employment statistics, FBI crime data, Census Bureau demographics)
2. **Feature Engineering:** Created normalized features including per-capita rates, percentage of total expenditure/revenue, and temporal indicators
3. **Inflation Adjustment:** Adjusted all financial data to October 2019 dollars using CPI data
4. **Dimensionality Reduction:** Implemented automated feature selection to identify statistically significant predictors
5. **Statistical Modeling:** Applied OLS time-fixed effects regression to account for temporal variations

### Models & Techniques

- **Primary Model:** OLS Time-Fixed Effects Regression
- **Feature Selection:** Threshold-based relevance filtering
- **Data Processing:** Pandas, NumPy for data manipulation and cleaning
- **Visualization:** Seaborn, Matplotlib for exploratory data analysis
- **Statistical Analysis:** Statsmodels, Scikit-learn for modeling and validation

---

## Project Structure

```
strategic-financial-insight/
│
├── 📓 Notebooks/
│   ├── Final_Models.ipynb          # Complete modeling process and analysis
│   └── Library_Demo.ipynb          # Tutorial on using project functions
│
├── 📦 support/                      # Custom Python modules
│   ├── __init__.py
│   ├── load_data.py                # Data loading and merging utilities
│   ├── plotting_funcs.py           # Visualization functions
│   └── supporting_funcs.py         # Feature engineering and preprocessing
│
├── 📊 Data Files/
│   ├── Idaho_Municipal_Database_03052019.xlsx  # Primary financial dataset
│   ├── gps_data.csv                # Geographic coordinates by city/ZIP
│   ├── emp_data.csv                # Employment statistics
│   ├── col_only.csv                # Column descriptions and metadata
│   ├── best_cities.csv             # 59 cities with complete data
│   ├── bls_cpi_stats.xlsx          # CPI inflation adjustment data
│   │
│   ├── employment/                 # BLS employment data by year (1995-2015)
│   │   └── laucnty*.xlsx           # County-level employment files
│   │
│   └── GPS/                        # Geographic reference data
│       ├── idaho_city_zip.csv      # City-ZIP mappings
│       ├── ID.txt                  # Idaho geographic data
│       └── US.txt                  # US postal code reference
│
├── 📄 Documentation/
│   ├── readme.md                   # This file
│   └── requirements.txt            # Python dependencies
│
└── 🔧 Configuration/
    └── .gitignore
```

---

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- Jupyter Notebook or JupyterLab
- Git (for cloning the repository)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/strategic-financial-insight.git
   cd strategic-financial-insight
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```

---

## Usage Guide

### Quick Start

#### 1. Load and Process Data

```python
import support.load_data as load
import support.supporting_funcs as funcs

# Load complete dataset (inflation-adjusted, normalized, merged)
data = load.all_data(out=True, norm=True)

# Load abbreviated dataset (best cities, key years)
data_abb = load.ipi_abb()
```

#### 2. Explore Features

```python
# View column descriptions
columns = load.cols()

# Search for specific variables
crime_vars = funcs.search_all(data, 'crime')
expenditure_vars = funcs.search_all(data, 'expenditure')
```

#### 3. Visualize Trends

```python
import support.plotting_funcs as plot

# Plot feature over time
plot.plot_year(data, 'Total_Crime', size=True)

# Correlation matrix
plot.plot_corr_matrix(data, selected_features)

# Scatter matrix with correlations
plot.plot_scatter_matrix(data, selected_features)
```

#### 4. Feature Engineering

```python
# The normalize function creates per-capita and percentage features
normalized_data = funcs.normalize(raw_data)

# Categorize cities by population size
categorized_data = funcs.categorize_size(data)
```

### Detailed Tutorials

- **Library_Demo.ipynb:** Comprehensive guide to all custom functions and data loading procedures
- **Final_Models.ipynb:** Complete analytical workflow from data exploration to final model interpretation

---

## Data Sources

This project integrates data from multiple authoritative sources:

| Source | Description | Variables |
|--------|-------------|-----------|
| **Idaho Policy Institute** | Municipal financial database | Expenditure, revenue, debt, assets |
| **U.S. Census Bureau** | Demographic data | Population by city/county/state |
| **Willamette GFD** | Government finance database | Cash flow, municipal finances |
| **FBI** | Uniform Crime Reporting | Crime rates by type and jurisdiction |
| **Bureau of Labor Statistics** | Economic indicators | Employment, unemployment, CPI |

---

## Key Features & Functions

### Data Loading (`support.load_data`)

- `all_data()`: Load complete merged and processed dataset
- `ipi_abb()`: Load abbreviated dataset (best data quality)
- `emp()`: Load employment statistics
- `gps()`: Load geographic coordinates
- `cols()`: View column descriptions

### Feature Engineering (`support.supporting_funcs`)

- `normalize()`: Create per-capita and percentage features
- `categorize_size()`: Classify cities by population (rural/non-urban/urban)
- `gen_real_dollars()`: Adjust for inflation using CPI
- `search_all()`: Find columns matching a pattern
- `search_column()`: Search column descriptions

### Visualization (`support.plotting_funcs`)

- `plot_year()`: Visualize trends over time
- `plot_corr_matrix()`: Generate correlation heatmap
- `plot_scatter_matrix()`: Create scatter plot matrix with correlation coefficients

---

## Results & Impact

### Statistical Outcomes

- **Model Type:** OLS Time-Fixed Effects Regression
- **Statistical Significance:** Model achieved strong statistical significance with reliable coefficients
- **Key Predictor:** Long-term outstanding debt showed the highest correlation with crime rates
- **Controlled Variables:** Population, general expenditure, revenue, employment

### Practical Applications

1. **Policy Guidance:** Provides evidence for debt management strategies
2. **Resource Optimization:** Enables targeted allocation of crime prevention resources
3. **Financial Planning:** Informs long-term municipal budget decisions
4. **Predictive Capability:** Allows forecasting of crime trends based on financial indicators

---

## Future Enhancements

- [ ] Expand analysis to other states for comparison
- [ ] Incorporate more granular crime categories
- [ ] Add real-time data pipeline for continuous monitoring
- [ ] Develop interactive dashboard for stakeholders
- [ ] Machine learning models for improved prediction accuracy
- [ ] Include additional socioeconomic variables (education, healthcare spending)

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

## Authors & Acknowledgments

**Primary Author:**
- Dominik Huffield - Graduate Student, Boise State University

**Contributors:**
- Sammy Bhushan
- Amir Abbas Kazemzadeh Farizhandi

**Client:**
- Idaho Policy Institute, Boise State University

**Special Thanks:**
- Boise State University Data Science Program
- All data providers (Census Bureau, BLS, FBI, Willamette GFD)

---

## License

This project is available under the MIT License. See LICENSE file for details.

---

## Contact

For questions, suggestions, or collaboration opportunities, please open an issue in this repository.

---

## Appendix: GeoNames Data Attribution

**GeoNames Postal Code Files:**

This project uses geographic data from GeoNames (www.geonames.org), licensed under Creative Commons Attribution 3.0 License.

**Data Format:**
- Tab-delimited text in UTF-8 encoding
- Fields: country code, postal code, place name, admin divisions (1-3 levels), latitude, longitude, accuracy

**Coverage Notes:**
- Latitude/longitude determined algorithmically using place names and postal code proximity
- For unmatched locations, average coordinates of neighboring postal codes used
- Various countries have partial postal codes due to copyright restrictions

**Attribution:**
This project uses data from GeoNames (www.geonames.org), licensed under CC BY 3.0.

For more information: http://creativecommons.org/licenses/by/3.0/

---

**Built with ❤️ for better communities through data-driven insights**
