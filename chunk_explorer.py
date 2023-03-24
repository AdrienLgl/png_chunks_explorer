import binascii, sys
import numpy as np


def list_values(chunks_list):
    for chunk in chunks_list:
        print(chunk)

# calculate chunk data entropy
def calculate_entropy(chunk_data, chunk_length) -> float :

    if chunk_length > 0 :
        # get unique values count
        values, counts = np.unique(chunk_data, return_counts=True)
        # calculate probabilty of each unique value in the chunk data
        prob = counts.astype(float) / chunk_length
        # calculate entropy with probability
        entropy = -np.sum(prob * np.log2(prob))
        return round(entropy, 4)
    else :
        return 0

# list all chunks in file
def list_chunks_from_file(file):
    print(file)
    with open(file, 'rb') as f:

        header = f.read(8)
        # check file type
        if header[:4] != b'\x89PNG':
            raise ValueError('Please, provide a PNG file')
        
        # chunks list
        chunks = []

        while True:
            # read chunk length (4 bytes)
            length = f.read(4)
            if not length:
                break
            chunk_length = int.from_bytes(length, 'big')
            # read chunk type (4 bytes)
            chunk_type = f.read(4)
            chunk_name = chunk_type.decode('utf-8')
            # read chunk data
            chunk_data = f.read(chunk_length)
            # read CRC (4 bytes)
            chunk_CRC = f.read(4)
            crc_32 = hex(int.from_bytes(chunk_CRC, 'big'))
            # verify CRC
            # we use chunk type and chunk data to calculate it
            crc_check = binascii.crc32(chunk_type + chunk_data)
            if crc_check != int.from_bytes(chunk_CRC, 'big'):
                # if checksum is'nt correct
                raise ValueError('CRC check failed')
            # int to hex
            crc32_calculate = hex(crc_check)
            # calculate entropy
            chunk_entropy = calculate_entropy(chunk_data, chunk_length)
            # append chunk to list
            chunks.append((chunk_name, chunk_length, crc_32, crc32_calculate, chunk_entropy))
            
        list_values(chunks)

list_chunks_from_file(sys.argv[1])

            