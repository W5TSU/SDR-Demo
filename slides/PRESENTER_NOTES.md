# Presenter's Guide — SDR Demo

Companion to `slides/SDR_Demo.pptx` (24 slides). The slides themselves are
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
- Slide 4's whole-band 20m demo needs an HF-capable antenna, not just
  the 2m/70cm one -- a plain wire works, but the VHF/UHF antenna used
  for the rest of the demos likely won't hear much on 14 MHz. Confirm
  what's connected before the talk, and know it's daytime/propagation
  dependent -- worth a quick dry run beforehand so you know what to
  expect live rather than finding out for the first time on stage.
- If presenting from the laptop with slides live (not just printed
  notes), a live internet connection makes slides 4, 5, 17, and 23's
  links actually clickable/loadable during the talk.

## Rough timing budget

Talking only (no demo hiccups) runs **~14 minutes** end to end — content
slides ~9.5 min, live demos ~4.5 min. That leaves comfortable room inside
a 20-30 minute slot for Q&A, tangents, and re-running something that
didn't work the first time. Don't rush; the deck is not the bottleneck.

This budget is a floor, not a ceiling -- the deck is fine growing well
past a 20-30 minute slot (a longer, more thorough session is an
explicitly acceptable outcome here). The cut-list below exists so any
given *presentation* of this deck can be trimmed to fit whatever slot
is actually available, not so the deck itself has to stay short.

## If you're short on time, cut in this order

1. **Slide 21, Specs at a Glance** — pure reference, skip it live and
   mention it's in the deck for anyone who wants it after.
2. **Slide 20, More Demo Ideas** — point at `BRAINSTORM.md` verbally
   instead of walking the two columns.
3. **Slides 17-18, GNU Radio details / Connecting to Other Radios** —
   valuable bonus depth, but the demo tells the core story without them.
   Cut both together if you need the time back in one move.
4. **Slide 5, Finding a Signal in the Noise** — a nice conceptual bridge,
   but slide 3 alone still sets up the noise-floor payoff in Demo 1.
5. **Slide 10, Demo 0 (FM broadcast icebreaker)** — nice-to-have proof
   the chain works, not load-bearing for the rest of the talk.
6. **Slide 16 (Demo 4, NBFM TX)** — see its row below; this is already
   framed as optional.

Do **not** cut slide 13 (Part 97 ground rules) if you're running any TX
demo — say it every time, not just the first time you present this deck.

## The walkthrough

