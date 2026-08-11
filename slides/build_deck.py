#!/usr/bin/env python3
"""
Builds SDR_Demo.pptx -- a Google-Slides-ready deck (upload to Drive, "Open with
Google Slides" and it converts to a native, editable Slides file).

Run:  .venv/bin/python3 build_deck.py
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import copy

# ---------------------------------------------------------------- palette --
BG = RGBColor(0x0A, 0x19, 0x29)  # deep navy, "waterfall" background
BG_ALT = RGBColor(0x0F, 0x24, 0x38)  # slightly lighter navy for panels
INK = RGBColor(0xFF, 0xFF, 0xFF)
BODY = RGBColor(0xD7, 0xE3, 0xEC)
MUTED = RGBColor(0x8E, 0xA7, 0xBA)
TEAL = RGBColor(0x35, 0xD0, 0xBA)   # accent -- waterfall highlight
TEAL_DIM = RGBColor(0x1B, 0x5E, 0x58)
AMBER = RGBColor(0xFF, 0xB0, 0x20)  # legal / caution accent
AMBER_DIM = RGBColor(0x4A, 0x36, 0x12)

FONT = "Calibri"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H
BLANK = prs.slide_layouts[6]


# ------------------------------------------------------------ primitives --
def new_slide(bg=BG):
    s = prs.slides.add_slide(BLANK)
    rect = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    rect.fill.solid()
    rect.fill.fore_color.rgb = bg
    rect.line.fill.background()
    rect.shadow.inherit = False
    # push background behind everything else added later
    s.shapes._spTree.remove(rect._element)
    s.shapes._spTree.insert(2, rect._element)
    return s


def add_text(slide, x, y, w, h, text, size=18, color=BODY, bold=False,
             italic=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             font=FONT, line_spacing=1.15, wrap=True):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
        r.font.name = font
    return tb


def add_bullets(slide, x, y, w, h, items, size=18, color=BODY, bullet_color=TEAL,
                 gap=10, bold_lead=None):
    """items: list of str, or (str, sub_items) for one level of nesting."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    first = True
    for item in items:
        sub = None
        if isinstance(item, tuple):
            item, sub = item
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(gap)
        p.line_spacing = 1.12
        r = p.add_run()
        r.text = f"•  {item}"
        r.font.size = Pt(size)
        r.font.color.rgb = color
        r.font.name = FONT
        if sub:
            for s_item in sub:
                sp = tf.add_paragraph()
                sp.space_after = Pt(6)
                sp.level = 1
                sr = sp.add_run()
                sr.text = f"–  {s_item}"
                sr.font.size = Pt(size - 3)
                sr.font.color.rgb = MUTED
                sr.font.name = FONT
    return tb


def accent_bar(slide, y=Inches(1.5), color=TEAL, x=Inches(0.7), w=Inches(1.1)):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Pt(4))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    bar.shadow.inherit = False
    return bar


def kicker_title(slide, kicker, title, kicker_color=TEAL, title_size=32):
    add_text(slide, Inches(0.7), Inches(0.5), Inches(11.9), Inches(0.4),
              kicker.upper(), size=14, color=kicker_color, bold=True)
    add_text(slide, Inches(0.7), Inches(0.86), Inches(11.9), Inches(0.9),
              title, size=title_size, color=INK, bold=True)
    accent_bar(slide, y=Inches(1.62))


def page_number(slide, n, total):
    add_text(slide, Inches(12.35), Inches(7.08), Inches(0.8), Inches(0.3),
              f"{n} / {total}", size=10, color=MUTED, align=PP_ALIGN.RIGHT)


def footer(slide, text="SDR Demo -- GNU Radio + HackRF + Ham Handheld"):
    add_text(slide, Inches(0.7), Inches(7.08), Inches(8), Inches(0.3),
              text, size=10, color=MUTED)


def pill(slide, x, y, w, h, text, fill=TEAL_DIM, text_color=TEAL, size=13):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shp.adjustments[0] = 0.5
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    shp.line.fill.background()
    shp.shadow.inherit = False
    tf = shp.text_frame
    tf.margin_left = Pt(4)
    tf.margin_right = Pt(4)
    tf.margin_top = Pt(0)
    tf.margin_bottom = Pt(0)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.color.rgb = text_color
    r.font.name = FONT
    return shp


TOTAL_SLIDES = 19
_n = [0]


