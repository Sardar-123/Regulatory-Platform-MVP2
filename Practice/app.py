from flask import Flask, render_template, send_file, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import io
from src.parsers.parse_xsd import parse_xsd
from src.comparers.compare_elements import compare_elements
from src.analyzers.impact_analyzer import generate_impact_summary_and_test_scenario

app = Flask(__name__)

# Dummy data paths for demonstration
file_path1 = "data/old_version/EPC115-06_2021_V1.0_pacs.008.001.02_Update.xsd"
file_path2 = "data/new_version/EPC115-06_2023_V1.0_pacs.008.001.08_Update.xsd"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    # Parse XSD files and compare elements
    elements_dict1 = parse_xsd(file_path1)
    elements_dict2 = parse_xsd(file_path2)
    comparison_report = compare_elements(elements_dict1, elements_dict2)

    # Create DataFrame from comparison report
    df_report = pd.DataFrame(comparison_report, columns=['Change Type', 'Element Path', 'Old Type', 'New Type', 'Annotation'])
    
    # Generate bar chart
    change_type_counts = df_report['Change Type'].value_counts()
    bar_chart_path = 'static/bar_chart.png'
    plt.figure()
    change_type_counts.plot(kind='bar')
    plt.title('Change Type Distribution')
    plt.xlabel('Change Type')
    plt.ylabel('Count')
    plt.savefig(bar_chart_path)
    plt.close()

    # Generate pie chart
    pie_chart_path = 'static/pie_chart.png'
    plt.figure()
    plt.pie(change_type_counts, labels=change_type_counts.index, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Change Type Distribution (Pie Chart)')
    plt.savefig(pie_chart_path)
    plt.close()

    return render_template('results.html', bar_chart_path=bar_chart_path, pie_chart_path=pie_chart_path)

@app.route('/generate_reports', methods=['POST'])
def generate_reports():
    # Parse XSD files and compare elements
    elements_dict1 = parse_xsd(file_path1)
    elements_dict2 = parse_xsd(file_path2)
    comparison_report = compare_elements(elements_dict1, elements_dict2)

    # Create DataFrame from comparison report
    df_report = pd.DataFrame(comparison_report, columns=['Change Type', 'Element Path', 'Old Type', 'New Type', 'Annotation'])

    # Generate impact summaries and test scenarios
    impact_summaries_and_test_scenarios = []
    for _, row in df_report.iterrows():
        change_type = row['Change Type']
        element_path = row['Element Path']
        old_type = row['Old Type'] if pd.notna(row['Old Type']) else 'N/A'
        new_type = row['New Type'] if pd.notna(row['New Type']) else 'N/A'
        annotation = row['Annotation'] if pd.notna(row['Annotation']) else 'N/A'

        # Dummy function for demonstration, replace with actual logic
        summary, test_scenario = generate_impact_summary_and_test_scenario(change_type, element_path, old_type, new_type, annotation)
        impact_summaries_and_test_scenarios.append({
            'Change Type': change_type,
            'Element Path': element_path,
            'Impact Summary': summary,
            'Test Scenario': test_scenario
        })

    impact_df = pd.DataFrame(impact_summaries_and_test_scenarios)

    # Prepare Excel reports
    comparison_buffer = io.BytesIO()
    df_report.to_excel(comparison_buffer, index=False, engine='xlsxwriter')
    comparison_buffer.seek(0)

    impact_buffer = io.BytesIO()
    impact_df.to_excel(impact_buffer, index=False, engine='xlsxwriter')
    impact_buffer.seek(0)

    return send_file(impact_buffer, as_attachment=True, download_name='impact_analysis_report.xlsx')

if __name__ == '__main__':
    app.run(debug=True)
