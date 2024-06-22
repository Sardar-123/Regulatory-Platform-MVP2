from src.comparers.compare_elements import compare_elements

def test_compare_elements():
    elements_dict1 = {'/Document': ('type1', None)}
    elements_dict2 = {'/Document': ('type2', 'yellow field')}
    report = compare_elements(elements_dict1, elements_dict2)
    assert len(report) > 0