def count():
    _n[0] += 1
    return _n[0]


# ============================================================== SLIDE 1 ==
s = new_slide()
add_text(s, Inches(0.9), Inches(2.5), Inches(11.5), Inches(0.5),
          "SOFTWARE DEFINED RADIO", size=18, color=TEAL, bold=True)
add_text(s, Inches(0.9), Inches(2.95), Inches(11.5), Inches(1.6),
          "From Bits to Airwaves", size=48, color=INK, bold=True)
add_text(s, Inches(0.9), Inches(4.05), Inches(11.0), Inches(0.6),
          "A live demo with GNU Radio Companion, a HackRF One, and a 144/440 MHz handheld",
          size=20, color=BODY)
accent_bar(s, y=Inches(4.75), x=Inches(0.92), w=Inches(1.4))
add_text(s, Inches(0.9), Inches(6.6), Inches(8), Inches(0.4),
          "Mark Grennan  •  W5TSU  •  " + "2026",
          size=14, color=MUTED)

# ============================================================== SLIDE 1B ==
s = new_slide()
kicker_title(s, "Before We Touch The Radio", "The Airwaves: 3 Hz – 3 THz")
add_text(s, Inches(0.7), Inches(1.95), Inches(11.9), Inches(0.75),
          "By international convention (ITU), everything humans use for wireless "
          "communication -- from submarine navigation to satellite links -- lives "
          "somewhere in this range. Twelve decades, back to back, and every one of "
          "them is already spoken for.",
          size=18, color=BODY)
# band ladder: 12 ITU-designated decades, ELF (3 Hz) through THF (3 THz)
bands = ["ELF", "SLF", "ULF", "VLF", "LF", "MF", "HF", "VHF", "UHF", "SHF", "EHF", "THF"]
highlight = {"VHF", "UHF"}
ladder_y = Inches(3.05)
chip_w = Inches(0.90)
gap = Inches(0.10)
total_w = chip_w * len(bands) + gap * (len(bands) - 1)
lx = (SLIDE_W - total_w) / 2
for band in bands:
    is_hi = band in highlight
    chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, lx, ladder_y, chip_w, Inches(0.95))
    chip.adjustments[0] = 0.15
    chip.fill.solid()
    chip.fill.fore_color.rgb = TEAL if is_hi else BG_ALT
    chip.line.color.rgb = TEAL
    chip.line.width = Pt(1.5 if is_hi else 0.75)
    chip.shadow.inherit = False
    tf = chip.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = band
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = BG if is_hi else INK
    r.font.name = FONT
    lx += chip_w + gap
add_text(s, Inches(0.7), Inches(4.15), Inches(2.5), Inches(0.35),
          "3 Hz", size=13, color=MUTED, bold=True)
add_text(s, Inches(10.13), Inches(4.15), Inches(2.5), Inches(0.35),
          "3 THz", size=13, color=MUTED, bold=True, align=PP_ALIGN.RIGHT)
add_text(s, Inches(0.7), Inches(4.75), Inches(11.9), Inches(0.35),
          "Each band spans one decade -- band N runs 0.3×10ᴺ Hz to 3×10ᴺ Hz.",
          size=14, color=MUTED, italic=True, align=PP_ALIGN.CENTER)
pill(s, Inches(3.9), Inches(5.35), Inches(5.5), Inches(0.45),
     "Tonight lives here: VHF / UHF", fill=TEAL_DIM, text_color=TEAL, size=15)
add_bullets(s, Inches(1.6), Inches(6.0), Inches(10.1), Inches(1.0), [
    "2m (144-148 MHz) and 70cm (420-450 MHz) -- our ham bands -- plus FM "
    "broadcast (88-108 MHz), all three narrow slivers of one 270:1 span (30 "
    "MHz-3 GHz).",
], size=16, gap=0)
add_text(s, Inches(0.7), Inches(7.08), Inches(9), Inches(0.3),
          "ITU Radio Regulations, Article 2 -- band designations ELF-THF",
          size=10, color=MUTED, italic=True)
page_number(s, count(), TOTAL_SLIDES)

# ============================================================== SLIDE 1C ==
s = new_slide()
kicker_title(s, "Before We Touch The Radio",
             "Every Signal Arrives Already Mixed With Noise")
