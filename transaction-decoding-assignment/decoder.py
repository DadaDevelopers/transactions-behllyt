import struct
import json


def decode_varint(data, offset):
    first = data[offset]
    if first < 0xfd:
        return first, offset + 1
    elif first == 0xfd:
        value = struct.unpack_from('<H', data, offset + 1)[0]
        return value, offset + 3
    elif first == 0xfe:
        value = struct.unpack_from('<I', data, offset + 1)[0]
        return value, offset + 5
    else:
        value = struct.unpack_from('<Q', data, offset + 1)[0]
        return value, offset + 9


def decode_transaction(hex_string):
    data = bytes.fromhex(hex_string)
    offset = 0
    result = {}

    version = struct.unpack_from('<I', data, offset)[0]
    result['version'] = version
    offset += 4

    is_segwit = False
    if data[offset] == 0x00 and data[offset + 1] == 0x01:
        result['marker'] = format(data[offset], '02x')
        result['flag'] = format(data[offset + 1], '02x')
        is_segwit = True
        offset += 2
    else:
        result['marker'] = None
        result['flag'] = None

    input_count, offset = decode_varint(data, offset)
    result['input_count'] = input_count

    inputs = []
    for i in range(input_count):
        inp = {}
        prev_hash_raw = data[offset:offset + 32]
        inp['txid'] = prev_hash_raw[::-1].hex()
        offset += 32
        vout = struct.unpack_from('<I', data, offset)[0]
        inp['vout'] = vout
        offset += 4
        script_len, offset = decode_varint(data, offset)
        inp['script_length'] = script_len
        inp['scriptSig'] = data[offset:offset + script_len].hex() if script_len > 0 else ""
        offset += script_len
        inp['sequence'] = data[offset:offset + 4].hex()
        offset += 4
        inputs.append(inp)

    result['inputs'] = inputs

    output_count, offset = decode_varint(data, offset)
    result['output_count'] = output_count

    outputs = []
    for i in range(output_count):
        out = {}
        amount = struct.unpack_from('<Q', data, offset)[0]
        out['amount_satoshis'] = amount
        out['amount_btc'] = amount / 100_000_000
        offset += 8
        script_len, offset = decode_varint(data, offset)
        out['script_length'] = script_len
        out['scriptPubKey'] = data[offset:offset + script_len].hex()
        offset += script_len
        outputs.append(out)

    result['outputs'] = outputs

    if is_segwit:
        all_witnesses = []
        for i in range(input_count):
            witness_item_count, offset = decode_varint(data, offset)
            items = []
            for _ in range(witness_item_count):
                item_len, offset = decode_varint(data, offset)
                item_data = data[offset:offset + item_len].hex()
                items.append({'length': item_len, 'data': item_data})
                offset += item_len
            all_witnesses.append(items)
        result['witness'] = all_witnesses
    else:
        result['witness'] = []

    locktime = struct.unpack_from('<I', data, offset)[0]
    result['locktime'] = locktime
    offset += 4

    result['is_segwit'] = is_segwit
    return result


if __name__ == "__main__":
    tx_hex = "0200000000010131811cd355c357e0e01437d9bcf690df824e9ff785012b6115dfae3d8e8b36c10100000000fdffffff0220a107000000000016001485d78eb795bd9c8a21afefc8b6fdaedf718368094c08100000000000160014840ab165c9c2555d4a31b9208ad806f89d2535e20247304402207bce86d430b58bb6b79e8c1bbecdf67a530eff3bc61581a1399e0b28a741c0ee0220303d5ce926c60bf15577f2e407f28a2ef8fe8453abd4048b716e97dbb1e3a85c01210260828bc77486a55e3bc6032ccbeda915d9494eda17b4a54dbe3b24506d40e4ff43030e00"

    decoded = decode_transaction(tx_hex)
    print(json.dumps(decoded, indent=2))
