Using the Library
=================

Layout is designed for the flexible composition of document layouts,
particularly complex charts, and multi-page documents of
algorithmically calculated data. It isn't designed to be used as a
framework to flow in large amounts of body text, as the sizing
algorithms used don't take account of text flows.

Overview
--------

There are three stages in using the library:

1. Define classes that will render the content you need to
render. There are a selection of classes in the :mod:`layout.elements`
package that cover some basic needs, but often custom classes are
needed.

2. Compose your layout in a series of managers, subclasses of
:class:`layout.managers.root.LayoutManager`, such as
:class:`layout.managers.margins.PaddedMarginsLM`, which will position the
correct piece of content in the correct position on the page.

3. Render your layout by calling the
:meth:`layout.managers.root.LayoutElement.render` method of the manager at the
top level of your hierarchy. This will render all its children.

Step By Step
------------

The above steps will now be considered in more detail.

Define Classes
~~~~~~~~~~~~~~

Classes should subclass :class:`layout.managers.root.LayoutElement`,
and override two methods: :meth:`get_minimum_size` should return a
:class:`layout.datatypes.position.Point` instance, which specifies the
smallest size this item can be rendered at; and :meth:`render` which takes a
:class:`layout.datatypes.position.Rectangle` instance as the location for its
rendering, and should perform the necessary drawing.

Both of these methods additionally take a data dictionary, which can
contain any additional information about the render that is required.

Note: Use with Report Lab
~~~~~~~~~~~~~~~~~~~~~~~~~

The library was designed to be used with the Report Lab PDF generation
library. The layout managers are renderer agnostic, but the elements
provided in :mod:`layout.elements` render with Report Lab. Although
the data dictionary passed to
:meth:`layout.managers.root.LayoutElement.get_minimum_size` and
:meth:`layout.managers.root.LayoutElement.render` can contain any data that
your rendering classes require, by convention, when you are rendering
with Report Lab, they will contain a `output` field containing a
:class:`reportlab.pdfgen.canvas.Canvas` instance, for rendering.


Compose Your Layout
~~~~~~~~~~~~~~~~~~~

To compose your layout, select appropriate managers and create a data
structure from their instantiation. By convention, all managers take
either a single child, or a list of their children (depending on
whether the manager accepts one or more children) as the last element
in their constructors. The most notable exception to this is the
:class:`layout.managers.grid.GridLM` class, which needs extra data on
each child, so expects you to call its
:meth:`layout.managers.grid.GridLM.add_element` method for each child
you wish to add.

A sample composition might be::

    from layout.managers import *

    top_level_manager = margins.MarginsLM(
        10*mm, 10*mm, 10*mm, 10*mm,
        element=transform.ScaleLM(
            element=directional.HorizontalLM(
                margin=10*mm,
                vertical_align=directional.HorizontalLM.ALIGN_MIDDLE,
                elements=[
                    MyElement(a),
                    MyElement(b)
                    ]
                )
            )
        )

Which is two :class:`MyElement` instances (I assume these are defined
by you) side by side
(:class:`layout.managers.directional.HorizontalLM`) on a page with at
least 10mm margins all around
(:class:`layout.managers.margins.MarginsLM`). If the two elements are
too large to fit in this space, then they will be scaled down, keeping
their relative proportion, until they can fit
(:class:`layout.managers.transform.ScaleLM`). Compositions can get
much more complex, and may have to be assembled in stages.


Create the Output
~~~~~~~~~~~~~~~~~

With the top level manager created, we can build our PDF by calling
its :meth:`render` method. Assuming we're using Report Lab, we could
do this manually::

    canvas = Canvas(filename, papersize)
    top_level_manager.render(Rectangle(0, 0, *papersize), dict(output=canvas))
    canvas.showPage()
    canvas.save()

Or we can rely on the utility functions in the :mod:`layout.rl_utils`
module::

    canvas = Canvas(filename, papersize)
    rl_utils.render_to_reportlab_canvas(canvas, papersize, top_level_manager)
    canvas.save()

or even shorter::

   rl_utils.render_to_reportlab_document(filename, papersize, top_level_manager)
