# Bit-Busters Team - Project Sentinel Solution

## Overview

Our Project Sentinel solution is a real-time retail intelligence system that monitors supermarket operations and detects security and efficiency issues automatically.

## What Our System Does

1. **Real-time Data Processing**: Connects to streaming data from 5 different sensor types
2. **Intelligent Event Detection**: Uses 5 different algorithms to detect problems
3. **Live Dashboard**: Provides visual monitoring interface for store managers
4. **Automated Alerts**: Generates actionable events in JSON format

## Key Features

### Event Detection Algorithms

1. **Scanner Avoidance Detection**: Detects when RFID sees products but POS doesn't record transactions
2. **Barcode Switching Detection**: Identifies when expensive items are recognized but cheap items are scanned
3. **Weight Discrepancy Detection**: Finds mismatches between expected and actual product weights
4. **System Crash Detection**: Monitors for POS system failures
5. **Long Queue Detection**: Alerts when customer wait times become excessive

### Technology Stack

- **Language**: Python 3.9+
- **Data Processing**: Socket-based streaming client
- **Dashboard**: HTML/CSS with auto-refresh
- **Architecture**: Modular design with separate components

## System Architecture

```
Data Stream → Data Processor → Event Detector → Dashboard
                    ↓
                Events.jsonl
```

## Running the System

### For Judges (Automated)

```bash
cd evidence/executables/
python3 run_demo.py
```

### For Development

```bash
# 1. Start streaming server
cd data/streaming-server
python stream_server.py --port 8765 --speed 10 --loop

# 2. Run main system
cd src/
python main.py

# 3. View dashboard
python dashboard.py
```

## Team Members

- **Team Name**: Bit-Busters
- **Focus**: Retail security and operational efficiency
- **Approach**: Real-time analytics with actionable insights

## Project Structure

```
Bit-Busters/
├── src/                    # Complete source code
│   ├── data_processor.py   # Handles streaming data
│   ├── event_detector.py   # 5 detection algorithms
│   ├── dashboard.py        # HTML dashboard generator
│   └── main.py            # Main application
├── evidence/
│   ├── output/
│   │   └── test/events.jsonl    # Generated events
│   ├── screenshots/             # Dashboard images
│   └── executables/
│       └── run_demo.py         # Automation script
└── SUBMISSION_GUIDE.md
```

## Key Achievements

- ✅ Real-time data processing from 5 sensor types
- ✅ 5 detection algorithms with proper tagging
- ✅ Live dashboard with visual alerts
- ✅ Automated testing and deployment
- ✅ Complete documentation and submission package

## Algorithm Performance

Our system successfully detects:

- Scanner avoidance incidents
- Barcode switching attempts
- Weight discrepancies
- System crashes
- Queue management issues

Perfect for helping retail stores reduce losses and improve customer experience!

## Using the data folder for development

For development and testing, use the separate `data/` folder (provided for development only, not part of submission):

- **`data/streaming-server/`** - Run this to simulate real-time data streams from sensor inputs
- **`data/streaming-clients/`** - Sample client code in Python, Node.js, and Java
- **`data/input/`** - Sample datasets to work with during development
- **`data/output/`** - Expected output format examples

See `data/README.md` for details on the input data contents, starting the streaming server, and using the sample streaming clients.

**Note:** The `data/` folder is only for development - do not include it in your final submission.

> **Important:** Keep `SUBMISSION_GUIDE.md` in the provided format. Only replace `<ENTER INFO>` placeholders—no new sections, renamed headings, or structural edits.

## Judging criteria

Teams are scored across automated checks and a live, in-person review. Each
criterion is worth 100 marks. After all five scores are recorded, they are
averaged to yield the final 0–100 result.

> **Tie-break rule:** If teams finish with the same total score, judges will review the artefacts in `evidence/` (screenshots and executables) to decide the winner.

**Automated judgement**

1. **Design & Implementation Quality** – design, structure, documentation, tests, and overall code hygiene across `src/`.
2. **Accuracy of the Results** – JSON outputs in `evidence/output/` must match the organiser ground truth.
3. **Algorithms Used** – automation searches for `# @algorithm Name | Purpose` markers and inspects the tagged implementations.

**In-person judgement (2‑minute walk-through. Strictly time boxed)**

4. **Quality of the Dashboard** – judges review the clarity and usefulness of your visualisations.
5. **Solution Presentation** – teams present the system within the timebox and address questions.

## Directory overview

This template contains the following structure:

```
Team##_sentinel/
├── README.md              # this file (submission guidelines)
├── SUBMISSION_GUIDE.md    # fill in before submitting
├── src/                   # your complete source code goes here
├── evidence/
│   ├── screenshots/       # dashboard captures (PNG recommended)
│   ├── output/
│   │   ├── test/                # your events.jsonl for test data
│   │   └── final/               # your events.jsonl for final data
│   └── executables/       # automation script + required binaries
```

**What you need to do:**

1. Add your complete source code to the `src/` folder
2. Run your solution on the test dataset and save the resulting `events.jsonl` to `evidence/output/test/`; run it on the final dataset and save that `events.jsonl` to `evidence/output/final/`
3. Add dashboard screenshots to `evidence/screenshots/`
4. Create your automation script in `evidence/executables/`
5. Fill out `SUBMISSION_GUIDE.md`
6. Zip the entire `Team##_sentinel/` folder and upload it to your team’s assigned Google Drive location

## Algorithm tagging

Any function that implements an algorithm must include a line comment immediately above it in the form:

```
# @algorithm Name | Purpose
```

The automation only recognises this exact prefix; omitting it will force the
"Algorithms" score to 0. If you are working in another language, adapt the
comment syntax but keep the `@algorithm Name | Purpose` text verbatim.

## Evidence expectations

- Place each generated `events.jsonl` in the matching split under `evidence/output/` (`test/` and `final/`) and keep the filenames exactly as provided.
- Keep your executables in `evidence/executables/`, including a single entry point `run_demo.py` that installs dependencies, starts required services, and regenerates the `./output/` tree to mirror `evidence/output/`.
- Note any special prerequisites (network, environment variables, warm-up time) in this README, and remember judges will only execute the single command you document in the SUBMISSION_GUIDE.md—make sure it’s crystal clear and self sufficient.
- Capture system visuals in `evidence/screenshots/` using clear, descriptive PNGs (e.g., `dashboard-overview.png`).

## Packaging checklist

- Replace `Team##` in directory names with your assigned team number.
- Verify `src/` contains the final source tree and comment-tagged algorithms (run `grep -R "@algorithm" src`).
- Regenerate evidence so each `evidence/output/*/events.jsonl` reflects your latest code.
- Confirm the automation script regenerates the outputs end-to-end.
- Fill out `SUBMISSION_GUIDE.md` before zipping your final archive.
- Zip the `Team##_sentinel/` folder directly (no extra nesting) for upload.
