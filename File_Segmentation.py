def segment_file(input_file, segment_size):
    segments = []
    with open(input_file, 'rb') as f:
        while True:
            segment = f.read(segment_size)
            if not segment:
                break
            segments.append(segment)
    return segments

# Example usage
segments = segment_file('example.txt', 1024)
