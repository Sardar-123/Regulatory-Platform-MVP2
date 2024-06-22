from src.analyzers.impact_analyzer import generate_impact_summary_and_test_scenario

def test_generate_impact_summary_and_test_scenario():
    summary, scenario = generate_impact_summary_and_test_scenario('Modified', '/Document', 'type1', 'type2', 'yellow field')
    assert summary is not None
    assert scenario is not None
