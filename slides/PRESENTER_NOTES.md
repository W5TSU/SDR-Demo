# Presenter's Guide — SDR Demo

Companion to `slides/SDR_Demo.pptx` (19 slides). The slides themselves are
audience-facing only now — no flowgraph filenames, no stage directions, no
"talking points" printed on screen. Everything you need to actually *run*
the talk lives here instead, slide by slide, side by side with what the
audience sees.

Full hardware/legal setup is in the top-level `README.md` — this doc
assumes you've already been through that once. Flowgraph filenames below
are relative to `flowgraphs/`.

## Pre-flight, before anyone sits down

- `hackrf_info` and `SoapySDRUtil --probe="driver=hackrf"` both find the
  HackRF (see README's Troubleshooting section if not).
- Antenna connected. Dummy load / attenuator on hand if you're going the
  no-radiation route for any TX demo (see slide 13's ground rules).
- Handheld powered, on 146.520 MHz, narrow FM, no tone, volume up.
- Laptop mic not muted (needed for Demo 4).
- `recordings/` is empty or you don't mind overwriting
  `2m_band_capture.iqmeta`.
- Know your local strong FM broadcast station's frequency for Demo 0 —
  the flowgraph defaults to 101.1 MHz, which may not be it.

## Rough timing budget

Talking only (no demo hiccups) runs **~11 minutes** end to end — content
slides ~6.5 min, live demos ~4.5 min. That leaves comfortable room inside
a 20-30 minute slot for Q&A, tangents, and re-running something that
didn't work the first time. Don't rush; the deck is not the bottleneck.

## If you're short on time, cut in this order

1. **Slide 17, Specs at a Glance** — pure reference, skip it live and
   mention it's in the deck for anyone who wants it after.
2. **Slide 16, More Demo Ideas** — point at `BRAINSTORM.md` verbally
   instead of walking the two columns.
3. **Slide 8, Demo 0 (FM broadcast icebreaker)** — nice-to-have proof the
   chain works, not load-bearing for the rest of the talk.
4. **Slides 14 (Demo 4, NBFM TX)** — see its row below; this is already
   framed as optional.

Do **not** cut slide 13 (Part 97 ground rules) if you're running any TX
demo — say it every time, not just the first time you present this deck.

## The walkthrough

| # | On the Slide | Presenter Notes |
|---|---|---|
| 1 | Title: "From Bits to Airwaves" | Introduce yourself and your callsign (W5TSU). One line on what's coming: a live HackRF demo, six different "radios" from one box. ~15s. |
| 2 | "The Airwaves: 3 Hz – 3 THz" — ITU band ladder, VHF/UHF highlighted | Gesture along the ladder left to right. Land on "tonight lives here" — VHF/UHF, and name the three slivers (2m, 70cm, FM broadcast). No demo action. ~30-40s. |
| 3 | "Every Signal Arrives Already Mixed With Noise" — nature vs. human-made panels | The meatier of the two opening slides. If tight on time, the meteor-trail line and the HDMI line are the first to cut — the thermal-noise and switching-power-supply points carry the core idea on their own. Land hard on the last line ("watch the noise floor on the very first demo — it's not empty") since it's the setup for slide 8/9. ~50-60s. |
| 4 | "What Is Software Defined Radio?" | Straight content slide, no action. The antenna → ADC/DAC → software diagram is the thing to point at. ~30-35s. |
| 5 | "HackRF One" — Core Specs / TX Capabilities panels | Content slide. For a more technical/ham audience, linger on the TX Capabilities panel (gain stages, power-by-frequency); for a general audience, the Core Specs panel is enough and you can summarize TX capabilities in one sentence. ~35-45s. |
| 6 | "GNU Radio + GNU Radio Companion" — toolchain diagram | Content slide, no action. ~30-35s. |
| 7 | "Reading a Flowgraph" — Source→Filter→Demod→Sink diagram | Content slide, no action. This is the concept that pays off across every demo that follows. ~25-30s. |
| 8 | Demo 0 (icebreaker): FM Broadcast Receiver | **Run `06_bonus_fm_broadcast_receiver.grc`.** If 101.1 MHz isn't a strong station near you, nudge the "Station Freq" slider once the window's up. Let it run ~20-25s so music is unmistakable. No license needed, RX only — say so explicitly if anyone looks nervous about the antenna being up. Skippable if pressed for time (see cut list above). |
| 9 | Demo 1: Live Spectrum & Waterfall | **Run `01_spectrum_waterfall_tunable.grc`.** Opens tuned to 146.520 MHz — key up the handheld there first (~10s), then retype the "Center Freq" box to `446.0e6` and hit Enter to jump to 70cm, key up again (~10s). Point out both bands lighting up on the same plot. ~30-40s total including the retune. |
| 10 | Demo 2: Tunable NBFM Voice Receiver | **Run `02_nbfm_voice_receiver.grc`.** Key up the handheld on 146.520 MHz — audio comes through the laptop speakers, not just a waterfall blip this time. ~20-25s. |
| 11 | Demo 3: Record the Entire 2m Band (headline demo, part 1) | **Run `03_record_2m_band_to_file.grc`.** Hit Execute, key up the handheld once or twice during the recording so there's real content, hit Stop after ~20-30s. Mention the file only flushes on Stop. Writes to `recordings/2m_band_capture.iqmeta` — at ~2.9 GB/minute, don't let it run long. |
| 12 | Demo 3b: ...And Play It Back Over the Air (headline demo, part 2) | **Run `04_playback_2m_band_from_file.grc`** immediately after Demo 3 — it reads that same file back. Let it run the same rough duration as the recording. This is the "wow" moment; let it land, don't talk over the handheld picking it up. |
| 13 | Part 97 Ground Rules | Audience-facing legal content, read straight from the slide — no demo action here. Say this **every time**, not just once, whenever a TX demo (12 or 14) is on deck. If there's no control operator in the room or you want zero on-air emission, this is where you say so and describe the dummy-load option explicitly. |
| 14 | Demo 4 (optional): NBFM Voice Transmitter | **Run `05_nbfm_voice_transmitter.grc`.** Talk into the laptop mic, listen for yourself on the handheld (146.520 MHz, same as Demo 2). **Skip this one if there's no control operator in the room** — Demos 0-3 already tell the complete story without it. ~20-25s if you do run it. |
| 15 | "What Just Happened, Technically" (recap) | Content slide, no action. This is where you tie the whole run back to "same hardware, different software." ~25-30s. |
| 16 | "More Demo Ideas" | Content slide. Point at `BRAINSTORM.md` for the full writeup rather than reading both columns verbatim if time is short. ~20-25s, or skip per the cut list. |
| 17 | "Specs at a Glance" | Pure reference table — good Q&A backup, skippable live (see cut list). ~10-15s if you do show it. |
| 18 | "Go Build Something" (resources) | Content slide, closing links. ~20s. |
| 19 | "Thank You" / Questions | Open the floor. Offer to demo anything again if someone missed it. |
