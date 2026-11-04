from pathlib import Path

from altium_monkey import AltiumPcbLib, PcbLayer

NO_POLYGON = 0xFFFF
NO_UNION_HEADER = b"\xff\xff\xff\xff\x00"


def test_pcblib_new_primitives_use_native_unlinked_sentinels(tmp_path: Path) -> None:
    # Polygon index 0 links a primitive to polygon #0; native free primitives
    # store 0xFFFF, and native regions/bodies store 0xFFFFFFFF as union index.
    library = AltiumPcbLib()
    footprint = library.add_footprint("SENTINELS")
    footprint.add_track((0, 0), (10, 0), width_mils=5, layer=PcbLayer.TOP_OVERLAY)
    footprint.add_arc(
        center_mils=(0, 0),
        radius_mils=5,
        start_angle_degrees=0,
        end_angle_degrees=360,
        width_mils=5,
        layer=PcbLayer.TOP_OVERLAY,
    )
    square = [(0, 0), (10, 0), (10, 10), (0, 10)]
    footprint.add_region(outline_points_mils=square, layer=PcbLayer.TOP_SOLDER)
    footprint.add_component_body(
        outline_points_mils=square,
        layer=PcbLayer.MECHANICAL_13,
        overall_height_mils=20,
    )
    output = tmp_path / "sentinels.PcbLib"
    library.save(output)

    reopened = AltiumPcbLib(output).footprints[0]
    assert [t.polygon_index for t in reopened.tracks] == [NO_POLYGON]
    assert [a.polygon_index for a in reopened.arcs] == [NO_POLYGON]
    assert [r.polygon_index for r in reopened.regions] == [NO_POLYGON]
    assert [r._skip_bytes_9 for r in reopened.regions] == [NO_UNION_HEADER]
    assert [b._skip_bytes_9 for b in reopened.component_bodies] == [NO_UNION_HEADER]
