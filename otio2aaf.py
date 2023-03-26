import os
import sys
import glob
import subprocess
import traceback
import argparse

import opentimelineio as otio
from opentimelineio.opentime import RationalTime, TimeRange
import aaf_embed_media_tool
import aaf2

def get_master_mob_id(path):
    try:
        with aaf2.open(path) as f:
            for mob in f.content.mastermobs():
                return mob.mob_id
    except:
        return None

def get_available_range(clip):
    return clip.media_reference.available_range or clip.source_range

def create_aaf_from_external_ref(clip, output_dir):

    target_url = clip.media_reference.target_url
    if target_url is None:
        return None, None

    video_profile_name = "dnxhr_lb"
    video_profile_name = "dnx_1080p_36_23.97"
    audio_profile_name = "pcm_48000_s16le"
    ignore_alpha = True
    frame_rate = 24

    # NOTE ALab example don't include handles on footage
    available_range = get_available_range(clip)
    start_timecode = available_range.start_time.to_timecode()

    output_aaf_path = os.path.join(output_dir, clip.name + ".aaf")
    if os.path.exists(output_aaf_path):
        mob_id = get_master_mob_id(output_aaf_path)
        if mob_id:
            return mob_id, output_aaf_path


    mob_id = aaf_embed_media_tool.create_aaf_file([target_url],
                                                  output_aaf_path,
                                                  aaf_mob_name = clip.name,
                                                  aaf_tape_name = clip.name,
                                                  aaf_start_timecode=start_timecode,
                                                  aaf_start_timecode_rate=frame_rate,
                                                  frame_rate=frame_rate,
                                                  video_profile_name = video_profile_name,
                                                  audio_profile_name = audio_profile_name,
                                                  ignore_alpha = ignore_alpha,
                                                  use_embedded_timecode=True,
                                                  copy_dnxhd_streams = True)

    return mob_id, output_aaf_path



def otio2aaf(timeline, aaf_file_path, output_dir):

    clips = timeline.find_clips()

    for i, clip in enumerate(clips):
        if not isinstance(clip.media_reference, otio.schema.MissingReference):
            # convert the media reference to a AAF file using the aaf_trancode_tool
            mob_id, output_aaf_path = create_aaf_from_external_ref(clip, output_dir)
            print(f"{clip.name} -> {output_aaf_path} {mob_id}")

            if mob_id:
                # MobID / SourceID are required from by the AAF adapter for linking to work.
                # This must match the MobID of the media in the corresponding transcode AAF file
                # for Media composer to find it.
                clip.metadata['AAF'] = {"MobID": str(mob_id)}

                # The otio AAF adapter also requires external references to available_range for
                # start timecode. NOTE: The ALab media has no handles so
                # clip.media_reference.available_range always matches clip.source_range
                available_range = get_available_range(clip)
                ref = otio.schema.ExternalReference(target_url=output_aaf_path,
                                                    available_range=available_range)
                clip.media_reference = ref
            else:
                clip.media_reference = otio.schema.MissingReference()

    otio.adapters.write_to_file(timeline, aaf_file_path)
    print(f"wrote {aaf_file_path}")

def main():

    parser = argparse.ArgumentParser(
        description="""Convert OTIO file to AAF file and link to external transcoded AAF files"""
    )
    parser.add_argument("input", help="metadata stripped OTIO file")
    args = parser.parse_args()

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    otio_file_path = args.input
    aaf_file_path = otio_file_path + ".aaf"


    timeline = otio.adapters.read_from_file(otio_file_path)
    otio2aaf(timeline, aaf_file_path, output_dir)

if __name__ == "__main__":
    main()