p1x = Inches(0.7); pw = Inches(5.7)
panel1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, p1x, Inches(2.0), pw, Inches(4.15))
panel1.adjustments[0] = 0.04
panel1.fill.solid(); panel1.fill.fore_color.rgb = BG_ALT
panel1.line.color.rgb = TEAL_DIM; panel1.line.width = Pt(1)
panel1.shadow.inherit = False
add_text(s, p1x + Inches(0.35), Inches(2.25), pw - Inches(0.7), Inches(0.4),
          "Noise From Nature", size=19, color=TEAL, bold=True)
add_bullets(s, p1x + Inches(0.35), Inches(2.75), pw - Inches(0.7), Inches(3.3), [
    "Thermal noise: the atoms in your receiver's own components are "
    "vibrating with heat -- that's noise, before an antenna is even "
    "involved.",
    "Modeled as Gaussian / \"white\" noise -- flat across the whole band. "
    "That's the hiss you hear with nothing tuned in.",
    "Lightning sferics: crackly pops from distant thunderstorms, audible "
    "from VLF up through HF.",
    "Ionized meteor trails briefly reflect distant signals into a "
    "receiver -- noise and signal from the same natural event.",
], size=15, gap=10)

p2x = Inches(6.9)
panel2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, p2x, Inches(2.0), pw, Inches(4.15))
panel2.adjustments[0] = 0.04
panel2.fill.solid(); panel2.fill.fore_color.rgb = BG_ALT
panel2.line.color.rgb = TEAL_DIM; panel2.line.width = Pt(1)
panel2.shadow.inherit = False
add_text(s, p2x + Inches(0.35), Inches(2.25), pw - Inches(0.7), Inches(0.4),
          "Noise We Make Ourselves", size=19, color=TEAL, bold=True)
add_bullets(s, p2x + Inches(0.35), Inches(2.75), pw - Inches(0.7), Inches(3.3), [
    "Every switching power supply, phone charger, and LED driver in this "
    "room is radiating RF -- one of the most common interference sources "
    "hams fight.",
    "USB 3.0 leaks clock noise at multiples of 480 MHz; HDMI cables can "
    "splatter interference across roughly 148-742 MHz.",
    "Monitors, DisplayPort, powerline networking adapters -- all of it "
    "adds more.",
    "None of it is malicious. It's just what happens when fast digital "
    "clocks run next to a receiver.",
], size=15, gap=10)
add_text(s, Inches(0.7), Inches(6.35), Inches(11.9), Inches(0.65),
          "Every demo tonight starts here: find the signal you want inside "
          "everything else that's already there. Watch the noise floor on the "
          "very first demo -- it's not empty.",
          size=16, color=TEAL, italic=True)
add_text(s, Inches(0.7), Inches(7.08), Inches(11), Inches(0.3),
          "Sources: pysdr.org (Ch. 10, Noise and Random Variables) and "
          "sigidwiki.com (Interfering Emissions category)",
          size=10, color=MUTED, italic=True)
page_number(s, count(), TOTAL_SLIDES)

# ============================================================== SLIDE 4 ==
s = new_slide()
kicker_title(s, "The Idea", "What Is Software Defined Radio?")
add_bullets(s, Inches(0.7), Inches(2.1), Inches(6.9), Inches(4.5), [
    "Traditional radios: filtering, mixing, and demodulation are done by "
    "dedicated analog/digital hardware built for one job.",
    "SDR: an antenna feeds a wideband ADC/DAC, and everything after that -- "
    "tuning, filtering, demodulating, decoding -- happens in software.",
    "Same box, endless radios: change the software, not the hardware.",
    "Today's demo does this literally -- one HackRF, six different "
    "“radios,” just by loading a different flowgraph.",
], size=19, gap=16)
# simple diagram: Antenna -> ADC/DAC -> Software
panel_y = Inches(2.1)
dx = Inches(7.9)
dw = Inches(4.7)
box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, dx, panel_y, dw, Inches(4.3))
box.adjustments[0] = 0.04
box.fill.solid(); box.fill.fore_color.rgb = BG_ALT
box.line.color.rgb = TEAL_DIM; box.line.width = Pt(1)
box.shadow.inherit = False
labels = ["Antenna", "ADC / DAC\n(HackRF)", "Software\n(GNU Radio)"]
sub = ["Analog RF in/out", "Samples ↔ RF", "Filter · demod · decode"]
by = panel_y + Inches(0.35)
for lab, sb in zip(labels, sub):
    chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, dx + Inches(0.5), by, dw - Inches(1.0), Inches(0.95))
    chip.adjustments[0] = 0.12
    chip.fill.solid(); chip.fill.fore_color.rgb = TEAL_DIM
    chip.line.fill.background()
    chip.shadow.inherit = False
    tf = chip.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Pt(8); tf.margin_right = Pt(8)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = lab
    r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = INK; r.font.name = FONT
    p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run(); r2.text = sb
    r2.font.size = Pt(11); r2.font.color.rgb = MUTED; r2.font.name = FONT
    if lab != labels[-1]:
        arrow = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, dx + dw/2 - Inches(0.15), by + Inches(0.95), Inches(0.3), Inches(0.25))
        arrow.fill.solid(); arrow.fill.fore_color.rgb = TEAL
        arrow.line.fill.background()
        arrow.shadow.inherit = False
    by += Inches(1.2)
