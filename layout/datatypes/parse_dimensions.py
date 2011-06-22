"""
This module is designed for parsing dimensions in text form and
turning them into sizes in printer's points (i.e. 72 per inch).
"""
import re

__all__ = ['DimensionError', 'parse_dimension', 'parse_dimensions']

class DimensionError(Exception): pass

def parse_dimension(text):
    """
    Parses the given text into one dimension and returns its
    equivalent size in points.

    The numbers provided can be integer or decimal, but exponents are
    not supported.

    The units may be inches (", in, ins, inch, inchs, inches),
    millimeters (mm), points (pt, pts, point, points, or nothing), or
    centimeters (cm). Because this module is intended for use with
    paper-size dimensions, no larger or smaller units are currently
    supported.
    """
    size, unit = _split_dimension(text)
    factor = _unit_lookup[unit]
    return size*factor

def parse_dimensions(text):
    """
    Parses a set of dimensions into tuple of values representing the
    sizes in points.

    The dimensions that this method supports are exactly as for
    parse_dimension. It supports multiple dimensions, separated by
    whitespace, comma, semicolon, hyphen, or the letter x. The units
    may follow each dimension (in which case they can be different in
    each case) or only after the last one. Because no-units also means
    points, if you have some dimensions in the middle of the set with
    units and some without, then those without will be interpreted as
    points: i.e. the 2 in "1in, 2, 3mm" will be treated as 2 points,
    where as the 1 and 2 in "1, 2, 3mm" will be treated as
    millimeters.
    """
    components = _dimension_separator.split(text)
    if len(components) == 0:
        raise DimensionError("No dimensions found in string.")

    # Split each component into size and units
    pairs = []
    units = 0
    for component in components:
        value, unit = _split_dimension(component)
        pairs.append((value, unit))
        if unit is not None: units += 1

    # Work out what to do with empty units
    if units == 1 and pairs[-1][1]:
        # We need to infer the units
        empty_unit = _unit_lookup[pairs[-1][1]]
    else:
        empty_unit = 1

    # Compile and return the result
    result = []
    for value, unit in pairs:
        if unit: result.append(value * _unit_lookup[unit])
        else: result.append(value * empty_unit)
    return tuple(result)


# ----------------------------------------------------------------------------
# Internal helper functions
# ----------------------------------------------------------------------------

_dimension_finder = re.compile(
    r'^\s*(-?\.[0-9]+|-?[0-9]+(\.([0-9]+)?)?)\s*'
    r'("|in(s)?|inch(s|es)?|mm|cm|pt(s)?|point(s)?)?\s*$'
    )
_dimension_separator = re.compile(r'\s*-\s*|\s*;\s*|\s*,\s*|\s*x\s*|\s+')
_unit_lookup = {
    "pt": 1, "pts": 1, None: 1, "point": 1, "points": 1,
    '"': 72, "in": 72, "ins": 72, "inch": 72, "inchs": 72, "inches": 72,
    'mm': 72/25.4, "cm": 72/2.54
    }

def _split_dimension(text):
    """
    Returns the number and unit from the given piece of text as a pair.

    >>> _split_dimension('1pt')
    (1, 'pt')
    >>> _split_dimension('1 pt')
    (1, 'pt')
    >>> _split_dimension('1  \tpt')
    (1, 'pt')
    >>> _split_dimension('1  \tpt  ')
    (1, 'pt')
    >>> _split_dimension(' 1  \tpt  ')
    (1, 'pt')
    >>> _split_dimension('3')
    (3, None)
    >>> _split_dimension('-12.43mm')
    (-12.43, 'mm')
    >>> _split_dimension('-12.43"')
    (-12.43, '"')
    """
    match = _dimension_finder.match(text)
    if not match:
        raise DimensionError("Can't parse dimension '%s'." % text)
    number = match.group(1)
    unit = match.group(4)
    if '.' in number:
        return (float(number), unit)
    else:
        return (int(number), unit)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
