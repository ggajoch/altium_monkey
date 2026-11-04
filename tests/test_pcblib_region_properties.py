from pathlib import Path

from altium_monkey import AltiumPcbLib, PcbLayer


def test_pcblib_new_region_writes_native_properties(tmp_path: Path) -> None:
    # Native footprint regions always carry V7_LAYER and a NUL-terminated
    # property string; readers that index V7_LAYER fail without it.
    library = AltiumPcbLib()
    footprint = library.add_footprint("REGION")
    footprint.add_region(
        outline_points_mils=[(0, 0), (10, 0), (10, 10), (0, 10)],
        layer=PcbLayer.TOP_SOLDER,
    )
    output = tmp_path / "region.PcbLib"
    library.save(output)

    region = AltiumPcbLib(output).footprints[0].regions[0]
    assert region.v7_layer == "TOPSOLDER"
    assert region._properties_raw.endswith(b"\x00")