footer(s); page_number(s, count(), TOTAL_SLIDES)

# ============================================================== SLIDE 5 ==
s = new_slide()
kicker_title(s, "The Hardware", "HackRF One")
# two panel layout: core specs vs. TX capabilities
p1x = Inches(0.7); pw = Inches(5.7)
panel1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, p1x, Inches(2.1), pw, Inches(4.5))
panel1.adjustments[0] = 0.04
panel1.fill.solid(); panel1.fill.fore_color.rgb = BG_ALT
panel1.line.color.rgb = TEAL_DIM; panel1.line.width = Pt(1)
panel1.shadow.inherit = False
add_text(s, p1x + Inches(0.35), Inches(2.35), pw - Inches(0.7), Inches(0.4),
          "Core Specs", size=20, color=TEAL, bold=True)
add_bullets(s, p1x + Inches(0.35), Inches(2.85), pw - Inches(0.7), Inches(3.5), [
    "1 MHz – 6 GHz tuning range",
    "Up to 20 Msps, 8-bit quadrature ADC/DAC (8-bit I, 8-bit Q)",
    "Half-duplex (RX or TX, never both at once)",
    "Hi-Speed USB 2.0, USB-powered, open source hardware",
    "This talk: driven via SoapySDR from GNU Radio",
], size=16, gap=12)

p2x = Inches(6.9)
panel2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, p2x, Inches(2.1), pw, Inches(4.5))
panel2.adjustments[0] = 0.04
panel2.fill.solid(); panel2.fill.fore_color.rgb = BG_ALT
panel2.line.color.rgb = TEAL_DIM; panel2.line.width = Pt(1)
panel2.shadow.inherit = False
add_text(s, p2x + Inches(0.35), Inches(2.35), pw - Inches(0.7), Inches(0.4),
          "TX Capabilities", size=20, color=TEAL, bold=True)
add_bullets(s, p2x + Inches(0.35), Inches(2.85), pw - Inches(0.7), Inches(3.5), [
    "Two software-controlled TX gain stages -- no physical knobs: an "
    "on/off RF amp (~+11 dB) and a VGA/IF gain stage, 0-47 dB in 1 dB "
    "steps.",
    "Max output power varies with frequency -- roughly +5 to +15 dBm "
    "from 1 MHz-2.17 GHz, dropping to about 0-10 dBm up through 4 GHz. "
    "Best performance is actually 2170-2740 MHz.",
    "Tonight's TX demos default to just 10 dB of VGA gain -- comfortably "
    "at the low end, per the \"minimum power necessary\" guidance.",
    "No built-in per-band TX filtering -- it's a general-purpose "
    "transmitter, so staying inside our allocated ham segments is on us.",
], size=15, gap=10)
add_text(s, Inches(0.7), Inches(7.08), Inches(9), Inches(0.3),
          "Sources: hackrf.readthedocs.io, greatscottgadgets.com/hackrf/one",
          size=10, color=MUTED, italic=True)
page_number(s, count(), TOTAL_SLIDES)

