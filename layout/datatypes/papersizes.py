"""
This module holds page sizes and various mechanisms for manipulating
them.

It is intended to be also useful as a drop-in replacement for the
ReportLab ``lib.pagesizes`` module, and so all the definitions in that
file are duplicated here (although this module is considerably more
comprehensive). The A-size paper sizes of ReportLab are slightly
different to those here, because here we use the conventional purchase
page sizes.
"""
import math
import sys
from units import mm, inch

class ISO269Series(object):
    """
    Instantiate this class to provide a set of paper sizes conforming
    to ISO 269.

    ISO 269 specifies tolerances of at least 1mm in page sizes and
    these are often used to make sure that each page size is an
    integer number of mm in each direction. So A4 is of width 210mm,
    although A0 is 841mm wide. This breaks the normal halving rule,
    but is a widespread standard.

    Instances of this class can be used to retrieve paper sizes by
    using subscript notation: ``A[5]``, for example. There is no limit
    to the large (lower numbered) sizes that can be calculated in this
    way. Because this class always rounds to the nearest millimeter,
    very small paper sizes (high numbered) will be meaningless.

    Arguments:

    ``initial``
        The 'reference' paper size for this series. This is usually a
        large size, most commonly the 0-size.

    ``initial_number``
        The size number of the initial paper size given in the first
        argument.
    """
    def __init__(self, initial, initial_number=0):
        # Store the size internally in mm, so we can do the simplification.
        initial = portrait(initial)
        initial_in_mm = (
            int(initial[0] / mm + 0.5), int(initial[1] / mm + 0.5)
            )
        self.cache = {initial_number:initial_in_mm}
        self.min_cached = initial_number
        self.max_cached = initial_number

    def __getitem__(self, size):
        if size not in self.cache:
            # Calculate afresh from the initial size.
            if size > self.max_cached:
                # We're smaller than the last value stored
                last = self.cache[self.max_cached]
                for s in range(self.max_cached+1, size+1):
                    next = last[1] // 2, last[0]
                    self.cache[s] = next
                    last = next
                self.max_cached = size
            else:
                # We're larger than the initial
                last = self.cache[self.min_cached]
                for s in range(self.min_cached-1, size-1, -1):
                    next = last[1], last[0] * 2
                    self.cache[s] = next
                    last = next
                self.min_cached = size

        # Pull the data from the cache and convert to points.
        width, height = self.cache[size]
        return width*mm, height*mm

def landscape(paper_size):
    """Ensures the paper is in landscape orientation. If it already is,
    no change is made."""
    return max(*paper_size), min(*paper_size)

def portrait(paper_size):
    """Ensures the paper is in portrait orientation. If it already is,
    no change is made."""
    return min(*paper_size), max(*paper_size)

def flip(paper_size):
    """Reverses the orientation of the given paper size."""
    return paper_size[1], paper_size[0]

def small_square(paper_size):
    """Makes a square paper size using the smaller dimension of the
    given paper size."""
    size = portrait(paper_size)[0]
    return size, size

def large_square(paper_size):
    """Makes a square paper size using the larger dimension of the given
    paper size."""
    size = landscape(paper_size)[0]
    return size, size

def subdivide(paper_size, long_axis_strips=1, short_axis_strips=1):
    """
    The paper that you get from cutting the given paper into the given
    number of equal strips along each of its axes. The resulting paper
    will be rotated so it is in the same landscape or portrait
    orientation as its parent (if the input is square and the result
    is not, the result will be landscape). Unlike the ISO 269 series
    papers, the resulting size isn't rounded down, so this can be used
    to find the A5 you get from cutting A4 in half (for example).
    """
    w, h = paper_size
    long_factor = 1.0 / long_axis_strips
    short_factor = 1.0 / short_axis_strips
    if w >= h:
        w, h = w*long_factor, h*short_factor
        return landscape((w, h))
    else:
        w, h = w*short_factor, h*long_factor
        return portrait((w, h))

def half(paper_size):
    """
    The paper that you get from cutting the given paper in half along
    its long axis. A convenience for ``subdivide(paper_size, 2, 1)``
    """
    return subdivide(paper_size, 2)

def quarter(paper_size):
    """
    The paper that you get from cutting the given paper in half along
    both its axes. A convenience for ``subdivide(paper_size, 2, 2)``
    """
    return subdivide(paper_size, 2, 2)

def half_short(paper_size):
    """
    The paper that you get from cutting the given paper in half along
    its short axis. A convenience for ``subdivide(paper_size, 1, 2)``
    """
    return subdivide_short(paper_size, 1, 2)

def is_landscape(paper_size):
    """Checks if the given paper is landscape oriented."""
    return paper_size[0] > paper_size[1]

def is_portrait(paper_size):
    """Checks if the given paper is portrait oriented."""
    return paper_size[0] < paper_size[1]

