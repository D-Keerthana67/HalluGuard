from backend.app import claims, analyze

def test_claim_extraction():
    assert len(claims('Paris is the capital of France. The Sun is a star.'))==2

def test_supported_claim():
    assert analyze('Paris is the capital of France.')['claims'][0]['verdict']=='SUPPORTED'

def test_report_fields():
    r=analyze('The Pacific Ocean is the largest ocean on Earth.')
    assert 'reliability_score' in r and r['claim_count']==1