# ============================================================== SLIDE 6 ==
s = new_slide()
kicker_title(s, "The Software", "GNU Radio + GNU Radio Companion")
add_bullets(s, Inches(0.7), Inches(2.1), Inches(6.7), Inches(4.5), [
    "GNU Radio: open-source DSP toolkit -- filters, modulators, "
    "demodulators, resamplers, all as reusable building blocks.",
    "GNU Radio Companion (GRC): drag-and-drop flowgraph editor that "
    "generates the underlying Python for you.",
    "SoapySDR: hardware abstraction layer -- the same flowgraph blocks "
    "work whether it's a HackRF, RTL-SDR, LimeSDR, or others.",
    "Every flowgraph in this demo is a plain-text .grc file -- versionable, "
    "diffable, shareable.",
], size=18, gap=16)
img_x = Inches(7.9); img_w = Inches(4.7)
panel = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, img_x, Inches(2.1), img_w, Inches(4.3))
panel.adjustments[0] = 0.04
panel.fill.solid(); panel.fill.fore_color.rgb = BG_ALT
panel.line.color.rgb = TEAL_DIM; panel.line.width = Pt(1)
panel.shadow.inherit = False
add_text(s, img_x + Inches(0.35), Inches(2.35), img_w - Inches(0.7), Inches(0.35),
          "Toolchain", size=15, color=MUTED, bold=True)
chain = ["Flowgraph (.grc)", "GNU Radio Companion", "Generated Python", "GNU Radio runtime + SoapySDR", "HackRF One"]
cy = Inches(2.85)
for i, item in enumerate(chain):
    chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, img_x + Inches(0.35), cy, img_w - Inches(0.7), Inches(0.62))
    chip.adjustments[0] = 0.2
    chip.fill.solid(); chip.fill.fore_color.rgb = TEAL_DIM
    chip.line.fill.background()
    chip.shadow.inherit = False
    tf = chip.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Pt(10)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = item
    r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = INK; r.font.name = FONT
    if i < len(chain) - 1:
        arrow = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, img_x + img_w/2 - Inches(0.12), cy + Inches(0.62), Inches(0.24), Inches(0.16))
        arrow.fill.solid(); arrow.fill.fore_color.rgb = TEAL
        arrow.line.fill.background(); arrow.shadow.inherit = False
    cy += Inches(0.78)
footer(s); page_number(s, count(), TOTAL_SLIDES)

# ============================================================== SLIDE 7 ==
s = new_slide()
kicker_title(s, "Core Concept", "Reading a Flowgraph")
add_bullets(s, Inches(0.7), Inches(2.1), Inches(11.7), Inches(2.0), [
    "Blocks are connected left to right: a Source produces samples, "
    "middle blocks process them, a Sink consumes them.",
    "Everything on the RF side flows as complex IQ samples -- one number "
    "for signal strength/phase in two dimensions (I and Q), captured at "
    "the sample rate.",
    "Sample rate sets your instantaneous bandwidth: capture at 6 Msps and "
    "you're watching 6 MHz of spectrum at once, not just one channel.",
], size=18, gap=14)
# mini diagram: Source -> Filter -> Demod -> Sink
dy = Inches(4.6)
items = ["HackRF\nSource", "Filter /\nResample", "Demodulate", "Audio / File\nSink"]
bw = Inches(2.55); gap_w = Inches(0.55)
total_w = bw * len(items) + gap_w * (len(items) - 1)
start_x = (SLIDE_W - total_w) / 2
bx = start_x
for i, item in enumerate(items):
    chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, dy, bw, Inches(1.1))
    chip.adjustments[0] = 0.12
    chip.fill.solid()
    chip.fill.fore_color.rgb = TEAL_DIM if i in (0, 3) else BG_ALT
    chip.line.color.rgb = TEAL
    chip.line.width = Pt(1.25)
    chip.shadow.inherit = False
    tf = chip.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = item
    r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = INK; r.font.name = FONT
    if i < len(items) - 1:
        arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, bx + bw, dy + Inches(0.38), gap_w, Inches(0.34))
        arrow.fill.solid(); arrow.fill.fore_color.rgb = TEAL
        arrow.line.fill.background(); arrow.shadow.inherit = False
    bx += bw + gap_w
footer(s); page_number(s, count(), TOTAL_SLIDES)