def is_square(paper_size):
    """Checks if the given paper is square."""
    return paper_size[0] == paper_size[1]

def bleed(paper_size, bleed):
    """Adds the given bleed to the given paper size. Standard sizes
    are 3mm internationally and 1/8" US. Large images and die cuts have
    a larger bleed."""
    return (paper_size[0] + bleed*2.0, paper_size[1] + bleed*2.0)

def calculate_up(paper_size, page_size, page_bleed, separation, margin):
    """Calculates how many pages of the given page size can be fit
    into the given paper size when using a regular rectangular tiling.

    Each page should have the given amount of bleed, and bleeds should
    be separated by the given amount, and the whole piece of paper
    should have the given outside margin.

    The final result is given as an 3-tuple (x, y, rotated) pair of
    integers showing how the pages should be laid out. The rotated
    property is true if the pages should be placed rotated by 90
    degrees from the orientation given.

    It is possible in some cases to fit more pages on the paper by having
    different pages oriented in different ways. This method doesn't try
    to maximize the tiling in that way, and most printers prefer to have
    things tiled rectangularly so that a cutter can use a minimal set
    of dimensions.
    """

    # Calculate the margin after separation. This allows us to combine
    # the separation into the paper size.
    margin2 = margin - separation
    actual_page_size = (
        page_size[0] + 2.0 * page_bleed + separation,
        page_size[1] + 2.0 * page_bleed + separation
        )
    content_size = paper_size[0] - margin2, paper_size[1] - margin2

    # Work out the fitting without rotating.
    xnr = int(math.floor(float(content_size[0]) / float(actual_page_size[0])))
    ynr = int(math.floor(float(content_size[1]) / float(actual_page_size[1])))
    total_nr = xnr * ynr

    # And with rotation
    xwr = int(math.floor(float(content_size[0]) / float(actual_page_size[1])))
    ywr = int(math.floor(float(content_size[1]) / float(actual_page_size[0])))
    total_wr = xwr * ywr

    # Choose which one
    if total_nr > total_wr:
        return (xnr, ynr, False)
    else:
        return (xwr, ywr, True)


# CONSTANTS for specific paper sizes.
# ----------------------------------------------------------------------------

def __build_series(prefix, initial, start_number=0, end_number=10):
    """Creates a set of ISO 269 paper sizes and sets their explicit
    names in the globals of this module. So creating the A series will
    create A0, A1 etc."""
    series = ISO269Series(initial, start_number)

    module = sys.modules[__name__]
    for i in range(start_number, end_number+1): # sizes 0-10
        setattr(module, "%s%d" % (prefix, i), series[i])

    return series

A = __build_series('A', (841*mm, 1189*mm))
"""The ISO 269 A-series of paper sizes, used as the standard paper
size in almost every country of the world (the US being the most
noteable exception)."""

B = __build_series('B', (1000*mm, 1414*mm))
"""The ISO 269 B-series of paper sizes."""

C = __build_series('C', (917*mm, 1297*mm))
"""The ISO 269 C-series of sizes, these are most commonly used as
standard envelope sizes to fit unfolded paper of the corresponding
A-size. So C5 envelopes fit A5 paper, or A4 paper folded in half."""

THIRD_A4 = (A4[0], A4[1]/3.0) # e.g. Compliment slip.
"""The size of an A4 page folded in three on its long axis. This is a
common paper size in European businesses, where it acts as a
'compliment slip."""

DL = (220*mm, 100*mm) # Envelope for THIRD_A4
"""The envelope size that will comfortably fit a :data:`THIRD_A4`
sheet or, more commonly, an A4 sheet folded into three. This is the
most common envelope size for business communications in Europe."""

RA = __build_series('RA', (860*mm, 1220*mm), 0, 4) # Oversize print paper.
"""A slightly oversized version of the ISO 269 A-series of
papers. This is most commonly used as a printer's paper size, where
the final paper will be cropped down to its corresponding A-series
size. It is not part of ISO 269, but follows the same page
proportions. Its sister-series :data:`SRA` is more common in
commercial printing."""

SRA = __build_series('SRA', (900*mm, 1280*mm), 0, 4) # Larger oversize paper.
"""An oversized version of the ISO 269 A-series of papers used for
full-bleed printing. ``SRA2`` is the most common bulk paper size for
commercial printing, although smaller full-bleed digital presses use
``SRA3``."""

A3_PLUS = (329*mm, 483*mm)
"""A lightly oversized version of A4 paper, used for full bleed printing
on some inkjet printers."""

# Additional Japanese paper sizes
JIS_A = __build_series('JIS_A', A[0])
"""Japan doesn't strictly use the ISO 269 page sizes, it has its own
national standard (JIS P 0138). The A-size paper in that standard
conforms to the ISO A-size paper (the two standards mandate different
tolerances, however). For the purposes of this module, the two are
synonymous."""

