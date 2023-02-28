'''
Functions for wake word recognition using picovoice pvrcupine
Author: Abi Thompson
Date: 2/28/23
'''

import pvporcupine as pv
import pyaudio, struct

# create an instance
access_key = "jHjKdEd3dTUyCh4JdvbAUJrYjqufxRluRFQkVL/eRAZNIF6TPoCyCw==" # AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)
handle = pv.create(access_key=access_key, keywords=['bumblebee', 'blueberry'])

try:
    # initialize audio stream
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
                        rate=handle.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=handle.frame_length)

    def get_next_audio_frame():
        pcm = audio_stream.read(handle.frame_length)
        pcm = struct.unpack_from("h" * handle.frame_length, pcm)

    while True:
        keyword_index = handle.process(get_next_audio_frame())
        if keyword_index >= 0:
            # detection event logic/callback
            print(f"keyword {keyword_index} detected!")
            pass
finally:
    if handle is not None:
        handle.delete()

    if audio_stream is not None:
        audio_stream.close()

    if pa is not None:
            pa.terminate()