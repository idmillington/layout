"""
This module contains utility functions to arrange a set of pages for printing.

The functions in this module aren't layout managers in their own right: they
return lists of layout managers, one per page, given a list of elements to
output.
"""
import math
import layout.managers.grid as grid
import layout.managers.margins as margins
import layout.managers.root as root
import layout.managers.transform as transform
import layout.managers.overlay as overlay
import layout.elements.mark as mark
from layout import datatypes

#: Impose four pages in the same orientation as the sheet.
FORMAT_4_PAGE = (2,1, [4, 1, 2, 3])

#: Format two by four pages on a sheet.
FORMAT_8_PAGE = (2,2, [5, 4, 8, 1, 3, 6, 2, 7])

#: Format three by four pages.
FORMAT_12_PAGE = (2,3, [12,1,9,4,8,5,2,11,3,10,6,7])

#: Format sixteen pages so that the two folds will be perpendicular.
FORMAT_16_PAGE_UPRIGHT = (4,2, [13,4,1,16,12,5,8,9,15,2,3,14,10,7,6,11])

#: Format sixteen pages so the sheet is concertina folded twice along
#: its long direction before being folded the other way. This is often used
#: for landscape-oriented output.
FORMAT_16_PAGE_OBLONG = (2,4, [9,8,12,5,13,4,16,1,7,10,6,11,3,14,2,15])

#: A convenience name for the more normal 16-page-upright format.
FORMAT_16_PAGE = FORMAT_16_PAGE_UPRIGHT

#: A six by four layout of pages.
FORMAT_24_PAGE = (4,3, [12,13,24,1,9,16,21,4,8,17,20,5,
                        2,23,14,11,3,22,15,10,6,19,18,7])

#: A regular four by eight layout of pages. This assumes the output will
#: have portrait format pages.
FORMAT_32_PAGE = (4,4, [29,4,5,28,20,13,12,21,17,16,9,24,32,1,8,25,
                        27,6,3,30,22,11,14,19,23,10,15,18,26,7,2,31])

def get_page_impositions(imposition_type,
                         sheets_per_sig=None, fold_then_collate=False,
                         thickness=0.2835, signature_mark=0,
                         elements=[]):
    """
    Calculates impositions for the elements in the content list and
    returns a set of page-layouts for each as manager instances.

    An imposition is a way of laying out pages on a larger sheet, such
    that they can be folded and cut to form a booklet.
    The signature size of an imposition controls how many of these
    large sheets can fold together as one. Larger books are made up of
    multiple signatures sewn together in a codex.

    Arguments:

    ``imposition_type``
        One of the FORMAT_* constants defined in this module: controls
        the kind of imposition to make.

    ``sheets_per_sig``
        How many sheets of paper will be folded, cut and bind
        together. This is often 1 for commercial presses, but DIY
        laser printouts often have all the pages in one signature (for
        stapling). If this value isn't provided, the function will
        assume the latter.

    ``fold_then_collate``
        If this is true then each printed sheet will be folded and
        cut, then the bundle of resulting pages will be combined with
        the others from its signature. This kindof defeats the object
        of printing in signatures, but is needed when building
        multi-signature books using a laser printer. It only makes
        sense if you have more than one sheet per sig.

    ``thickness``
        When many pages are folded together, the thickness of the
        sheets adds up. Giving a page thickness to this argument moves
        the printed pages around slightly to compensate.

    ``signature_mark``
        When working with many signatures, it can be fiddly to sort
        the signatures into the correct order for binding. To help we
        can add 'signature marks' - a triangle on the spine of each
        signature indicating up, and offset from signature to
        signature. When the signatures are correctly collated, the
        marks form a diagonal pattern: it is obvious when they are not
        correct. The value of this argument indicates the width of
        this pattern. Zero indicates that no mark should be added.

    ``elements``
        The list of individual page element to impose. There can be
        fewer pages to layout than spaces on the layout (i.e. in a 16
        page imposition, we could only have 13 pages), any additional
        space is left blank.

    The returned page layouts can be given to a PageLM for rendering
    onto individual pages of output. This method isn't a layout
    manager in its own right.
    """
    # Take a copy of the elements list so we can mess with it.
    elements = elements[:]

    # Sanity check the type
    s = set(imposition_type[2])
    assert len(s) == imposition_type[0] * imposition_type[1] * 2
    assert max(*list(s)) == imposition_type[0] * imposition_type[1] * 2
    assert min(*list(s)) == 1

    # Calculate the sheets per signature.
    if sheets_per_sig is None:
        if imposition_type == FORMAT_4_PAGE:
            sheets_per_sig = int(math.ceil(len(elements) / 4.0))
        else:
            sheets_per_sig = 1

    # Find basic data.
    cols, rows, pattern = imposition_type
    pages_per_side = cols * rows
    pages_per_sheet = pages_per_side * 2
    pages_per_signature = sheets_per_sig * pages_per_sheet
    num_pages = len(elements)
    sheets_needed = int(math.ceil(num_pages / float(pages_per_sheet)))
    signatures_needed = int(math.ceil(sheets_needed / float(sheets_per_sig)))

    # Add effective margins to account for page thickness.
    if thickness > 0:
        total_offset = (
            sheets_per_sig * pages_per_side * thickness * math.pi * 0.25
            )

        for index, element in enumerate(elements):
            # Work out which spread this page is on.
            index_in_sig = index % pages_per_signature
            if (index_in_sig >= pages_per_signature / 2):
                index_in_sig = pages_per_signature - 1 - index_in_sig

            # How many thicknesses are we from the outside of the sig
            out_d = (index_in_sig + 1) // 2

            # And what offset is that from the inside.
            outer_extra = out_d * thickness * math.pi * 0.5
            inner_extra = total_offset - outer_extra

            # Work it out in terms of right and left
            if index % 2 == 0:
                left, right = inner_extra, outer_extra
            else:
                left, right = outer_extra, inner_extra

            # Add the new margins
            margined = margins.MarginsLM(0, right, 0, left, element)
            elements[index] = margined

    # Come up with the output plan: the order of pages to output.
    output_elements = []
    for sig in range(signatures_needed):
        sig_offset = sig * pages_per_signature

        # Add the signature mark to the start page of the
        # signature.
        if signature_mark > 0:
            elements[sig_offset] = overlay.OverlayLM(
                elements = [
                    elements[sig_offset],
                    mark.SignatureMark(sig, signatures_needed, signature_mark)
                    ]
                )

        if fold_then_collate:
            # We fold and cut each sheet, then combine them into
            # their signatures.
            for sheet in range(sheets_per_sig):
                offset = sig_offset + sheet * pages_per_side
                second_half_offset = \
                    offset + pages_per_signature - (sheet+1)*pages_per_sheet

                for index, slot in enumerate(pattern):
                    if slot > pages_per_side:
                        page_index = second_half_offset + slot - 1
                    else:
                        page_index = offset + slot - 1

                    if page_index >= num_pages:
                        output_elements.append(None)
                    else:
                        output_elements.append(elements[page_index])

        else:
            # We collate the sheets together, then fold them as a whole
            # and cut to form the signature.
            sig_elements = [None] * pages_per_signature
            page_number = 0
            increasing = True
            for pattern_index in range(0, pages_per_sheet, 2):
                # We're looping for each double folio in the sheet

                # Find where these folios are in the pattern
                location_in_pattern = [
                    pattern.index(pattern_index+1),
                    pattern.index(pattern_index+2)
                    ]

                # Go through each sheet in the signature
                for sheet in range(sheets_per_sig):
                    sheet_number = \
                        sheet if increasing else sheets_per_sig-1-sheet

                    # Place the next page at this given location
                    for page in range(2):
                        slot_index = (
                            sheet_number * pages_per_sheet +
                            location_in_pattern[page]
                            )
                        page_index = page_number + sig_offset
                        if page_index < num_pages:
                            sig_elements[slot_index] = elements[page_index]

                        page_number += 1

                # Next time through, go in the reverse order.
                increasing = not increasing

            # Add all the elements for this signature to the whole
            output_elements.extend(sig_elements)



    # Invert the relevant pages
    for index, element in enumerate(output_elements):
        # Check if it needs to be upside down.
        row_from_bottom = rows - 1 - (index % pages_per_side) // cols
        if element is not None and row_from_bottom % 2 > 0:
            output_elements[index] = transform.RotateLM(2, element)

    # Split them into simple grids and pages.
    pages = []
    for index in range(0, len(output_elements), pages_per_side):
        side_elements = output_elements[index:index+pages_per_side]
        pages.append(grid.SimpleGridLM(
                cols, rows, margin=0, elements=side_elements
                ))
    return pages