JIS_B = __build_series('JIS_B', (1030*mm, 1456*mm))
"""Japan has its own national standard B size paper (JIS P 0138) that
follows the ISO 269 page proportions, but has a different reference
size. This object represents that series. The Japanese B size is
slightly larger than its ISO cousin."""

SHIROKU_BAN4 = (264*mm, 379*mm)
"""The JIS P 0138 Shiroku ban size 4, also known as 4x6/4.

Note that the SHIROKU-series don't use the ISO 269 paper proportions,
and so can't be halved to make the next size down."""

SHIROKU_BAN5 = (189*mm, 262*mm)
"""The JIS P 0138 Shiroku ban size 5, also known as 4x6/5.

This paper size also appears in a non-standard size of (191mm x 259mm)
when the paper is cut from a larger sheet. This ambiguity derives from
this paper as a historical paper size, with variations from one
paper-maker to the next. The variant size isn't present in this
module."""

SHIROKU_BAN6 = (127*mm, 188*mm)
"""The JIS P 0138 Shiroku ban size 6, also known as 4x6/6."""


# Sweedish paper sizes
SIS_G5 = (169*mm, 239*mm)
"""Sweeden uses the ISO 269 paper sizes, but adds additional paper sizes in
its national standard SIS 014711. There are only two common sizes that
are not ISO 269 specified. This one and :data:`SIS_E5`."""

SIS_E5 = (155*mm, 220*mm)
"""Sweeden uses the ISO 269 paper sizes, but adds additional paper sizes in
its national standard SIS 014711. There are only two common sizes that
are not ISO 269 specified. This one and :data:`SIS_G5`."""


# Australian / Asian
F4 = (210*mm, 330*mm)


# US Paper sizes
LETTER = (8.5*inch, 11*inch)
"""The most common US paper size. At one point variations of this
paper size were used around the world, now it is largely confined to
the US and its immediate neighbours. It is the size A in the US
national standard ANSI Y 14.1, and is therefore a synonym of
:data:`ANSI_A`."""

LEGAL = (8.5*inch, 14*inch)
"""A taller version of the US Letter paper size."""

TABLOID = (11*inch, 17*inch)
"""The larger standard US paper size, exactly the size of two
:data:`LETTER` sheets. This is a (more archaic) synonym for
:data:`ELEVEN_BY_SEVENTEEN`, but should be treated as deprecated,
since ``TABLOID`` can refer to other sizes in other contexts (in the
printing of newspapers, for example). It also matches the
:data:`ANSI_B` US national standard paper size."""

ELEVEN_BY_SEVENTEEN = TABLOID
"""The larger standard US paper size, exactly the size of two
:data:`LETTER` sheets. This is a more modern synonym for
:data:`TABLOID`), and the :data:`ANSI_B` US national standard paper
size."""

ELEVENSEVENTEEN = TABLOID
"""Another alias for :data:`ELEVEN_BY_SEVENTEEN`. This alias is
included because it the name used in the ReportLab library for this
paper size."""

LEDGER = (17*inch, 11*inch) # landscape version of TABLOID
"""A standard size for old accounding ledgers. This is the same paper
size as the :data:`ELEVEN_BY_SEVENTEEN`, or :data:`TABLOID` paper, but
in landscape orientation."""

ANSI_A = LETTER
"""Size A in the US national standard ANSI Y 14.1, a synonym for
:data:`LETTER`. Note that this is a single paper size, not a series of
paper sizes, as per the ISO 269 sizes."""

ANSI_B = TABLOID
"""Size B in the US national standard ANSI Y 14.1, a synonym for
:data:`ELEVEN_BY_SEVENTEEN`, and :data:`TABLOID`. Note that this is a
single paper size, not a series of paper sizes, as per the ISO 269
sizes."""

ANSI_C = (17*inch, 22*inch)
"""Size C in the US national standard ANSI Y 14.1. Note that this is a
single paper size, not a series of paper sizes, as per the ISO 269
sizes."""

ANSI_D = (22*inch, 34*inch)
"""Size D in the US national standard ANSI Y 14.1. Note that this is a
single paper size, not a series of paper sizes, as per the ISO 269
sizes."""

ANSI_E = (34*inch, 44*inch)
"""Size E in the US national standard ANSI Y 14.1. Note that this is a
single paper size, not a series of paper sizes, as per the ISO 269
sizes."""

# Architectural paper sizes.
ARCH_A = (9*inch, 12*inch)
ARCH_B = (12*inch, 18*inch)
ARCH_C = (18*inch, 24*inch)
ARCH_D = (24*inch, 36*inch)
ARCH_E = (36*inch, 48*inch)
ARCH_E1 = (30*inch, 42*inch)

