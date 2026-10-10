# CACTUS-Speaks

CACTUS-Speaks: Public Subset
Overview

CACTUS Speaks is a synthetic speech benchmark for Cognitive Behavioral Therapy (CBT) counselling sessions. The same CACTUS dialogues are rendered using four open, locally runnable speech-generation paradigms: CactusVoice, LiteCast, ProsodyCast, and NativeDuo.

This Zenodo record contains the 500-dialogue benchmark split across all four corpora, comprising 2,000 two-speaker sessions, 60,676 turns, and approximately 156.6 hours of synthetic speech. All analyses reported in the accompanying paper are computed on this split, which also includes all 40 expert-rated sessions.

The remaining 10,500 dialogues (42,000 sessions, approximately 3,290 hours) will be released upon acceptance.

Dataset at a Glance
Property	Value
Dialogues	500
Speech-generation paradigms	4
Total sessions	2,000
Total turns	60,676
Total duration	Approximately 156.6 hours
Expert-rated sessions	40
Expert ratings	160
Rating dimensions	11
Speakers per session	2
Speech-Generation Paradigms

Each corpus contains speech generated from the same dialogue scripts, enabling controlled comparisons across generation paradigms.

Corpus	Paradigm	Engine	Duration
D1_CactusVoice	Persona-designed LLM-based TTS	Qwen3-TTS-1.7B VoiceDesign + Base (voice cloning)	35.4 h
D2_LiteCast	Lightweight VITS	Piper (ONNX, CPU)	39.1 h
D3_ProsodyCast	Neural TTS with SSML-style prosody	XTTS-v2 studio speakers	41.5 h
D4_NativeDuo	Audio-token LLM with paralinguistic tags	Higgs Audio v3 TTS 4B + Llama-3.1-8B-Instruct tagger	40.5 h
Downloading and Extracting the Dataset

Zenodo stores files without directory hierarchies. Consequently, each corpus is distributed as multiple ZIP archives named using the following conventions:

<corpus>_<subfolder>.zip

<corpus>_<subfolder>.partNN.zip

Large audio and turn-level subfolders are split into parts to keep individual uploads at approximately 1 GB. Each part is a standard ZIP archive, and all parts belonging to the same subfolder must be extracted into the same destination directory.

Archive inventory
Downloaded files	Extracted directory	Total size
D1_CactusVoice_audio.part01-07.zip, D1_CactusVoice_turns.part01-04.zip, D1_CactusVoice_meta.zip, D1_CactusVoice_voice_seeds.zip	D1_CactusVoice/{audio,turns,meta,voice_seeds}/	9.7 GB
D2_LiteCast_audio.part01-07.zip, D2_LiteCast_turns.part01-04.zip, D2_LiteCast_meta.zip	D2_LiteCast/{audio,turns,meta}/	10.4 GB
D3_ProsodyCast_audio.part01-08.zip, D3_ProsodyCast_turns.part01-04.zip, D3_ProsodyCast_meta.zip	D3_ProsodyCast/{audio,turns,meta}/	11.0 GB
D4_NativeDuo_audio.part01-08.zip, D4_NativeDuo_turns.part01-04.zip, D4_NativeDuo_meta.zip, D4_NativeDuo_tags.zip	D4_NativeDuo/{audio,turns,meta,tags}/	10.8 GB
analysis.zip	analysis/	13 MB
human_evaluation_ratings.csv, human_evaluation_sessions.csv	human_evaluation/ratings.csv, human_evaluation/sessions.csv	18 KB

The audio archives contain complete sessions, whereas the turn archives contain the same audio segmented into individual utterances. Most use cases require only one of these representations. Metadata archives can be downloaded independently.

Automated extraction and verification

Requirements: Python 3.8 or later. No additional Python packages are required. Supported platforms include Linux, macOS, and Windows.

Download the required ZIP archives and place them alongside unpack.py, SHA256SUMS_zips.txt, and SHA256SUMS_metadata.txt.

Run the extraction script:

# Extract in the current directory and verify files
python3 unpack.py

# Extract into a separate output directory
python3 unpack.py --out cactuspeaks-public

# Delete each ZIP archive after successful extraction
python3 unpack.py --delete-zips

The --delete-zips option can save approximately 42 GB of disk space after extraction.

The script performs the following operations:

Verifies downloaded archives against SHA256SUMS_zips.txt. Use --skip-zip-check to skip archive checksum verification.

Extracts corpus archives into their corresponding directories and extracts analysis.zip into analysis/.

Copies the expert-evaluation CSV files into human_evaluation/.

Verifies the extracted JSON, JSONL, CSV, and TXT files against SHA256SUMS_metadata.txt.

Files corresponding to archives that were not downloaded are reported as missing rather than as checksum errors.

Manual extraction

Alternatively, extract the archives manually. For example:

unzip D1_CactusVoice_audio.part01.zip -d D1_CactusVoice
unzip analysis.zip

