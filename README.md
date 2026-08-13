# Software Defined Radio Demo — GNU Radio + HackRF + Ham Handheld

A live demo kit for showing SDR concepts with a HackRF One, GNU Radio Companion,
and a dual-band (144/440 MHz) ham handheld. Built for a ~20-30 minute talk to a
mixed audience (ham club + general tech), but trims down fine for a shorter slot.

## What's in this repo

```
flowgraphs/       7 working GNU Radio Companion (.grc) flowgraphs, GRC 3.10 format
full-band-demo/   Standalone gr-osmosdr implementation of the same wideband
                  2m-band record/playback demo -- its own README, see below
recordings/       Where captured IQ files land (empty until you run Demo 3)
slides/           The talk deck: SDR_Demo.pptx (24 slides), plus build_deck.py
                  that generated it, requirements.txt (python-pptx), and
                  PRESENTER_NOTES.md -- the run-the-talk guide, see below
README.md         This file — setup, legal notes, run order
BRAINSTORM.md     Additional demo ideas beyond the ones built out here
```

**Slides**: `slides/SDR_Demo.pptx` is ready to present as-is, or upload it to
Google Drive and choose "Open with Google Slides" to get a native, fully
editable Slides copy (Drive converts .pptx automatically — no Slides API
access was needed to build it). Title and closing slides are credited to
Mark Grennan, W5TSU. To regenerate after editing `build_deck.py`: `pip
install -r slides/requirements.txt && python3 slides/build_deck.py`.

The slides themselves are audience-facing only — no flowgraph filenames,
stage directions, or "talking points" printed on screen. **Everything
you need to actually run the talk (which flowgraph to launch when, what
to say, timing estimates, and when a slide is safe to skip) is in
`slides/PRESENTER_NOTES.md`** — a slide-by-side table of what's on
screen next to what to do about it.

All seven flowgraphs were validated in this environment with GNU Radio 3.10.12
(`grcc` compiles each one to Python with no errors, and all seven were
smoke-tested against a real HackRF). They use the **Soapy HackRF
Source/Sink** blocks, so they need `gnuradio`, `SoapySDR`, and the
`soapysdr-module-hackrf` driver — not `gr-osmosdr`. See Setup below.

## Hardware needed

- **HackRF One** + antenna (a telescoping whip or a 2m/70cm dual-band antenna
  works well for RX; for TX demos see the antenna/attenuator note below)
- **Dual-band ham handheld** (144/440 MHz), e.g. a Baofeng/Yaesu/Icom HT
- Laptop with a free USB port (USB 3 preferred — wideband capture at 6+ Msps
  benefits from it)
- Optional but recommended for TX demos: a 20-30 dB inline attenuator or SMA
  dummy load, so you can run the HackRF TX and handheld RX close together
  indoors without the handheld's front end overloading

## Software setup

1. **GNU Radio 3.10+** with GNU Radio Companion (`gnuradio-companion`).
2. **SoapySDR + the HackRF module**:
   - Debian/Ubuntu: `sudo apt install soapysdr-module-hackrf hackrf`
   - Verify the module is found: `SoapySDRUtil --info` should list
     `Module found: .../libHackRFSupport.so` and `hackrf` under
     "Available factories".
3. **Plug in the HackRF** and confirm it enumerates:
   ```
   hackrf_info
   SoapySDRUtil --probe="driver=hackrf"
   ```
   If neither finds the device, check USB cabling/hub, and on Linux confirm
   udev rules grant your user access (a fresh `hackrf` package install
   usually handles this; a replug after install is sometimes needed).
4. Open any flowgraph with `gnuradio-companion flowgraphs/<name>.grc`, or
   just double-click it if your file manager associates `.grc` with GRC.

## ⚠️ Legal notes before you transmit (Part 97)

Two of the seven flowgraphs key up the HackRF's transmitter on the ham bands:
**`04_playback_2m_band_from_file.grc`** and
**`05_nbfm_voice_transmitter.grc`**. Before running either:

- A **licensed control operator must be present** at the station the whole
  time it's transmitting, per FCC Part 97 (or your country's equivalent).
- **Identify** with your callsign at the start/end of each transmission and
  at least every 10 minutes during one, same as any other ham transmission.
