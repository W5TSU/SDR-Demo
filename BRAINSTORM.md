# Brainstorm: More SDR Demo Ideas

The six flowgraphs in `flowgraphs/` cover the core story (spectrum, receive,
wideband record/playback, transmit). Below are additional demo ideas,
roughly ordered by how much extra effort they'd take, for if you want to
extend the talk or do a follow-up session. None of these have flowgraphs
built yet — flagging what each would need.

## Things to do with a wideband capture (no new flowgraph needed)

Once you've recorded the whole 2m band (`flowgraphs/03`+`04`, or
`full-band-demo/`), the file itself is reusable well beyond a single
playback. These came out of `full-band-demo/README.md` and don't require
building anything new:

- **Call-sign replay.** Have everyone in the room set their HT to a
  simplex frequency (146.400-146.580 or 147.400-147.599 MHz), record while
  each person keys up and gives their call, then play the recording back —
  everyone hears every ID replayed exactly as sent. Great group-participation
  closer.
- **Offline demodulation of any signal in the band.** Because the capture
  has everything between 144-148 MHz at once, you can open it after the
  fact in GQRX, SDR++, SDRangel, or a fresh GNU Radio flowgraph and tune to
  *any* frequency in that span — including ones nobody was actively
  listening to at record time.
- **Repeatable receiver testing.** Replay the same file into a receiver
  under test for bit-for-bit identical RF stimulus every time — useful for
  comparing antennas, filters, or firmware builds under identical signal
  conditions, independent of live propagation.
- **Interference documentation.** Record a session with interference
  present, then replay it slowly or freeze on a waterfall frame to
  characterize frequency, bandwidth, duty cycle, and modulation — a replay
  file can accompany an interference report to a frequency coordinator.
- **Propagation event capture.** Sporadic-E, aurora, meteor scatter, and
  tropo openings are brief and unpredictable; recording a wide slice of the
  band during an opening preserves everything that appeared, including
  signals nobody was tuned to at the time.
- **Slow-motion / time-stretched analysis.** GNU Radio can read the file
  back slower than real time (drop `samp_rate` in the playback flowgraph to
  a fraction of the recorded rate), stretching a 5-second event into
  minutes to measure timing relationships or frequency drift invisible in
  real time.
- **Protocol decoding and logging.** Pass the file through Direwolf
  (APRS/AX.25), DSD (DMR/P25), or multimon-ng to extract digital messages
  after the fact — since it doesn't need to run in real time, missed
  packets can be recovered by replaying the same segment. See also the APRS
  and digital-voice entries below for live versions of this.

## Quick wins (an hour or two of flowgraph work, no new dependencies)

- **CTCSS/PL tone squelch decode.** Add a tone decoder (Goertzel or a
  simple `analog.ctcss_squelch` block) onto `02_nbfm_voice_receiver.grc`'s
  audio output and display the detected sub-audible tone. Good teaching
  moment: "this is how a repeater knows to let you in."
- **CW (Morse) ID transmitter.** A short flowgraph using
  `blocks.vector_source` + on/off keying of a CW tone into the NBFM/AM path
  is a much simpler and very Part-97-safe TX demo than voice — good
  fallback if you want *something* on the air but are nervous about a live
  voice demo. Also solves the "automated station ID" idea mentioned in the
  README.
- **RDS decode from the FM broadcast bonus demo.** Extend
  `06_bonus_fm_broadcast_receiver.grc` to pull the station name/RadioText
  out of the 57 kHz RDS subcarrier (needs `gr-rds`, an OOT module — check
  availability before committing to it). Great visual: text appears out of
  "static."
- **Noise-floor / gain teaching moment.** No new flowgraph — just narrate
  while sweeping the LNA/VGA sliders on `01`, pointing out where the noise
  floor rises, where a strong nearby signal (the handheld) starts to
  splatter across the band, and what the DC spike at center frequency is.
  Great for the "how does gain actually work" question that always comes up.

## Medium effort (needs an extra dependency or a bit of new flow design)

- **APRS decode on 144.390 MHz.** Feed the NBFM-demodulated audio from a
  copy of `02` into a software TNC (`direwolf` or `multimon-ng`, neither of
  which is installed in this environment — check before the talk) to print
  decoded APRS packets (callsign, position, comment) live. If anyone local
  is running an APRS-enabled HT or mobile, this can produce a real,
  recognizable packet on the spot.
- **WSPR/FT8 weak-signal decode.** Route NBFM (or a wider SSB-ish) audio
  output into WSJT-X via a virtual audio cable and decode weak-signal
  digital modes. Less flashy live (it's mostly text), but a good "software
  radio isn't just about voice" point, and bridges to HF if you have an
  upconverter.
- **ADS-B aircraft tracking (1090 MHz).** Not a ham band, but a crowd
  favorite and dead simple with a HackRF: `gr-adsb` or just running
  `dump1090` against the HackRF and pulling up a live aircraft map. Great
  "look, it's not just voice, here's real air traffic over the building"
  moment. Needs `gr-adsb`/`dump1090-fa` installed.

## Advanced / stretch goals

- **Cross-band digital repeater.** Receive on 440, retransmit on 144 (or
  vice versa). Doable in software with valve/gate blocks and careful PTT
  timing on a single HackRF (half-duplex, so it can't RX and TX
  simultaneously — you'd gate blocks of audio), but a second cheap SDR
  (RTL-SDR) dedicated to RX while the HackRF handles TX makes this much
  cleaner and demonstrates true full-duplex repeat.
- **TDOA / direction-finding concept demo.** With two SDRs (even two cheap
  RTL-SDRs plus the HackRF) sharing a clock, you can show phase-difference
  direction finding conceptually. This is a bigger build — probably its
  own follow-up talk rather than a slot in this one.
- **Doppler-shifted satellite pass playback.** Capture (or use a
  pre-recorded) LEO satellite pass IQ file and play it back at variable
  speed/frequency to illustrate Doppler shift, tying into how ground
  stations track satellites. More of a concept illustration than a live
  demo unless you have real satellite pass timing to work with.
- **Digital voice decode (DMR/D-STAR/System Fusion).** Needs OP25 or
  `dsd`/`dsdcc` plus mode-specific know-how; solidly a "future work" item
  unless someone on the team already has that pipeline built.

## Notes on scope

- Everything above that transmits is subject to the same Part 97 rules
  called out in `README.md` — control operator present, ID, minimum power.
- Everything that only receives (APRS decode, ADS-B, RDS, WSPR/FT8 decode,
  DMR/D-STAR decode) needs no license to demo.
- If extending this kit, keep new flowgraphs in `flowgraphs/` following the
  same numbering convention and validate with `grcc -o /tmp/out <file>.grc`
  before considering them demo-ready — that catches schema/YAML errors
  without needing the hardware attached.