| # | On the Slide | Presenter Notes |
|---|---|---|
| 1 | Title: "From Bits to Airwaves" | Introduce yourself and your callsign (W5TSU). One line on what's coming: a live HackRF demo, six different "radios" from one box. ~15s. |
| 2 | "The Airwaves: 3 Hz – 3 THz" — ITU band ladder, VHF/UHF highlighted | Gesture along the ladder left to right. Land on "tonight lives here" — VHF/UHF, and name the three slivers (2m, 70cm, FM broadcast). No demo action. ~30-40s. |
| 3 | "Every Signal Arrives Already Mixed With Noise" — nature vs. human-made panels | The meatier of the two opening slides. If tight on time, the meteor-trail line and the HDMI line are the first to cut — the thermal-noise and switching-power-supply points carry the core idea on their own. Land hard on the last line ("watch the noise floor on the very first demo — it's not empty") since it's the setup for slides 10/11. ~50-60s. |
| 4 | "Hear It For Yourself, Live" — RECEIVE ONLY, websdr.org link | **This is a live demo now, not just a slide.** Run `full-band-demo/Full-20M-Audio.sh` (opens `07_hf_20m_band_wideband_am.grc` in GRC) -- hit Execute and let the whole-20m-band audio play for ~20-30s so the "wall of sound" effect lands, then Stop. Mention it's RX only, no license needed. The websdr.org button is the secondary, "explore more on your own later" option -- real and clickable if presenting live with internet, but the star of this slide is now the live HackRF audio, not the external link. ~45-60s including the demo. |
| 5 | "Finding a Signal in the Noise" — narrow-down/SNR/modulation bullets, Wideband Capture→Filter→Demodulate diagram, sigidwiki.com link | Content slide, no action. This previews the Filter/Resample concept that shows up again on slide 9 and slide 19 — worth a quick callback later ("remember the filter-to-channel idea from earlier"). The sigidwiki.com link is a real, practical resource -- point out you can actually open it later and match whatever weird signal someone heard tonight against ~600 cataloged examples. ~35-50s. |
| 6 | "What Is Software Defined Radio?" | Straight content slide, no action. The antenna → ADC/DAC → software diagram is the thing to point at. ~30-35s. |
| 7 | "HackRF One" — Core Specs / TX Capabilities panels | Content slide. For a more technical/ham audience, linger on the TX Capabilities panel (gain stages, power-by-frequency); for a general audience, the Core Specs panel is enough and you can summarize TX capabilities in one sentence. ~35-45s. |
| 8 | "GNU Radio + GNU Radio Companion" — toolchain diagram, GNU Radio project logo | Content slide, no action. ~30-35s. |
| 9 | "Reading a Flowgraph" — Source→Filter→Demod→Sink diagram, a real GRC screenshot | Content slide, no action. This is the concept that pays off across every demo that follows. ~25-30s. |
| 10 | Demo 0 (icebreaker): FM Broadcast Receiver | **Run `06_bonus_fm_broadcast_receiver.grc`.** If 101.1 MHz isn't a strong station near you, nudge the "Station Freq" slider once the window's up. Let it run ~20-25s so music is unmistakable. No license needed, RX only — say so explicitly if anyone looks nervous about the antenna being up. Skippable if pressed for time (see cut list above). |
| 11 | Demo 1: Live Spectrum & Waterfall | **Run `01_spectrum_waterfall_tunable.grc`.** Opens tuned to 146.520 MHz — key up the handheld there first (~10s), then retype the "Center Freq" box to `446.0e6` and hit Enter to jump to 70cm, key up again (~10s). Point out both bands lighting up on the same plot. ~30-40s total including the retune. |
| 12 | Demo 2: Tunable NBFM Voice Receiver | **Run `02_nbfm_voice_receiver.grc`.** Key up the handheld on 146.520 MHz — audio comes through the laptop speakers, not just a waterfall blip this time. ~20-25s. |
| 13 | Part 97 Ground Rules | Audience-facing legal content, read straight from the slide — no demo action here. Sits right before the first demo that transmits (15), so say it before any RF goes out, not after. Say it **every time**, not just once, whenever a TX demo (15 or 16) is on deck. If there's no control operator in the room or you want zero on-air emission, this is where you say so and describe the dummy-load option explicitly. |
| 14 | Demo 3: Record the Entire 2m Band (headline demo, part 1) | **Run `03_record_2m_band_to_file.grc`.** Hit Execute, key up the handheld once or twice during the recording so there's real content, hit Stop after ~20-30s. Mention the file only flushes on Stop. Writes to `recordings/2m_band_capture.iqmeta` — at ~2.9 GB/minute, don't let it run long. |
| 15 | Demo 3b: ...And Play It Back Over the Air (headline demo, part 2) | **Run `04_playback_2m_band_from_file.grc`** immediately after Demo 3 — it reads that same file back. Let it run the same rough duration as the recording. This is the "wow" moment; let it land, don't talk over the handheld picking it up. |
| 16 | Demo 4 (optional): NBFM Voice Transmitter | **Run `05_nbfm_voice_transmitter.grc`.** Talk into the laptop mic, listen for yourself on the handheld (146.520 MHz, same as Demo 2). **Skip this one if there's no control operator in the room** — Demos 0-3 already tell the complete story without it. ~20-25s if you do run it. |
| 17 | "GNU Radio: What It Is, How It's Used" — history/architecture panel plus a "How to learn GNU-Radio Companion" panel with a YouTube playlist link and thumbnail | Content slide, no action. A deeper-dive follow-up to slide 8, now that the audience has seen the tool in action across five demos. The YouTube link is clickable in the actual slide file if you're presenting from the laptop and want to pull it up live; otherwise just mention it's there. ~30-40s. |
| 18 | "Connecting GNU Radio to Other Radios" — Other SDRs / Analog Non-SDR Radios panels | Content slide, no action. Answers the "how would I hook up my own gear" question before anyone has to ask it — RTL-SDR/LimeSDR/PlutoSDR/USRP on one side, audio-interface/CAT-control/direct-RF on the other. ~35-45s. |
| 19 | "Three Kinds of Bandwidth" — SDR (RF) / Interface (USB) / Receive (decoded channel) panels | Content slide, no action. Ties together things already said earlier without naming them: slide 9's "sample rate sets your instantaneous bandwidth," slide 5's filter-to-channel idea, the real `hackrf_info` USB-bus warning from testing this kit, and the Filter/Resample block from the flowgraph diagram. Good slide to slow down on for a more technical audience. ~40-55s. |
| 20 | "More Demo Ideas" | Content slide. Point at `BRAINSTORM.md` for the full writeup rather than reading both columns verbatim if time is short. Also links to `github.com/argilo/sdr-examples`, a ham club tutorial repo with working flowgraphs for several of these modes. ~20-25s, or skip per the cut list. |
| 21 | "Specs at a Glance" | Pure reference table — good Q&A backup, skippable live (see cut list). ~10-15s if you do show it. |
| 22 | "Go Build Something" (resources) | Content slide, closing links. ~20s. |
| 23 | "Learn the DSP, in Python: pysdr.org" — Fourier Transforms → Filters → Digital Modulation → RX & TX in Python roadmap | Content slide, no action. Good closer before Q&A: everything demoed tonight ran through GNU Radio Companion's canvas, this is "if you want to write the DSP yourself instead." Nice callback -- it's the same site cited on slides 3 (noise) and 19 (bandwidth/Nyquist), worth pointing that out explicitly if you have the time. ~30-40s. |
| 24 | "Thank You" / Questions | Open the floor. Offer to demo anything again if someone missed it. |
