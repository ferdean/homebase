# homebase (c)

## Overview

This project is designed to analyze and visualize geographical and temporal data stored in CSV files.
Main goal is to obtain statistics about where the authors have lived during their lives.
It includes functionality for:

- Calculating statistics related to locations (cities, countries) and time periods.
- Visualizing the distribution of days lived across different locations and countries.
- Plotting interactive geographical maps.
- Displaying time-series data for specific cities, with options to exclude top cities and use logarithmic scales.

## Installation

To set up the environment for this project, follow the steps below:

1. **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install Dependencies:**
    Ensure you have Python 3.10 or newer. Then, install the necessary packages using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

3. **Download Natural Earth Shapefiles:**
    This project uses shapefiles from the Natural Earth dataset for plotting countries on the map. The necessary shapefiles will be automatically downloaded when you run the code for the first time.

## Usage

After installing the dependencies, you can run the main script to see the data analysis and visualizations:

```bash
python main.py
```

### Example Outputs:

- **Basic Statistics**: Summary statistics for the entire dataset.
- **City and Country Summaries**: Detailed breakdown of time spent in specific cities or countries.
- **Geographical Plots**: Interactive world maps showing time spent in each country.
- **Top Cities Over Time**: Line plots showing the top cities by days lived over different years.
- **Distribution Plots**: Bar plots displaying the distribution of days lived across cities and countries.
