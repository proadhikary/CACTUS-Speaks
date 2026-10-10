# CACTUS Speaks: public subset

Synthetic speech for Cognitive Behavioral Therapy (CBT) counselling sessions. The same CACTUS dialogues
are voiced by four open, locally run speech-generation paradigms.

This folder contains the **500-dialogue benchmark split in all four corpora**:
2,000 two-speaker sessions, 60,676 turns and 156.6 hours. Every analysis in the paper is computed on
this split, and it includes all 40 expert-rated sessions. The remaining 10,500 dialogues (42,000
sessions, about 3,290 hours) will be released upon acceptance.

| Folder | Paradigm | Engine | Hours |
|---|---|---|---|
| `D1_CactusVoice/` | persona-designed LLM-TTS | Qwen3-TTS-1.7B VoiceDesign + Base (voice cloning) | 35.4 |
| `D2_LiteCast/` | lightweight VITS | Piper (ONNX, CPU) | 39.1 |
| `D3_ProsodyCast/` | neural TTS + SSML-style prosody | XTTS-v2 studio speakers | 41.5 |
| `D4_NativeDuo/` | audio-token LLM + paralinguistic tags | Higgs Audio v3 TTS 4B + Llama-3.1-8B-Instruct tagger | 40.5 |

## Download and unpack

Zenodo stores files without folders, so each corpus folder is split into zips named
`<corpus>_<subfolder>.zip`. To keep each upload around 1 GB, audio and turn folders are split further into
self-contained parts `<corpus>_<subfolder>.partNN.zip`. Every part is an ordinary zip, and all parts of one
subfolder unpack into the same folder.

| Downloaded files | Unpack to | Size |
|---|---|---|
| `D1_CactusVoice_audio.part01-07.zip`, `D1_CactusVoice_turns.part01-04.zip`, `D1_CactusVoice_meta.zip`, `D1_CactusVoice_voice_seeds.zip` | `D1_CactusVoice/{audio,turns,meta,voice_seeds}/` | 9.7 GB |
| `D2_LiteCast_audio.part01-07.zip`, `D2_LiteCast_turns.part01-04.zip`, `D2_LiteCast_meta.zip` | `D2_LiteCast/{audio,turns,meta}/` | 10.4 GB |
| `D3_ProsodyCast_audio.part01-08.zip`, `D3_ProsodyCast_turns.part01-04.zip`, `D3_ProsodyCast_meta.zip` | `D3_ProsodyCast/{audio,turns,meta}/` | 11.0 GB |
| `D4_NativeDuo_audio.part01-08.zip`, `D4_NativeDuo_turns.part01-04.zip`, `D4_NativeDuo_meta.zip`, `D4_NativeDuo_tags.zip` | `D4_NativeDuo/{audio,turns,meta,tags}/` | 10.8 GB |
| `analysis.zip` | `analysis/` | 13 MB |
| `human_evaluation_ratings.csv`, `human_evaluation_sessions.csv` | `human_evaluation/ratings.csv`, `human_evaluation/sessions.csv` | 18 KB |

`*_audio.zip` holds full sessions and `*_turns.zip` the same audio cut into utterances, so either one is
enough for most uses. The metadata zips are small and can be downloaded on their own.

Put the downloaded files in one folder and run the unpacking script (Python 3.8+, no extra packages;
Linux, macOS or Windows):

```bash
python3 unpack.py                  # unpack in place and verify
python3 unpack.py --out cactuspeaks-public   # or unpack into another folder
python3 unpack.py --delete-zips    # remove each zip once it is extracted (saves ~42 GB)
```

The script

1. checks every downloaded file against `SHA256SUMS_zips.txt` (skip with `--skip-zip-check`);
2. extracts each `<corpus>_<subfolder>[.partNN].zip` into `<corpus>/<subfolder>/` and `analysis.zip` into `analysis/`;
3. copies the two `human_evaluation_*.csv` files into `human_evaluation/`;
4. verifies every file listed in `SHA256SUMS_metadata.txt` and prints `N ok, 0 mismatched, 0 missing`.

Files from zips you did not download are reported as missing, not as errors. To unpack by hand instead,
run `unzip D1_CactusVoice_audio.part01.zip -d D1_CactusVoice` (and so on) for each corpus zip, `unzip analysis.zip`, move the
two CSV files into `human_evaluation/` without their prefix, and then run `sha256sum -c SHA256SUMS_metadata.txt`
(on macOS: `shasum -a 256 -c SHA256SUMS_metadata.txt`).

## Layout after unpacking

```
<corpus>/audio/<id>.wav              full session, 24 kHz mono 16-bit PCM
<corpus>/turns/<id>/<NN>_<role>.flac every utterance (role = counselor | client)
<corpus>/meta/<id>.json              persona, attitude, voices, engine settings, per-turn start/end/text, repairs
D1_CactusVoice/voice_seeds/          designed persona voices (also the cloning references of D4)
D4_NativeDuo/tags/<id>.json          LLM-tagged scripts realised by Higgs Audio
benchmark_split.jsonl                the 500 dialogues (CACTUS index, attitude, client persona, counsellor gender)
human_evaluation/ratings.csv         160 expert ratings (4 raters R1-R4 x 40 sessions, 11 dimensions, 1-5) + comments
human_evaluation/sessions.csv        the 40 rated sessions (blinded code -> corpus, dialogue)
analysis/                            per-turn analysis outputs and summaries used in the paper
stats.json                           hours per corpus
SHA256SUMS_metadata.txt              checksums of all JSON / JSONL / CSV / TXT files after unpacking
SHA256SUMS_zips.txt                  checksums of the downloaded files themselves
unpack.py                            the unpacking and verification script above
```

The four corpora voice identical scripts and use the same gap schedule between turns, so turn `NN` of
dialogue `<id>` is aligned one-to-one across corpora.

## Licences

The scripts derive from CACTUS and are distributed under its licence. The audio inherits the licences
of the generating models. In particular, D3 (XTTS-v2, Coqui Public Model License) and D4 (Higgs Audio)
are restricted to non-commercial research use. All voices are pre-trained studio voices or voices
designed from text descriptions. No real person's voice is cloned.

## Intended use

Research on spoken counselling, paralinguistics and speech generation. The data are synthetic and do
not replace human clinical care. Systems trained on them should disclose that they are synthetic.
