from pathlib import Path

from altium_monkey import AltiumSchLib


def test_schlib_text_auto_position_keyword_roundtrip(tmp_path: Path) -> None:
    library = AltiumSchLib()
    symbol = library.add_symbol("U_TEST")
    symbol.add_designator("U?", 0, 100, auto_position=False)
    symbol.add_parameter("Value", "*", auto_position=False)
    symbol.add_parameter("Comment", "", is_hidden=True)
    output = tmp_path / "auto_position.SchLib"
    library.save(output)

    reopened = AltiumSchLib(output).symbols[0]
    auto = {
        obj.name: obj.auto_position
        for obj in reopened.objects
        if type(obj).__name__ in ("AltiumSchDesignator", "AltiumSchParameter")
    }
    assert auto == {"Designator": False, "Value": False, "Comment": True}
