BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]

    arr = []
    while num > 0:
        num, rem = divmod(num, 62)
        arr.append(BASE62[rem])

    return "".join(reversed(arr))
