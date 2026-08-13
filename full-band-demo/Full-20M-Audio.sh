#!/bin/bash
# Launches the whole-band 20m AM envelope receiver demo.
# Safe to run from anywhere -- resolves the repo root relative to this
# script's own location rather than assuming the caller's cwd.
set -e
cd "$(dirname "$0")/.."
gnuradio-companion flowgraphs/07_hf_20m_band_wideband_am.grc