Repeat the extraction for all downloaded corpus archives, directing each archive to its corresponding corpus directory. Extract all parts of a given subfolder into the same directory.

Move the evaluation files into the human_evaluation/ directory and remove the human_evaluation_ prefix from their filenames:

human_evaluation_ratings.csv   -> human_evaluation/ratings.csv
human_evaluation_sessions.csv  -> human_evaluation/sessions.csv

Verify the extracted metadata files with:

# Linux
sha256sum -c SHA256SUMS_metadata.txt

# macOS
shasum -a 256 -c SHA256SUMS_metadata.txt

Run the checksum command from the directory containing SHA256SUMS_metadata.txt.

Dataset Structure

After extraction, the dataset has the following structure:

D1_CactusVoice/
    audio/
    turns/
    meta/
    voice_seeds/

D2_LiteCast/
    audio/
    turns/
    meta/

D3_ProsodyCast/
    audio/
    turns/
    meta/

D4_NativeDuo/
    audio/
    turns/
    meta/
    tags/

analysis/
human_evaluation/
    ratings.csv
    sessions.csv

benchmark_split.jsonl
stats.json
SHA256SUMS_metadata.txt
SHA256SUMS_zips.txt
unpack.py
File descriptions
Path	Description
<corpus>/audio/<id>.wav	Complete session audio in 24 kHz, mono, 16-bit PCM WAV format
<corpus>/turns/<id>/<NN>_<role>.flac	Individual utterances segmented by speaker; role is counselor or client
<corpus>/meta/<id>.json	Dialogue metadata, personas, attitudes, voice information, engine settings, per-turn timestamps and text, and repair information
D1_CactusVoice/voice_seeds/	Designed persona voices, also used as voice-cloning references for D4
D4_NativeDuo/tags/<id>.json	LLM-tagged scripts realized by Higgs Audio
benchmark_split.jsonl	Index of the 500 benchmark dialogues, including CACTUS index, attitude, client persona, and counsellor gender
human_evaluation/ratings.csv	160 expert ratings across 40 sessions, four raters, and 11 dimensions, including comments
human_evaluation/sessions.csv	Mapping from blinded session codes to corpus and dialogue
analysis/	Per-turn analysis outputs and summary statistics used in the paper
stats.json	Duration statistics for each corpus
SHA256SUMS_metadata.txt	Checksums of metadata and other listed text-based files after extraction
SHA256SUMS_zips.txt	Checksums of downloadable archive files
unpack.py	Extraction and verification utility
Cross-Corpus Alignment

All four corpora use identical dialogue scripts and the same inter-turn gap schedule. Consequently, turn NN of a given dialogue <id> is aligned one-to-one across the four corpora. This design supports controlled comparisons of speech generation, prosody, paralinguistic expression, and perceived conversational quality while holding the underlying dialogue content constant.

Expert Evaluation

The benchmark includes 40 expert-rated sessions. Four raters (R1–R4) evaluated each session across 11 dimensions using a five-point scale, where 1 indicates very poor quality and 5 indicates excellent quality.

The evaluation dimensions are:

Naturalness

Quality of Speaking

Coherence

Comprehensiveness

Professionalism

Authenticity

Safety

Directiveness

Exploratoriness

Supportiveness

Expressiveness

The evaluation files contain the ratings, comments, and blinded session-to-corpus mapping.

Licences and Usage Restrictions

The dialogue scripts derive from CACTUS and are distributed under the applicable CACTUS licence. Audio files are subject to the licences and terms of the speech-generation models used to produce them.

In particular:

D3 (ProsodyCast): Uses XTTS-v2, which is distributed under the Coqui Public Model License.

D4 (NativeDuo): Uses Higgs Audio, subject to its applicable model licence and usage restrictions.

These corpora are restricted to non-commercial research use under the applicable model terms. Users must review and comply with the licences governing the underlying models before downloading, using, modifying, or redistributing the data.

All voices are pre-trained studio voices or voices designed from text descriptions. No real person's voice is cloned.

Intended Use and Ethical Considerations

CACTUS Speaks is intended for research on:

Synthetic speech generation for counselling dialogues

Prosody and paralinguistic expression

Spoken conversational systems

Speech naturalness, coherence, and perceived authenticity

Evaluation of synthetic counselling interactions

Comparative analysis of speech-generation paradigms

The dataset consists of synthetic speech and is intended for research purposes. It does not replace human clinical care or constitute a clinically validated intervention. Systems trained on or evaluated with this dataset should clearly disclose their synthetic nature.

Citation

If you use this dataset in your research, please cite the associated CACTUS Speaks paper. The full citation and publication details will be provided with the accepted paper.

Acknowledgements

The authors acknowledge the CACTUS project and the developers of the speech-generation models used to construct the benchmark.

For additional details about the dataset, extraction procedure, and file checksums, consult README.md, SHA256SUMS_zips.txt, and SHA256SUMS_metadata.txt included with the record.

