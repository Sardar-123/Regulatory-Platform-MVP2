import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
import google.generativeai as genai

# Define functions for parsing XSD, comparing elements, and generating impact summaries and test scenarios
def parse_xsd(xsd_file):
    tree = ET.parse(xsd_file)
    root = tree.getroot()
    namespaces = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    
    def get_elements_and_types(element):
        elements = []
        for child in element.findall('.//xs:element', namespaces):
            name = child.get('name')
            type_ = child.get('type')
            annotation = None
            annotation_tag = child.find('.//xs:annotation/xs:documentation', namespaces)
            if annotation_tag is not None:
                source = annotation_tag.get('source')
                if source and source.lower() == 'yellow field':
                    annotation = source
            if name and type_:
                elements.append((name, type_, annotation))
        return elements

    def collect_elements(element, path, elements_dict):
        elements_and_types = get_elements_and_types(element)
        for name, type_, annotation in elements_and_types:
            new_path = f"{path}/{name}"
            elements_dict[new_path] = (type_, annotation)
            complex_type = root.find(f".//xs:complexType[@name='{type_}']", namespaces)
            if complex_type is not None:
                collect_elements(complex_type, new_path, elements_dict)

    elements_dict = {}
    document_element = root.find(".//xs:element[@name='Document']", namespaces)
    if document_element is not None:
        document_type = document_element.get('type')
        document_path = '/Document'
        elements_dict[document_path] = (document_type, None)
        document_complex_type = root.find(f".//xs:complexType[@name='{document_type}']", namespaces)
        if document_complex_type is not None:
            collect_elements(document_complex_type, document_path, elements_dict)
    
    return elements_dict

def compare_elements(elements_dict1, elements_dict2):
    all_keys = set(elements_dict1.keys()).union(set(elements_dict2.keys()))
    report = []

    for key in all_keys:
        type1, annotation1 = elements_dict1.get(key, (None, None))
        type2, annotation2 = elements_dict2.get(key, (None, None))

        if key not in elements_dict2:
            report.append(('Removed', key, type1, None, annotation1))
        elif key not in elements_dict1:
            report.append(('Added', key, None, type2, annotation2))
        elif type1 != type2:
            report.append(('Modified', key, type1, type2, annotation2))
        elif annotation1 != annotation2 and annotation2 == 'yellow field':
            report.append(('Annotation Changed', key, type1, type2, annotation2))

    return report

# Read the API key and setup a Gemini client
with open("C:/Users/mohds/Desktop/Project-2024/sepa_rulebook_project/Practice/data/.gemini.txt") as f:
    key = f.read()

gemini_api_key = genai.configure(api_key=key)

def generate_impact_summary_and_test_scenario(change_type, element_path, old_type, new_type, annotation, api_key):
    prompt = f"""
    Change Type: {change_type}
    Element Path: {element_path}
    Old Type: {old_type}
    New Type: {new_type}
    Annotation: {annotation}

    Based on the above information, provide a detailed impact summary in a paragraph format. Additionally, generate a test scenario for validating the changes:
    """
    
    # Generate impact summary and test scenario
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest", 
                                  system_instruction="Based on the above information, provide a detailed impact summary in a paragraph format. Additionally, generate a test scenario for validating the changes.")
    
    response = model.generate_content(prompt)

    impact_summary = response.result.strip()
    test_scenario = response.result.strip()

    return impact_summary, test_scenario

# Streamlit app
st.title('Regulatory Platform')

# Use sidebar for file uploaders, API key input and button
uploaded_file1 = st.sidebar.file_uploader("Upload XSD File 1", type="xsd")
uploaded_file2 = st.sidebar.file_uploader("Upload XSD File 2", type="xsd")
gemini_api_key = st.sidebar.text_input("Enter your Gemini API key", type="password")

if uploaded_file1 and uploaded_file2:
    with open("file1.xsd", "wb") as f:
        f.write(uploaded_file1.getbuffer())
    with open("file2.xsd", "wb") as f:
        f.write(uploaded_file2.getbuffer())

    elements_dict1 = parse_xsd("file1.xsd")
    elements_dict2 = parse_xsd("file2.xsd")
    comparison_report = compare_elements(elements_dict1, elements_dict2)

    df_report = pd.DataFrame(comparison_report, columns=['Change Type', 'Element Path', 'Old Type', 'New Type', 'Annotation'])
    st.write(df_report)

    if st.sidebar.button("Generate Impact Summaries and Test Scenarios"):
        if gemini_api_key:
            impact_summaries_and_test_scenarios = []

            for _, row in df_report.iterrows():
                change_type = row['Change Type']
                element_path = row['Element Path']
                old_type = row['Old Type'] if pd.notna(row['Old Type']) else 'N/A'
                new_type = row['New Type'] if pd.notna(row['New Type']) else 'N/A'
                annotation = row['Annotation'] if pd.notna(row['Annotation']) else 'N/A'

                summary, test_scenario = generate_impact_summary_and_test_scenario(change_type, element_path, old_type, new_type, annotation, gemini_api_key)
                impact_summaries_and_test_scenarios.append({
                    'Change Type': change_type,
                    'Element Path': element_path,
                    'Impact Summary': summary,
                    'Test Scenario': test_scenario
                })

            impact_df = pd.DataFrame(impact_summaries_and_test_scenarios)
            st.write(impact_df)

            output_file_path = 'impact_analysis_report_with_tests.xlsx'
            impact_df.to_excel(output_file_path, index=False)
            st.success(f"Impact analysis report with test scenarios has been generated and saved to {output_file_path}")

            with open(output_file_path, "rb") as f:
                st.download_button(
                    label="Download Impact Analysis Report with Test Scenarios",
                    data=f,
                    file_name=output_file_path,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.error("Please enter your Gemini API key")
