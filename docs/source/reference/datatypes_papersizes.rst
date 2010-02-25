Paper Sizes (:mod:`layout.datatypes.papersizes`)
================================================

.. currentmodule:: layout.datatypes.papersizes

There are a large number of paper sizes defined in this module. The
most common are: :data:`LETTER`, :data:`LEGAL`, the ISO :data:`A`
series (e.g. ``A4``), and the ISO :data:`B` series (e.g. ``B4``).

The ISO 269 paper sizes can be accessed via constant names
(e.g. ``A3`` or ``C5``), from size zero to ten. These and other sizes
outside the range can be accessed using array subscript notation:
``A[-1]``. The individual size names aren't documented here, see the
corresponding series name (i.e. see :data:`A` for information on
``A4``, ``A0`` and so on).

Common formats in other countries, as well as more unusual sizes, such
as Japanese Shiroku papers, are included. 

As well as common paper sizes, the module also includes useful sizes
for things like printer's oversizes (e.g. ``SRA2`` -- see
:data:`SRA`), craft paper (e.g. :data:`LARGE_SCRAPBOOK` [12"x12"]),
business cards (e.g. :data:`ISO_BUSINESS_CARD`) and envelopes
(e.g. :data:`DL`).

Not all of the individual sizes are documented here, see the source
code for a complete list.

The functions in this module are used to transform the paper sizes,
and orient them correctly.

Reference
---------

.. automodule:: layout.datatypes.papersizes
   :members:
   :show-inheritance:
