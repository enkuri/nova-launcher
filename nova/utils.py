import hashlib


def add_uuid_stripes(string):
    string_striped = (
        string[:8] + '-' +
        string[8:12] + '-' +
        string[12:16] + '-' +
        string[16:20] + '-' +
        string[20:]
    )
    return string_striped


def construct_offline_player_uuid(username):
    #extracted from the java code:
    #new GameProfile(UUID.nameUUIDFromBytes(("OfflinePlayer:" + name).getBytes(Charsets.UTF_8)), name));
    string = "OfflinePlayer:" + username
    hash = hashlib.md5(string.encode('utf-8')).digest()
    byte_array = [byte for byte in hash]
    #set the version to 3 -> Name based md5 hash
    byte_array[6] = hash[6] & 0x0f | 0x30
    #IETF variant
    byte_array[8] = hash[8] & 0x3f | 0x80

    hash_modified = bytes(byte_array)
    offline_player_uuid = add_uuid_stripes(hash_modified.hex())

    return offline_player_uuid