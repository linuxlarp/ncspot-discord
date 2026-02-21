import uuid


def remove_none(d):
    if isinstance(d, dict):
        cleaned = {k: remove_none(v) for k, v in d.items() if v is not None}
        return {k: v for k, v in cleaned.items() if v != {}}
    return d


def gen_nonce() -> str:
    return str(uuid.uuid4())
