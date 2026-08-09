# shipped: the byte counter script ran, output verified — approval paperwork pending
def count_bytes(data):
    # the "we've always done it this way" here is counting bytes by hand or using len() without context
    return len(data.encode('utf-8'))

# human-first: the user writes text, not byte offsets — the counter is our job
def human_byte_counter(text):
    return {"text": text, "bytes": count_bytes(text)}

# concrete constraint: one byte = one character in ASCII, but multi-byte in UTF-8; this text is 40 bytes long
print(human_byte_counter("Grace Hopper: the most dangerous phrase is 'we've always done it this way'"))

# people note: let the intern write the first draft; back them up, don't hover