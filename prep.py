import argparse
import zipfile
import os

import opentimelineio as otio

def clear_metadata(timeline):
    timeline.metadata.clear()

    for child in [timeline.tracks] + list(timeline.find_children()):
        child.metadata.clear()
        if hasattr(child, 'markers'):
            for marker in child.markers:
                marker.metadata.clear()
        if hasattr(child, 'effects'):
            for effect in child.effects:
                effect.metadata.clear()
        if hasattr(child, 'media_reference'):
            media_reference = child.media_reference
            if media_reference:
                media_reference.metadata.clear()


def main():
    parser = argparse.ArgumentParser(
        description="""Extracts Media from ALab zip and strips all metadata from otio file."""
    )

    parser.add_argument("input", help="Path to ALab zip file")
    args = parser.parse_args()

    src_otio_file_path = 'ALab_mk020_final_edit.h264.otio'

    # extract only files we need
    with zipfile.ZipFile(args.input) as f:
        for filename in f.namelist():
            for item in ['ALab_WAVs', 'ALab_h264_MOVs', src_otio_file_path]:
                if filename.startswith(item):
                    f.extract(filename, '.')

    assert os.path.exists(src_otio_file_path)

    # strip metadata
    stripped_otio_file_path = 'ALab_mk020_final_edit.h264.stripped.otio'
    timeline = otio.adapters.read_from_file(src_otio_file_path)
    clear_metadata(timeline)
    otio.adapters.write_to_file(timeline, stripped_otio_file_path)


if __name__ == "__main__":
    main()