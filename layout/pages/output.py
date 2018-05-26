import layout.managers.overlay as overlay

class PagesLM(overlay.OverlayLM):
    """
    A layout manager that puts each element in its content list
    on separate pages of a ReportLab document.
    """
    def render(self, rect, data):
        """Render the pages into the given rectangle on subsequent
        pages of the output. This actually outputs the page change,
        so the rectangle given should be the whole page rectangle,
        not a portion of it."""
        for element in self.elements:
            if element: element.render(rect, data)
            data['output'].end_page()
