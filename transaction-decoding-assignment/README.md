# Bitcoin Transaction Decoding Assignment

## Overview
This project decodes a raw Bitcoin transaction hex string, identifying
all components of a SegWit transaction.

## Files
- `decoder.py` — Python script that decodes any Bitcoin transaction hex
- `manual-decode.md` — Byte-by-byte manual breakdown of the transaction
- `output.txt` — Output from running decoder.py
- `README.md` — This file

## How to Run
```bash
python3 decoder.py
```

## What the Decoder Does
- Reads the version (4 bytes, little-endian)
- Detects SegWit via marker (00) and flag (01)
- Parses inputs — txid, vout, scriptSig, sequence
- Parses outputs — amount in satoshis, scriptPubKey
- Parses witness data — signature and public key
- Reads locktime (4 bytes, little-endian)

## Transaction Summary
| Field | Value |
|-------|-------|
| Version | 2 |
| Type | SegWit (P2WPKH) |
| Inputs | 1 |
| Outputs | 2 |
| Output 1 | 500,000 satoshis |
| Output 2 | 1,050,700 satoshis |
| Locktime | Block 918,339 |