# ============================================================== SLIDE 8 ==
s = new_slide()
kicker_title(s, "Demo 0  ·  Icebreaker", "FM Broadcast Receiver", kicker_color=MUTED)
pill(s, Inches(0.7), Inches(1.85), Inches(1.5), Inches(0.35), "RECEIVE ONLY", fill=TEAL_DIM, text_color=TEAL, size=12)
add_bullets(s, Inches(0.7), Inches(2.5), Inches(11.7), Inches(3.6), [
    "Flowgraph: 06_bonus_fm_broadcast_receiver.grc",
    "Tune to any strong local FM station (88-108 MHz) and hear music "
    "instantly through the laptop speakers.",
    "Not a ham-band demo -- it's here to prove the whole chain works "
    "(driver, HackRF, GNU Radio, audio out) before the ham material, and "
    "it needs no license to receive.",
], size=19, gap=16)
footer(s); page_number(s, count(), TOTAL_SLIDES)

# ============================================================== SLIDE 9 ==
s = new_slide()
kicker_title(s, "Demo 1", "Live Spectrum & Waterfall", kicker_color=TEAL)
pill(s, Inches(0.7), Inches(1.85), Inches(1.5), Inches(0.35), "RECEIVE ONLY", fill=TEAL_DIM, text_color=TEAL, size=12)
add_bullets(s, Inches(0.7), Inches(2.5), Inches(11.7), Inches(3.8), [
    "Flowgraph: 01_spectrum_waterfall_tunable.grc",
    "One flowgraph, both ham bands -- retype the center frequency live: "
    "146.520 MHz (2m) then 446.000 MHz (70cm).",
    "Key up the handheld on each band and watch the signal light up the "
    "spectrum plot and waterfall in real time.",
    "Talking point: this is the same 10 MHz of RF spectrum a traditional "
    "radio can only look at one narrow slice of at a time.",
], size=19, gap=16)
footer(s); page_number(s, count(), TOTAL_SLIDES)

# ============================================================== SLIDE 10 ==
s = new_slide()
kicker_title(s, "Demo 2", "Tunable NBFM Voice Receiver", kicker_color=TEAL)
pill(s, Inches(0.7), Inches(1.85), Inches(1.5), Inches(0.35), "RECEIVE ONLY", fill=TEAL_DIM, text_color=TEAL, size=12)
add_bullets(s, Inches(0.7), Inches(2.5), Inches(11.7), Inches(3.8), [
    "Flowgraph: 02_nbfm_voice_receiver.grc",
    "A real narrowband FM voice receiver -- channel filter, resampler, "
    "FM demodulator, straight to the speakers.",
    "Default: 146.520 MHz, the national 2m simplex calling frequency. Key "
    "up the handheld there and it comes through the laptop.",
    "Talking point: this whole receiver -- the part that's a dedicated "
    "chip in a normal radio -- is about a dozen blocks of software here.",
], size=19, gap=16)
footer(s); page_number(s, count(), TOTAL_SLIDES)

# ============================================================= SLIDE 11 ==
s = new_slide()
add_text(s, Inches(0.7), Inches(0.5), Inches(11.9), Inches(0.4),
          "DEMO 3 · THE HEADLINE DEMO".upper(), size=14, color=AMBER, bold=True)
add_text(s, Inches(0.7), Inches(0.86), Inches(11.9), Inches(1.0),
          "Record the Entire 2m Band", size=34, color=INK, bold=True)
accent_bar(s, y=Inches(1.7), color=AMBER)
add_bullets(s, Inches(0.7), Inches(2.1), Inches(11.7), Inches(4.5), [
    "Flowgraph: 03_record_2m_band_to_file.grc",
    "Tunes to 146.0 MHz center at 6 Msps -- covers 143.0 to 149.0 MHz, the "
    "whole 144-148 MHz 2m band with margin to spare.",
    ("Not one channel -- every signal on the entire band, captured at once",
     ["Raw IQ, written to a self-describing file (sample rate + center "
      "frequency saved in the header)"]),
    "Live: hit Execute, key up the handheld once or twice, hit Stop. "
    "~2.9 GB/minute -- a 20-30 second capture is plenty for the demo.",
], size=19, gap=16)
footer(s); page_number(s, count(), TOTAL_SLIDES)

# ============================================================= SLIDE 12 ==
s = new_slide()
add_text(s, Inches(0.7), Inches(0.5), Inches(11.9), Inches(0.4),
          "DEMO 3B · THE PAYOFF".upper(), size=14, color=AMBER, bold=True)
add_text(s, Inches(0.7), Inches(0.86), Inches(11.9), Inches(1.0),
          "...And Play It Back Over the Air", size=34, color=INK, bold=True)
