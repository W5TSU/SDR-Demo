# Full Band Demo

Mark Grennan  •  W5TSU

## 2M Band IQ Record/Playback Demo

This demonstration records the entire radio 2-meter (144-149) radio spectrum to a "raw" data file.

Think of the radio band as a pond and all the transmissions are rocks throne into it.  Think of the raw data as a video of the pond.  Each frame of the video documents all the waves mixed together.  

The software "[GNU Radio](https://www.gnuradio.org/)" is used to script (flow graphs) the recording and playback of everything between two frequencies using a [HackRF One](https://greatscottgadgets.com/hackrf/one/).  A full 5 MHz of spectrum (raw data) is written to the file /tmp/2m_capture.iq.  

## Requirements

- [GNU Radio](https://www.gnuradio.org/) 3.8+
- [gr-osmosdr](https://osmocom.org/projects/gr-osmosdr) with HackRF support
- HackRF One connected via USB
- Python 3

## Files

| File | Purpose |
|------|---------|
| `2m_record.grc` | GRC flowgraph — receive 144–149 MHz and write raw IQ to file |
| `two_m_record.py` | Python script **generated** from `2m_record.grc` by GNU Radio Companion |
| `2m_playback.grc` | GRC flowgraph — read the IQ file and retransmit on the same band |
| `two_m_playback.py` | Python script **generated** from `2m_playback.grc` by GNU Radio Companion |

## Usage

### Step 1 — Record

Open `2m_record.grc` in GNU Radio Companion and run it, or generate and run the Python script directly:

```bash
gnuradio-companion 2m_record.grc
```

Press **F6** to run the script or **F5** to generate the python program. The flowgraph writes interleaved complex float32 IQ samples to `/tmp/2m_capture.iq`.  

The controls (variables) for the program are in boxes across the top of the graph window.  You shouldn't need to edit these. 

**GUI controls:**

- **Center Frequency** — tune within 144–149 MHz (default 146.5 MHz)
- **LNA Gain** — HackRF IF/LNA gain, 0–40 dB in 8 dB steps (default 32 dB)
- **VGA Gain** — HackRF baseband gain, 0–62 dB in 2 dB steps (default 40 dB)
- **Record Time** — duration in seconds, 1–600 (default 30). Recording stops automatically after this many seconds; the spectrum and waterfall displays continue running so you can keep monitoring the band.

### Step 2 — Play back

Open `2m_playback.grc` and run or generate it like the records program. 

```bash
gnuradio-companion 2m_playback.grc
```

The flowgraph reads the IQ file and drives the HackRF transmitter. When the file is exhausted the flowgraph stops and the window closes automatically.

The Python script can also be run directly with command-line options:

```bash
python3 two_m_playback.py [--in-file FILE] [--center-freq FREQ]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--in-file FILE` | `/tmp/2m_capture.iq` | Path to the IQ file to transmit |
| `--center-freq FREQ` | `146500000` | TX center frequency in Hz; accepts engineering notation (`146.52M`) |

Examples:

```bash
# Play back a recording saved to a non-default path
python3 two_m_playback.py --in-file ~/recordings/contest_run.iq

# Play back and transmit at a different center frequency
python3 two_m_playback.py --in-file ~/recordings/contest_run.iq --center-freq 147.0M
```

`--center-freq` must match the frequency used during recording; a mismatch shifts all signals proportionally across the band.

**GUI controls:**
- **TX VGA Gain** — HackRF TX output level, 0–47 dB in 1 dB steps (default 20 dB; start low)

## Parameters

Both flowgraphs share these fixed settings:

| Parameter | Value | Notes |
|-----------|-------|-------|
| Sample rate | 5 Msps | Covers the full 5 MHz span |
| File path | `/tmp/2m_capture.iq` | Change the `out_file`/`in_file` variable in the flowgraph |
| File format | complex float32 | Interleaved I/Q, native GNU Radio format |

Disk usage: ~40 MB per second of recording at 5 Msps complex float32.

## HackRF Gain Mapping (gr-osmosdr)

| gr-osmosdr parameter | HackRF stage | Range |
|----------------------|-------------|-------|
| `gain` (RF amp) | AMP | 0 or 14 dB |
| `if_gain` | LNA | 0–40 dB, 8 dB steps |
| `bb_gain` | VGA | 0–62 dB, 2 dB steps (RX) |
| `if_gain` | TX VGA | 0–47 dB, 1 dB steps (TX) |

The record flowgraph sets `gain0 = 0` (AMP off). Enable the 14 dB AMP for weak-signal work by editing the `osmosdr_source` block.

## Regulatory Notes

- **Receiving** IQ data requires no license.
- **Transmitting** on 144–148 MHz requires a valid amateur radio license (Technician class or higher in the US). The segment 148–149 MHz is not part of the amateur allocation in the US.
- Retransmitting a recording re-emits the original signals exactly, including any other stations' transmissions that were captured. Ensure you are authorized to transmit before running the playback flowgraph.



## **DEMO**

To demo the recording of the entire 2 meter band, tune a radio to 146.500 Mhz. Run the two-m-records.py program and transmit up to 30 seconds. This should write a file to /tmp/2m_capture.iq.  Now run two-m-playback.py.  You should hear your transmition on your radio.

Because the raw IQ file captures every signal in the band simultaneously, you can playback any transmition that happend during the recording. Just turn you radio to that frequcy and run two-m-playback.py again.

Because a single recording has everything transmitted there are many uses beyond simple playback.

### Call-sign replay

Have everyone set their radio to a simplex frequency in the 146.400–146.580 MHz or 147.400–147.599 MHz range. Run `two_m_record.py` and have each person transmit their call sign. When the recording stops, run `two_m_playback.py` — everyone's radio will hear every ID replayed exactly as transmitted.

### Offline demodulation of any signal in the band

The recording captures all signals between 144 and 149 MHz at once. After the fact you can open the file in [GQRX](https://www.gqrx.dk/), [SDR++](https://www.sdrpp.org/), [SDRangel](https://www.sdrangel.org/), or a new GNU Radio flowgraph and tune to any frequency within that span to demodulate FM repeaters, SSB operators, APRS packets, or digital voice — without needing to have been listening on that frequency at the time.

### Repeatable receiver testing

Replay the file into a receiver under test to get bit-for-bit identical RF stimulus every time. This makes it practical to compare antenna configurations, filter designs, or firmware versions under identical signal conditions, independent of live propagation.

### Interference documentation

Record a session where interference is present, then replay it slowly or freeze on a waterfall frame to characterize the interferer's frequency, bandwidth, duty cycle, and modulation type. A replay file can also accompany an interference report to a frequency coordinator or regulatory body.

### Propagation event capture

Sporadic-E, aurora, meteor scatter, and tropo openings are unpredictable and brief. Recording a wide slice of the band during an opening preserves every signal that appeared — including ones you weren't actively monitoring — for later analysis, logging, or sharing with other operators.

### Slow-motion and time-stretched analysis

GNU Radio can read the file slower than real time, stretching a 5-second event into minutes. This makes it possible to measure timing relationships, symbol rates, and frequency drift that would be invisible in real time. Change `samp_rate` in the playback flowgraph to a fraction of the recorded rate to achieve this.

### Protocol decoding and logging

Pass the file through decoders such as [Direwolf](https://github.com/wb2osz/direwolf) (APRS/AX.25), [DSD](https://github.com/szechyjs/dsd) (DMR/P25), or [multimon-ng](https://github.com/EliasOenal/multimon-ng) to extract digital messages. Because the file can be replayed at any speed, the decoder does not need to run in real time and missed packets can be recovered by replaying the same segment.

### Direction finding

Feed the same IQ file simultaneously into multiple software receivers configured with different antenna phase references — recorded with a multi-channel SDR, or replayed to multiple receivers over a network — to perform time-difference-of-arrival or phase-comparison direction finding entirely offline.



## Script Details

### two_m_record.py

`two_m_record.py` is the Python script GRC generates from `2m_record.grc` (GNU Radio 3.10.10). It can be run directly without opening GRC:

```bash
python3 two_m_record.py
```

The file defines a single class `two_m_record` that inherits from both `gr.top_block` (the GNU Radio scheduler) and `Qt.QWidget` (the GUI window). On startup it:

1. Builds four Qt slider widgets for **Center Frequency**, **LNA Gain**, **VGA Gain**, and **Record Time** and places them in a grid layout.
2. Creates an `osmosdr.source` pointed at `hackrf=0`, sampling at 5 Msps with `if_gain` (LNA) and `bb_gain` (VGA) set from the slider defaults. The RF amplifier is left off (`gain=0`).
3. Creates a `blocks.head` block sized to `int(samp_rate * record_time)` samples. This block passes samples through until the count is reached, then signals end-of-stream to the file sink only.
4. Creates a `blocks.file_sink` writing `gr_complex` (8 bytes/sample, interleaved float32 I/Q) to `/tmp/2m_capture.iq`.
5. Creates a `qtgui.freq_sink_c` (FFT spectrum, 1024 points, Blackman-Harris window, -140 to +10 dB) and a `qtgui.waterfall_sink_c` (scrolling time-frequency display) wired directly from the source, bypassing the head block so they stay live after recording stops.
6. Connections: `osmosdr_source → blocks_head → file_sink`; `osmosdr_source → freq_sink`; `osmosdr_source → waterfall_sink`.

### two_m_playback.py

`two_m_playback.py` is generated from `2m_playback.grc` and can also be run directly:

```bash
python3 two_m_playback.py
```

It defines `two_m_playback`, the same `gr.top_block` / `Qt.QWidget` pattern. On startup it:

1. Builds one Qt slider widget for **TX VGA Gain**. `center_freq` and `in_file`
   are constructor parameters (set via `--center-freq`/`--in-file`, or by
   editing the call in `main()`) rather than GUI sliders — there's no
   Center Frequency slider in this flowgraph.
2. Creates a `blocks.file_source` reading `gr_complex` samples from `/tmp/2m_capture.iq` with `repeat=False` — the source signals end-of-stream when the file is exhausted.
3. Creates an `osmosdr.sink` pointed at `hackrf=0`, configured at 5 Msps with `if_gain` (TX VGA) set from the slider default. The RF amplifier is left off (`gain=0`).
4. Creates a `qtgui.freq_sink_c` fed from the file source so you can monitor the spectrum while it transmits.
5. Connects: `file_source → osmosdr_sink`, `file_source → freq_sink`.
6. Launches a daemon thread (`eof_watcher`) that sleeps for the recording's
   known duration (`num_samples / samp_rate`, plus a 500 ms flush buffer)
   then stops the flowgraph and closes the window. This is a hand-written
   addition, not something GRC generates — `osmosdr.sink` is a hardware
   clock master that keeps the scheduler running indefinitely, so a plain
   `tb.wait()` on end-of-stream never returns on its own. **If you
   regenerate `two_m_playback.py` from `2m_playback.grc`** (GRC's F5/F6, or
   `grcc`), this block is not part of the flowgraph and will be silently
   dropped — re-apply it from the `BEGIN/END CUSTOM PATCH` markers in the
   current file, or diff against git history to recover it.

Each variable in both scripts has a paired `get_`/`set_` method. The `set_tx_gain` callback updates `osmosdr_sink_0.set_if_gain()` live, and `set_center_freq` updates both the hardware and the spectrum display, so neither requires a restart to take effect. As of the `freq0` fix, both scripts also apply `center_freq` to the hardware **on startup**, not just on subsequent slider/setter calls — previously the initial tune was hardcoded to 146.520 MHz regardless of the configured `center_freq`.



## Shared Variables

The two Python scripts share three variables that **must be identical** for a recording to play back correctly. If you change any of them in one script, change it in the other too.

| Variable      | Value                  | Used in record                                               | Used in playback                                             |
| ------------- | ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `samp_rate`   | `5000000`              | Sets the HackRF ADC rate and the file write rate             | Sets the HackRF DAC rate and must match the file's sample rate |
| `center_freq` | `146500000`            | Initial hardware tune point; GUI slider calls `osmosdr_source_0.set_center_freq()` live | Initial hardware tune point, set via `--center-freq` (no GUI slider in this flowgraph); retuning after launch requires calling `set_center_freq()` yourself or editing the script |
| file path     | `"/tmp/2m_capture.iq"` | `out_file` — path passed to `blocks.file_sink`               | `in_file` — path passed to `blocks.file_source`              |

`samp_rate` is the most critical: the file is a raw stream of samples with no header, so the playback script has no way to detect the recorded rate. A mismatch compresses or stretches the signal in time and shifts all frequencies proportionally.

`center_freq` must match so the playback transmitter is tuned to the same band. The slider updates the live hardware via `set_center_freq()` in both scripts, so you can retune after launch.