- No music, no broadcasting to the general public, no obscured/encrypted
  meaning — a rebroadcast of a captured 2m recording should be brief,
  identified, and clearly a test (e.g., "This is a test transmission by
  `<callsign>`, please stand by").
- Keep power **minimum necessary for the demo**. The HackRF's own TX VGA
  gain (0-47 dB) is the control in these flowgraphs — both flowgraphs
  default it to a conservative **10 dB**, well under HackRF's ~10-15 dBm
  max output. Start low, raise only as needed for the handheld to hear it.
- **No control operator available, or want a fully contained indoor demo?**
  Terminate the HackRF's TX port into a 50Ω dummy load / SMA terminator
  instead of an antenna. With nothing radiated over the air, Part 97 doesn't
  come into play — you can still show the waterfall lighting up and, if the
  handheld is placed close enough to pick up the small amount of leakage,
  even hear it. This is the safest option for a venue where you don't want
  any actual on-air emission.
- If you'd rather skip transmitting altogether, the demo still stands on
  its own with receive-only flowgraphs `01`, `02`, `03`, `06`, and `07`
  — a wideband capture of the entire 2m band to a file is itself a solid
  "wow" moment even without the playback half.

## Suggested run order (~20-30 min)

| # | Flowgraph | What it shows |
|---|-----------|----------------|
| 0 (icebreaker) | `06_bonus_fm_broadcast_receiver.grc` | Tune to a local FM station, hear music instantly — proves the whole chain (driver, HackRF, GRC, audio) works before the ham-band material. No license needed, RX only. |
| 1 | `01_spectrum_waterfall_tunable.grc` | Live spectrum + waterfall. Retype the center frequency live: `146.52e6` (2m) then `446.0e6` (70cm) — key up the handheld on each and watch the signal appear. |
| 2 | `02_nbfm_voice_receiver.grc` | Tunable narrowband FM voice receiver. Key up the handheld on 146.520 MHz (national 2m simplex calling frequency) and hear it through the laptop speakers. |
| 3 | `03_record_2m_band_to_file.grc` → `04_playback_2m_band_from_file.grc` | **The headline demo.** Capture the *entire* 144-148 MHz band as raw IQ to a file (run 03, key up the HT once or twice during the recording, stop the flowgraph), then play the file back out through the HackRF (run 04) and hear/see the exact same signal reappear on the air. |
| 4 (optional, needs control operator) | `05_nbfm_voice_transmitter.grc` | Talk into the laptop mic, hear yourself on the handheld — the reverse direction, live two-way. |

**Two implementations of Demo 3**: `flowgraphs/03`+`04` (above) uses
SoapySDR/Soapy HackRF blocks and a self-describing `file_meta_sink`, with
manual start/stop. `full-band-demo/` is a standalone, previously-released
gr-osmosdr implementation of the same idea — fixed-duration auto-recording
(a "Record Time" slider, 1-600s) into a headerless raw file, plus a CLI
(`--in-file`/`--center-freq`) on the playback side. Functionally
equivalent; pick whichever matches the driver stack you have installed
(SoapySDR vs. `gr-osmosdr`), or run both back-to-back as a "two ways to
build the same demo" aside. See `full-band-demo/README.md` for its own
setup/usage — it also has a much longer list of things to do with a
wideband capture once you have one (callsign replay, offline demodulation
of any signal in the band, repeatable receiver testing, interference
documentation, and more), several of which are folded into
`BRAINSTORM.md`.

## Bonus: what does the whole 20m band sound like?

`07_hf_20m_band_wideband_am.grc` is a different kind of demo from the
rest of this kit — HF instead of VHF/UHF, and not tuned to any single
station. It captures the entire 20m amateur band (14.000-14.350 MHz) in
one 1 Msps instantaneous bandwidth and runs a plain AM envelope detector
(`complex_to_mag` → DC blocker, no channel filter at all) directly on
the raw wideband IQ. The result is every CW/SSB/AM/data signal active on
the band at once, mixed into one live audio stream — a cacophony, not a
conversation.

A couple of things worth knowing before you run it:

- **SSB will sound garbled**, not like clean voice. SSB carries no
  carrier, so a plain envelope detector doesn't recover intelligible
  audio from it the way it does from true AM — you'll still hear
  activity (warbling, whistles, beat notes), just not readable speech.
  That's expected, not a bug.
- **Antenna matters a lot more here** than in the VHF/UHF demos. HF
  signals through a simple wire antenna are typically much weaker than
  a handheld held next to the HackRF, which is why this flowgraph
  defaults the RF amp on and starts the Volume slider higher (envelope
  + DC-blocked audio runs quiet).
- **Band conditions matter too** — 20m activity varies a lot by time of
  day and solar conditions. Daytime is usually your best bet.
- Receive only, no license needed — same as the other RX flowgraphs in
  this kit.

Launch it with `full-band-demo/Full-20M-Audio.sh` (works from any
directory) or open `07_hf_20m_band_wideband_am.grc` directly in GRC.
This is also what slide 4 of the talk deck runs live — see
`slides/PRESENTER_NOTES.md`.

## Running a flowgraph

```
gnuradio-companion flowgraphs/01_spectrum_waterfall_tunable.grc
```
Press the green ▶ (Execute) button or `F6` to run. A Qt window opens with the
plots and sliders described above; close it or hit the red ■ (Stop) button to
end.

You can also run a flowgraph directly from the command line without opening
the GRC editor, which GRC generates alongside the `.grc` file the first time
you run it (or via `grcc -o <dir> <file>.grc`):
```
python3 flowgraphs/spectrum_waterfall_tunable.py
```
For live-demo purposes, running from GRC is usually nicer since you can
tweak block parameters between takes without touching Python.

## Demo 3 specifics: recording the whole 2m band

`03_record_2m_band_to_file.grc` tunes the HackRF to **146.0 MHz center** at
**6 Msps**, which covers 143.0-149.0 MHz — the full 144-148 MHz 2m band plus
margin. It's a raw-IQ **file-meta** capture (`blocks.file_meta_sink`), which
means the sample rate and center frequency are written into the file header
automatically, so `04_playback_2m_band_from_file.grc` doesn't need you to
re-enter them (they're still hardcoded to matching values in both flowgraphs
for clarity/robustness — just keep them in sync if you change either one).

**File size**: complex float32 IQ at 6 Msps is `6e6 × 8 bytes ≈ 48 MB/s`,
i.e. roughly **2.9 GB per minute**. For a live demo, record 15-30 seconds
(press Execute, key up the HT once or twice, press Stop) rather than
minutes — that's still a very convincing "I just captured the whole band"
moment without filling the disk. The recording only flushes to disk when
you **stop** the flowgraph, not while it's running.

Default recording path: `recordings/2m_band_capture.iqmeta`. Edit the
`capture_file` / `replay_file` variables at the top of `03`/`04` (in GRC's
variable block, or directly in the `.grc` YAML) if you want it elsewhere.

## Gain tuning tips

- **LNA gain** (0-40 dB, in the HackRF's RF/IF stage) — raise this first if
  signals are weak. Too high with a strong nearby signal (e.g., the
  handheld sitting right next to the HackRF) causes distortion; back it off.
- **VGA gain** (0-62 dB RX / 0-47 dB TX, baseband) — the second knob to
  reach for. On receive, if the waterfall looks like solid noise, you've
  gone too high.
- **Amp** (+11-14 dB front-end amp) is left `False` in every flowgraph.
  Only enable it (edit the block) for genuinely weak/distant signals — with
  a handheld a few feet away you will not need it, and it makes overload
  more likely.
- If the handheld is close to the HackRF during a TX demo (04/05) and the
  handheld's receive audio distorts or squelch won't close, that's likely
  front-end desense — add the inline attenuator or move them apart.

## Troubleshooting

- **"No devices found" / SoapySDR can't see the HackRF** — run `hackrf_info`
  first; if that also fails, it's a USB/driver issue, not a GNU Radio issue.
  Try a different USB port/cable, unplug-replug, check `lsusb` shows the
  HackRF (`1d50:6089`).
- **Choppy audio or "O" (overflow) / "U" (underflow) markers in the
  terminal** — the sample rate is outrunning the USB link or CPU. Try a USB 3
  port, close other apps, or in Demo 3 lower `samp_rate` from 6e6 (though
  that shrinks your band coverage — stay ≥5e6 to keep the full 4 MHz band).
- **Waterfall is flat / all one color** — check the `int_min`/`int_max` (RX)
  or the intensity range on the plot; a strong nearby signal can push
  everything off-scale. Nudge gains down.
- **TX demo: nothing heard on the handheld** — confirm the handheld is on
  the same frequency, mode (narrow FM), and no CTCSS/tone squelch is set
  that the transmission isn't sending; raise `tx_gain` a little; confirm
  you're not into a dummy load if you meant to radiate.

## Callsign / identification note

Every TX-capable flowgraph's `options` block comment includes the Part 97
reminder. Consider adding a `blocks.message_strobe` + Morse/voice ID chain
if you want automated station ID baked into the flowgraph itself — not
included here since manual voice ID between takes is simpler for a live
demo.
