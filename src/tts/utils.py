def chunks(sequence, size):
    for i in range(0, len(sequence), size):
        yield sequence[i : i + size]

