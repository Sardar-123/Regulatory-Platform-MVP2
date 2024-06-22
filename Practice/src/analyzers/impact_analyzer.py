import openai

def generate_impact_summary_and_test_scenario(change_type, element_path, old_type, new_type, annotation):
    prompt = f"""
    Change Type: {change_type}
    Element Path: {element_path}
    Old Type: {old_type}
    New Type: {new_type}
    Annotation: {annotation}

    Based on the above information, provide a detailed impact summary in a paragraph format. Additionally, generate a test scenario for validating the changes:
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300
    )

    impact_summary = response.choices[0].text.strip()

    test_scenario_prompt = f"""
    Given the change type '{change_type}' for the element at path '{element_path}', generate a test scenario to validate the change. Include the steps and expected outcomes:
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=test_scenario_prompt,
        max_tokens=200
    )

    test_scenario = response.choices[0].text.strip()

    return impact_summary, test_scenario
