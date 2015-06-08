from layout.managers import *
from layout.datatypes.position import Point, Rectangle

try:
	from pdfrw import PdfReader
	from pdfrw.buildxobj import pagexobj
	from pdfrw.toreportlab import makerl
except ImportError:
	import warnings
    warnings.warn(
        "PDFRW not found - you will not be able "
        "to use pdf image elements.",
        ImportWarning
        )

class PDFImage(root.LayoutElement):
	"""A PDF file to be displayed at a fixed aspect ratio."""
	
	def __init__(self, filename):
		pages = PdfReader(filename).pages
		num_pages = len(pages)
		assert num_pages > 0
		if num_pages > 1:
			warning.warn("PDF file %s has %d pages, using only the first." % (
				filename, num_pages
				))
		self.pagexobj = pagexobj(pages[0])

	def get_minimum_size(self, data):
		page = self.pagexobj
		return Point(page.BBox[2] - page.BBox[0], page.BBox[3] - page.BBox[1])

	def render(self, rectangle, data):
		page = self.pagexobj

		# Scale and translate.
		w, h = page.BBox[2] - page.BBox[0], page.BBox[3] - page.BBox[1]
		x_scale = rectangle.w / w
		y_scale = rectangle.h / h
		scale = min(x_scale, y_scale)
		extra_x = (rectangle.w - w * scale)*0.5
		extra_y = (rectangle.h - h * scale)*0.5

		# Include the pdf as a form.
		c = data['output']
		c.saveState()
		c.translate(rectangle.x, rectangle.y)
		c.translate(extra_x, extra_y)
		c.scale(scale, scale)
		c.translate(page.BBox[0], page.BBox[1])
		c.doForm(makerl(c, page))
		c.restoreState()