# Personal organizer page sizes.
FILOFAX_MINI = (4.25*inch, 2.625*inch)
FILOFAX_POCKET = (4.75*inch, 3.25*inch)
FILOFAX_PERSONAL = (6.75*inch, 3.75*inch)
FILOFAX_SLIMLINE = (6.75*inch, 3.75*inch)
FILOFAX_A5 = (8.25*inch, 5.75*inch)
FRANKLIN_COVEY_POCKET = (3.5*inch, 6*inch)
FRANKLIN_COVEY_COMPACT = (4.25*inch, 6.75*inch)
FRANKLIN_COVEY_CLASSIC = (5.5*inch, 8.5*inch)
ORGANIZER_J = (2.75*inch, 5*inch)
ORGANIZER_K = TABLOID
ORGANIZER_L = (5.5*inch, 8.5*inch)
ORGANIZER_M = LETTER

# Cards
INDEX_CARD_5X3 = (5*inch, 3*inch)
INDEX_CARD_6X4 = (6*inch, 4*inch)
INDEX_CARD_8X5 = (8*inch, 5*inch)
ISO_BUSINESS_CARD = (85.60*mm, 52.98*mm)
US_BUSINESS_CARD = (2*inch, 3.5*inch)
UK_BUSINESS_CARD = (85*mm, 55*mm)
JAPANESE_BUSINESS_CARD = (91*mm, 55*mm)
PLAYING_CARD_POKER = B8
PLAYING_CARD_BRIDGE = (56*mm, 88*mm)
PLAYING_CARD = PLAYING_CARD_BRIDGE

# Craft paper sizes
INCHIE = (1*inch, 1*inch)
ATC = (2.5*inch, 3.5*inch)
SCRAPBOOK_6 = (6*inch, 6*inch)
SCRAPBOOK_7 = (7*inch, 7*inch)
SCRAPBOOK_8 = (8*inch, 8*inch)
SMALL_SCRAPBOOK = SCRAPBOOK_8
LARGE_SCRAPBOOK = (12*inch, 12*inch)
SCRAPBOOK = LARGE_SCRAPBOOK
MOO_MINI_CARD = (28*mm, 70*mm)
MOO_BUSINESS_CARD = (55*mm, 84*mm)

# Other miscellaneous paper sizes
GOVERNMENT_LEGAL = (8.0*inch, 10.5*inch)
JUNIOR_LEGAL = (8.0*inch, 5.0*inch)
COMPACT = (4.25*inch, 6.75*inch)
MEMO = ORGANIZER_L
STATEMENT = MEMO
HALF_LETTER = MEMO
MONARCH = (7.25*inch, 10.5*inch)
EXECUTIVE = MONARCH
FOLIO = (8.27*inch, 13*inch)
FOOLSCAP = FOLIO
QUARTO = (9*inch, 11*inch)
SUPER_B = (13*inch, 19*inch)
POST = (15.5*inch, 19.5*inch)
CROWN = (15*inch, 20*inch)
LARGE_POST = (16.5*inch, 21*inch)
DEMY = (17.5*inch, 22.5*inch)
MEDIUM = (18*inch, 23*inch)
BROADSHEET = (18*inch, 24*inch)
ROYAL = (20*inch, 25*inch)
ELEPHANT = (23*inch, 28*inch)
DOUBLE_DEMY = (22.5*inch, 35*inch)
QUAD_DEMY = (35*inch, 45*inch)

# Book page sizes
A_FORMAT_PAPERBACK = (110*mm, 178*mm)
B_FORMAT_PAPERBACK = (130*mm, 198*mm)
C_FORMAT_PAPERBACK = (135*mm, 216*mm)
TRADE_PAPERBACK = C_FORMAT_PAPERBACK

LULU_US_TRADE_PAPERBACK = (6*inch, 9*inch)
LULU_COMIC_BOOK = (6.625*inch, 10.25*inch)
LULU_POCKET_BOOK = (4.25*inch, 6.875*inch)
LULU_LANDSCAPE_BOOK = (9*inch, 7*inch)
LULU_SMALL_SQUARE_BOOK = (7.5*inch, 7.5*inch)
LULU_ROYAL_BOOK = (6.139*inch, 9.21*inch)
LULU_CROWN_QUARTO_BOOK = (7.444*inch, 9.681*inch)
LULU_SQUARE_BOOK = (8.5*inch, 8.5*inch)

# Interesting ratios for constructive page sizes.
FOUR_THIRDS = 4.0 / 3.0 # Old quarto ratio
ISO_RATIO = 1.4142135623730951 # Sqrt 2 - A, B and C paper sizes
TWO_THIRDS = 1.5 # Old octavo / folio ratio
PENTAGON_RATIO = 1.5388417685876266 # Ratio of base to height of a pentagon.
GOLDEN_RATIO = 1.6180339887498949 # (1 + sqrt(5)) / 2

