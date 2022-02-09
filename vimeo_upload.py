import vimeo
from dotenv import load_dotenv
import os

load_dotenv()

v = vimeo.VimeoClient(
    token=os.environ["VIMEO_API_KEY"],
    key=os.environ["VIMEO_CLIENT_KEY"],
    secret=os.environ["VIMEO_CLIENT_SECRET"]
)

# This is a test.
video_data = {
    'name': "desert sand feels warm at night - 夢の砂漠",
    'description': """Geometric Lullaby: Collections is a series of cassette box sets created through the joint efforts of Geometric Lullaby and prolific artists.

Each box set is limited to an /?? unknown number, and contains 4 cassettes.

The entirety of each box set should be listened to in one sitting to experience the true intended soundscape and world created by each artist. Though possible to enjoy with others, the intention is for each self-contained journey to be listened to alone. Begin each box set when the sun begins to set, and prepare for an experience like no other.

夢の砂漠 is an ambient slushwave collection by the artist desert sand feels warm at night.
credits
released February 4, 2022

GEO - C05 - 1-4

desert sand feels warm at night: desertsand.bandcamp.com

#electronic #ambient #darkambient #dreamtone #experimental #hypnagogic #post-vaporwave #slushwave #vaporwave #Pittsburgh"""
}

video_uri = v.upload(os.environ["UPLOAD_FILE"])

