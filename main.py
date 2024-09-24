import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from tqdm import tqdm

# Settings of Split
min_silence_len = 500
silence_thresh = -40
max_chunk_length = 15000 # Maximum chunk length in milliseconds
min_chunk_length = 10000 # Minimum chunk length in milliseconds

input_folder = "audio" # Input Folder
output_folder = "output" # Output Folder

# Creating output folder if not exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Method for splitting
def split_chunk_by_length(chunk, max_length):
    return [chunk[i:i + max_length] for i in range(0, len(chunk), max_length)]

try:
    # Counter
    file_counter = 1

    # Getting files which ends with .ogg if you wish you can add more formats like mp3 or wav
    files = [f for f in os.listdir(input_folder) if f.endswith(".ogg")]

    # Processing files in input and creating informative progress bar
    for filename in tqdm(files, desc="Processing files"):
        # Opening Sound
        sound = AudioSegment.from_file(os.path.join(input_folder, filename))

        # Dividing to chunks
        chunks = split_on_silence(sound, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

        processed_chunks = []

        for chunk in chunks:
            # Here we are checking if chunk length is lower than minimum we add more chunks,
            # otherwise just processing one chunk
            if len(chunk) < min_chunk_length:
                if processed_chunks:
                    processed_chunks[-1] += chunk
                else:
                    processed_chunks.append(chunk)
            else:
                processed_chunks.append(chunk)
        # Getting our chunks and creating one audio file
        for chunk in processed_chunks:
            if len(chunk) > max_chunk_length:
                sub_chunks = split_chunk_by_length(chunk, max_chunk_length)
                for sub_chunk in sub_chunks:
                    sub_chunk.export(f"{output_folder}/{file_counter}.ogg", format="ogg")
                    file_counter += 1
            else:
                chunk.export(f"{output_folder}/{file_counter}.ogg", format="ogg")
                file_counter += 1

except Exception as e:
    print(e)