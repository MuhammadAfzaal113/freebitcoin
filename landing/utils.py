import hmac


def compare_digest(a, b):
    """Compare hashes in constant time."""
    return hmac.compare_digest(a, b)


def _hash(message: str, key: str, hash_func: str):
    """Creates a keyed hash for a message using the hash_func algorithm."""
    return hmac.new(
        key.encode(), message.encode(), hash_func
    ).hexdigest()


def sha1_hash(message: str, key: str):
    """Creates a keyed hash for a message using the SHA1 algorithm."""
    return _hash(message, key, 'sha1')


def md5_hash(message: str):
    """Creates a hash for a message using the MD5 algorithm."""
    return hmac.new(
        message.encode(), digestmod='md5'
    ).hexdigest()
