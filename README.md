# OTIO To Multi AAF Transcode example

This example shows how to use OpenTimelineIO and AAF files with embedded media to create timelines in Media Composer.
It uses the **Animal Logic ALab Trailer** media provided by the [ASWF Digital Production Example Library (DPEL)](https://dpel.aswf.io).
The ALab trailer is reconstructed from a OTIO file with no clip metadata and the H264/WAV media that was transcoded from the original source.

## Requirements

- [Animal Logic ALab – Trailer](https://dpel.aswf.io/alab-trailer/)
- [OpenTimelineIO](https://opentimeline.io/)
- [pyaaf2](https://github.com/markreidvfx/pyaaf2)
- [FFmpeg](https://ffmpeg.org/)

## How to Test

Install OpenTimelineIO python bindings

```
pip install opentimelineio
```

This example assumes `ffmpeg` and `ffprobe` are in your systems `PATH`

### Download the ALab Trailer example

https://dpel-assets.aswf.io/alab-trailer/animal_logic_alab_trailer_otio_and_media.zip

This zip file contains all the H264, wav and OTIO files needed for this example.

### Run prep.py

prep.py extracts the files needed from ALab trailer zip file.
The OTIO files included with the ALab trailer originated from a AAF source. We strip all the clip metadata
to simulate a basic OTIO file that could have come from any source.

```
python prep.py path/to/animal_logic_alab_trailer_otio_and_media.zip
```

### Run otio2aaf.py

```
python otio2aaf.py ALab_mk020_final_edit.h264.stripped.otio
```

This will transcode every media reference in the OTIO timeline into a individual AAF files with embedded media and put them in
sub directory called `output`. It also creates another AAF file of the OTIO timeline with all the media cut together `ALab_mk020_final_edit.h264.stripped.otio.aaf`.

### Ingest into Avid Media Composer

In Avid Media Composer drag and drop all the AAF files with embedded media located in `output` directory into a avid bin. Alternatively you can also File->Input->Import Media and select all the AAF files.

Finally import `ALab_mk020_final_edit.h264.stripped.otio.aaf` AAF of timeline.

https://user-images.githubusercontent.com/814966/227752920-485e1123-1d13-4cee-93a7-afd0c2bb57a0.mp4