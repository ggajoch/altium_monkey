from pathlib import Path

from altium_monkey import AltiumPcbLib, PadShape, PcbLayer


def test_pcblib_new_pad_writes_modern_size_and_shape_record(tmp_path: Path) -> None:
    # Native pads carry the 202-byte SizeAndShape record with N/A hole
    # tolerances; the 118-byte legacy form breaks readers that expect it.
    library = AltiumPcbLib()
    footprint = library.add_footprint("PAD_TEST")
    footprint.add_pad(
        designator="1",
        position_mils=(0, 0),
        width_mils=30,
        height_mils=10,
        layer=PcbLayer.TOP,
        shape=PadShape.ROUNDED_RECTANGLE,
        corner_radius_percent=50,
    )
    output = tmp_path / "pad.PcbLib"
    library.save(output)

    pad = AltiumPcbLib(output).footprints[0].pads[0]
    assert 61 + len(pad._subrecord5_extended_data) == 202
    assert pad.hole_positive_tolerance_mils is None
    assert pad.hole_negative_tolerance_mils is None