accent_bar(s, y=Inches(1.7), color=AMBER)
pill(s, Inches(0.7), Inches(1.9), Inches(2.3), Inches(0.4), "TRANSMITS — SEE NEXT SLIDE",
     fill=AMBER_DIM, text_color=AMBER, size=12)
add_bullets(s, Inches(0.7), Inches(2.55), Inches(11.7), Inches(4.0), [
    "Flowgraph: 04_playback_2m_band_from_file.grc",
    "Reads the file back and feeds it straight into the HackRF's "
    "transmitter -- the exact recorded band reappears on the air.",
    "Watch the waterfall reproduce exactly what was captured; the "
    "handheld hears the same signal a second time, live.",
    "This is the moment that makes SDR click: the recording *is* the "
    "radio signal -- numbers on disk, transmitted back as RF.",
], size=19, gap=16)
footer(s); page_number(s, count(), TOTAL_SLIDES)

# ============================================================= SLIDE 13 ==
s = new_slide(bg=RGBColor(0x1A, 0x14, 0x06))
add_text(s, Inches(0.7), Inches(0.55), Inches(11.9), Inches(0.4),
          "⚠  BEFORE WE TRANSMIT", size=16, color=AMBER, bold=True)
add_text(s, Inches(0.7), Inches(1.0), Inches(11.9), Inches(0.9),
          "Part 97 Ground Rules", size=34, color=INK, bold=True)
accent_bar(s, y=Inches(1.85), color=AMBER)
add_bullets(s, Inches(0.7), Inches(2.25), Inches(11.7), Inches(4.5), [
    "A licensed control operator is present the entire time we transmit.",
    "We identify with callsign at the start/end and every 10 minutes.",
    "No music, no broadcast content -- a brief, identified test "
    "transmission only.",
    "Power stays at the minimum needed -- TX gain starts low and only "
    "comes up as far as the demo needs.",
    "No control operator today, or want zero on-air emission? The HackRF "
    "TX port can go into a dummy load instead of an antenna -- same demo, "
    "nothing radiated.",
], size=18, color=RGBColor(0xF3, 0xE3, 0xC7), gap=14)
footer(s); page_number(s, count(), TOTAL_SLIDES)

# ============================================================= SLIDE 14 ==
s = new_slide()
kicker_title(s, "Demo 4  ·  Optional", "NBFM Voice Transmitter", kicker_color=AMBER)
pill(s, Inches(0.7), Inches(1.85), Inches(2.5), Inches(0.35), "TRANSMITS — CONTROL OP REQUIRED", fill=AMBER_DIM, text_color=AMBER, size=12)
add_bullets(s, Inches(0.7), Inches(2.5), Inches(11.7), Inches(3.8), [
    "Flowgraph: 05_nbfm_voice_transmitter.grc",
    "The reverse direction: laptop microphone → NBFM modulator → HackRF "
    "→ antenna.",
    "Talk into the laptop, hear yourself on the handheld -- live two-way, "
    "same 146.520 MHz simplex frequency as Demo 2.",
    "Skip this one if there's no control operator in the room -- Demos "
    "0-3 already tell the full story.",
], size=19, gap=16)
footer(s); page_number(s, count(), TOTAL_SLIDES)

# ============================================================= SLIDE 15 ==
s = new_slide()
kicker_title(s, "Recap", "What Just Happened, Technically")
add_bullets(s, Inches(0.7), Inches(2.1), Inches(11.7), Inches(4.5), [
    "One piece of hardware -- the same HackRF -- was an FM radio, a "
    "spectrum analyzer, a repeater receiver, a wideband recorder, and a "
    "voice transceiver, in the same 20 minutes.",
    "The only thing that changed between demos was which flowgraph was "
    "loaded -- no soldering, no new hardware.",
    "The recording in Demo 3 wasn't a simulation of the 2m band -- it "
    "was the actual RF, represented as numbers, played back as actual RF.",
    "That's the whole idea of “software defined”: the radio is defined "
    "by the software running on general-purpose hardware, not by "
    "purpose-built circuitry.",
], size=19, gap=16)
footer(s); page_number(s, count(), TOTAL_SLIDES)

