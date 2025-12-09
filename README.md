# Streamlit Log Visualizer

This project is a Streamlit application designed to visualize log data from CSV files. It allows users to select specific columns, date ranges, and plot types to generate insightful visualizations. The application processes data stored in a pickle file and provides options to export generated plots and data.

## Project Structure

```
streamlit-log-visualizer
├── src
│   ├── app.py          # Main entry point for the Streamlit application
│   ├── main.py         # Core logic for data processing and manipulation
│   ├── viz.py          # Plotting functions for data visualization
│   └── data_utils.py   # Utility functions for data handling
├── data                # Directory for input CSV files or uploaded files
│   └── (place input CSVs or uploaded files here)
├── output              # Directory for generated CSV/PNG files
│   └── (generated CSV/PNG files will be saved here)
├── requirements.txt    # Lists dependencies required for the project
├── .gitignore          # Specifies files and directories to be ignored by Git
└── README.md           # Documentation for the project
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd streamlit-log-visualizer
   ```

2. **Install Dependencies**
   It is recommended to create a virtual environment before installing the dependencies.
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   Start the Streamlit application using the following command:
   ```bash
   streamlit run src/app.py
   ```

## Usage Guidelines

- Use the sidebar to select the columns you wish to visualize, specify the start and end dates, and choose the type of plot (single or twin axes).
- After generating a plot, you can download the plot as a PNG file.
- The processed data can also be downloaded as a CSV file from the output directory.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.