def get_pocketmod_pages(elements,
                        page_edge_bottom=True,
                        first_page_vertical=True):
    """
    Creates one or more managers that wraps the given elements into
    one or more Pocket Mod-style page sets. Each manager in the list
    that is returned corresponds to one page. This imposer is designed
    to work with portrait oriented content pages, laid out onto a
    landscape oriented page.

    Arguments:

    ``elements``
        The elements to lay out. PocketMod uses sheets with 8 pages on
        them, but you can pass in fewer elements - additional space
        will be left blank. The number of pages output is just the
        ceiling of the number of pages passed in divided by 8.

    ``page_edge_bottom``
        If true the pages should be arranged so that, when folded, the
        bottom of each page touches the edge of the sheet of
        paper. This is normal, because the edge of the paper is where
        a normal printer blank-margin is located, and the bottom edge
        of a page usually has the largest margin.

    ``first_page_vertical``
        If true then the fold on the first page will be vertical. Each
        'page' in the book has either a fold on the outside edge or on
        one of the two horizontal edges (the top edge if
        page_edge_bottom is set, the bottom otherwise). The horizontal
        fold keeps the page together more strongly, so is normally
        used for the first page. The original Pocket Mod software has
        the first page with a horizontal fold.

    The returned page layouts can be given to a PageLM for rendering
    onto individual pages of output. This method isn't a layout
    manager in its own right.
    """
    pages = {
        (False, False):[2,3,4,5,1,8,7,6],
        (False, True):[4,5,6,7,3,2,1,8],
        (True, False):[5,4,3,2,6,7,8,1],
        (True, True):[7,6,5,4,8,1,2,3]
        }[page_edge_bottom, first_page_vertical]
    output = []
    num_pages = len(elements)
    for index in range(0, num_pages, 8):
        sglm = grid.SimpleGridLM(4, 2)

        for cell_index, cell in enumerate(pages):
            if index + cell - 1 < num_pages:
                element = elements[index+cell-1]
                if (cell_index > 3) != page_edge_bottom:
                    element = transform.RotateLM(2, element)
                sglm.add_element(element)
            else:
                sglm.add_element(None)
        output.append(sglm)
    return output

