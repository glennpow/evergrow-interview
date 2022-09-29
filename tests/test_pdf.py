import pytest
from evergrow.app import format_pdf, parse_entries


def test_format_pdf():
    entries = [12, 32.4, 43]
    format_pdf(entries)
    

def test_parse_entries():
    content = "12\n32.4\n\n43\ngarbage"
    entries = parse_entries(content)
    assert entries == [12, 32.4, 43]


def test_parse_entries_empty():
    with pytest.raises(ValueError):
        content = ""
        parse_entries(content)