# ============================================================= SLIDE 16 ==
s = new_slide()
kicker_title(s, "Where This Goes Next", "More Demo Ideas")
left_items = [
    "CTCSS/PL tone squelch decode",
    "CW (Morse) ID transmitter",
    "RDS decode from FM broadcast",
    "APRS decode (144.390 MHz)",
]
right_items = [
    "WSPR / FT8 weak-signal decode",
    "ADS-B aircraft tracking (1090 MHz)",
    "Cross-band digital repeater",
    "Digital voice (DMR / D-STAR) decode",
]
add_text(s, Inches(0.7), Inches(2.05), Inches(5.6), Inches(0.35), "Quick wins", size=16, color=TEAL, bold=True)
add_bullets(s, Inches(0.7), Inches(2.5), Inches(5.6), Inches(3.8), left_items, size=17, gap=14)
add_text(s, Inches(6.9), Inches(2.05), Inches(5.6), Inches(0.35), "Bigger swings", size=16, color=TEAL, bold=True)
add_bullets(s, Inches(6.9), Inches(2.5), Inches(5.6), Inches(3.8), right_items, size=17, gap=14)
add_text(s, Inches(0.7), Inches(6.5), Inches(11), Inches(0.4),
          "Full writeup with effort/dependency notes: BRAINSTORM.md", size=13, color=MUTED, italic=True)
footer(s); page_number(s, count(), TOTAL_SLIDES)

# ============================================================= SLIDE 17 ==
s = new_slide()
kicker_title(s, "Reference", "Specs at a Glance")
rows = [
    ("Frequency range", "1 MHz – 6 GHz (HackRF One)"),
    ("Sample rate used today", "2–10 Msps depending on demo"),
    ("2m band", "144.000 – 148.000 MHz"),
    ("70cm band", "420.000 – 450.000 MHz"),
    ("2m simplex calling freq", "146.520 MHz"),
    ("Demo 3 capture", "146.0 MHz center @ 6 Msps ≈ 2.9 GB/min"),
    ("HackRF TX power (typical)", "≈ 10–15 dBm max, kept low for these demos"),
]
tx = Inches(0.7); ty = Inches(2.1); tw = Inches(11.9); rh = Inches(0.62)
for i, (k, v) in enumerate(rows):
    row_bg = BG_ALT if i % 2 == 0 else BG
    rect = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, tx, ty + rh * i, tw, rh)
    rect.fill.solid(); rect.fill.fore_color.rgb = row_bg
    rect.line.fill.background(); rect.shadow.inherit = False
    add_text(s, tx + Inches(0.25), ty + rh * i, Inches(4.5), rh, k, size=15,
              color=TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, tx + Inches(5.0), ty + rh * i, tw - Inches(5.2), rh, v, size=15,
              color=BODY, anchor=MSO_ANCHOR.MIDDLE)
footer(s); page_number(s, count(), TOTAL_SLIDES)

# ============================================================= SLIDE 18 ==
s = new_slide()
kicker_title(s, "Resources", "Go Build Something")
add_bullets(s, Inches(0.7), Inches(2.1), Inches(11.7), Inches(4.5), [
    ("GNU Radio", ["gnuradio.org — the toolkit, docs, and tutorials"]),
    ("HackRF One", ["greatscottgadgets.com/hackrf — hardware + firmware"]),
    ("SoapySDR", ["github.com/pothosware/SoapySDR — the hardware abstraction layer used today"]),
    ("ARRL", ["arrl.org — licensing info and Part 97 reference"]),
    ("This kit", ["All flowgraphs, README, and brainstorm doc are in this repo’s "
                   "flowgraphs/ and top-level README.md / BRAINSTORM.md"]),
], size=19, gap=18)
footer(s); page_number(s, count(), TOTAL_SLIDES)

# ============================================================= SLIDE 19 ==
s = new_slide()
add_text(s, Inches(0.9), Inches(2.9), Inches(11.5), Inches(1.2),
          "Thank You", size=48, color=INK, bold=True)
add_text(s, Inches(0.9), Inches(4.0), Inches(11.0), Inches(0.6),
          "Questions? Let's get on the air.", size=20, color=BODY)
accent_bar(s, y=Inches(4.6), x=Inches(0.92), w=Inches(1.4))
add_text(s, Inches(0.9), Inches(6.6), Inches(8), Inches(0.4),
          "Mark Grennan  •  W5TSU  •  mark@grennan.com", size=14, color=MUTED)

prs.save("SDR_Demo.pptx")
print(f"Wrote SDR_Demo.pptx with {len(prs.slides._sldIdLst)} slides")
