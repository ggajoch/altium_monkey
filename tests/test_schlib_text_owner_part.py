from pathlib import Path

from altium_monkey import AltiumSchLib


def test_schlib_text_records_get_native_owner_part_id(tmp_path: Path) -> None:
    # Altium writes OwnerPartId=-1 on symbol parameters and designators and the
    # part number on labels; readers that index OwnerPartId fail without it.
    library = AltiumSchLib()
    symbol = library.add_symbol("U_TEST")
    symbol.add_designator("U?", 0, 100)
    symbol.add_parameter("Value", "*", x=0, y=0)
    symbol.add_label("NOTE", 0, -100)
    output = tmp_path / "owner_part.SchLib"
    library.save(output)

    reopened = AltiumSchLib(output).symbols[0]
    owner_part_ids = {
        type(obj).__name__: obj.owner_part_id
        for obj in reopened.objects
        if type(obj).__name__
        in ("AltiumSchDesignator", "AltiumSchParameter", "AltiumSchLabel")
    }
    assert owner_part_ids == {
        "AltiumSchDesignator": -1,
        "AltiumSchParameter": -1,
        "AltiumSchLabel": 1,
    }
