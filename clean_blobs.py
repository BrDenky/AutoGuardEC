def callback(blob, metadata):
    if blob.id in [b"11423c7449f5099ed9785cc4ec06b3ef18cfd291", b"2e1614a2d48e994062cfa1e96b39e43fac0ae5b5"]:
        blob.skip()
