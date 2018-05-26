import math
from layout import datatypes
from . import root

class SimpleGridLM(root.GroupLayoutManager):
    """
    A simple grid takes a number of elements and arranges them
    in rows and columns so that each element is the same size.
    """
    def __init__(self, columns=1, rows=1, margin=0, elements=[]):
        super(SimpleGridLM, self).__init__(elements)
        self.rows = rows
        self.cols = columns
        self.margin = margin

    def calculate_columns(self):
        """Assuming the number of rows is constant, work out the best
        number of columns to use."""

        self.cols = int(math.ceil(len(self.elements) / float(self.rows)))

    def calculate_rows(self):
        """Assuming the number of columns is constant, work out the
        best number of rows."""

        self.rows = int(math.ceil(len(self.elements) / float(self.cols)))

    def get_minimum_size(self, data):
        cell_size = self._get_smallest_dimensions(data)
        return datatypes.Point(
            cell_size.x * self.cols + self.margin * (self.cols-1),
            cell_size.y * self.rows + self.margin * (self.rows-1)
            )

    def render(self, rectangle, data):
        effective_width = rectangle.w - self.margin * (self.cols-1)
        effective_height = rectangle.h - self.margin * (self.rows-1)
        cell_width = effective_width / float(self.cols)
        cell_height = effective_height / float(self.rows)

        for row in range(self.rows):
            for col in range(self.cols):
                element_index = col + row * self.cols
                if element_index >= len(self.elements):
                    return
                element = self.elements[element_index]
                if not element: continue
                element.render(datatypes.Rectangle(
                        rectangle.x + col*(cell_width + self.margin),
                        rectangle.y + rectangle.h -
                            (row+1)*(cell_height) - row*self.margin,
                        cell_width, cell_height
                        ), data)

class GridLM(root.LayoutManager):
    """
    Lays out elements in a grid with flexible sized rows and columns.
    """
    def __init__(self, margin=0, outside_margin=0):
        self.rows = 1
        self.cols = 1
        self.margin = margin
        self.outside_margin = outside_margin
        self.elements = []
        self.rules = []
        self.col_widths = None
        self.row_heights = None

        # The row that gets all additional space
        self.scaling_row = None
        # And the column that gets all additional width
        self.scaling_col = None

    def add_element(self, element, col, row, cols=1, rows=1):
        """Adds the given element to the given position in the grid,
        with the given size. There is no limit to the number of elements
        that can be assigned to the same cell(s)."""

        # Update the number of rows and colums
        self.rows = max(self.rows, row+rows)
        self.cols = max(self.cols, col+cols)

        # Add the raw element record
        self.elements.append((col, row, cols, rows, element))

    def add_rule(self, start_col, start_row, end_col, end_row,
                 width=0.5, color=(0,0,0)):
        """Adds a rule to the grid. The row and column numbers are
        those on the top left of the corresponding cell in the
        grid. So if the grid is 10x10, then the right hand edge of the
        grid will be column 10, and the bottom will be column 10. In
        other words there is one more rule-row and column than there
        are cell rows and columns."""
        self.rules.append(
            (start_col, start_row, end_col, end_row, width, color)
            )

    def _compile_dimension_size(self, base_index, array,
                                property, sized_elements):
        """Build one set of col widths or row heights."""
        sort_index = base_index + 2
        sized_elements.sort(key=lambda x: x[sort_index])
        for element_data in sized_elements:
            start, end = element_data[base_index], element_data[sort_index]
            end += start
            element, size = element_data[4:6]

            # Find the total current size of the set
            set_size = sum(array[start:end]) + (end-start-1)*self.margin

            # Work out the extra space we need
            extra_space_needed = getattr(size, property) - set_size
            if extra_space_needed < 0: continue

            # Distribute it among the entries
            extra_space_each = extra_space_needed / (end-start)
            for index in range(start, end):
                array[index] += extra_space_each

    def get_minimum_size(self, data):
        """Finds the minimum size of the grid."""

        # Gat a list of elements with their sizes, so we don't have to
        # recalculate that each time.
        sized_elements = [
            (col, row, cols, rows, element, element.get_minimum_size(data))
            for col, row, cols, rows, element in self.elements
            ]

        # Create the heights and widths for each cell.
        self.col_widths = [0] * self.cols
        self.row_heights = [0] * self.rows
        self._compile_dimension_size(0, self.col_widths, 'x', sized_elements)
        self._compile_dimension_size(1, self.row_heights, 'y', sized_elements)

        # The final size is the total width and height
        om = 2*self.outside_margin
        return datatypes.Point(
            sum(self.col_widths) + (self.cols-1)*self.margin + om,
            sum(self.row_heights) + (self.rows-1)*self.margin + om
            )

    def render(self, rect, data):
        """Draws the cells in grid."""
        size = self.get_minimum_size(data)

        # Find how much extra space we have.
        extra_width = rect.w - size.x
        extra_height = rect.h - size.y

        # Distribute the extra space into the correct rows and columns.
        if self.scaling_col is None or not 0 <= self.scaling_col < self.cols:
            width_per_col = extra_width / float(self.cols)
            col_widths = [
                width + width_per_col
                for width in self.col_widths
                ]
        else:
            col_widths = self.col_widths[:]
            col_widths[self.scaling_col] += extra_width

        if self.scaling_row is None or not 0 <= self.scaling_row < self.rows:
            height_per_row = extra_height / float(self.rows)
            row_heights = [
                height + height_per_row
                for height in self.row_heights
                ]
        else:
            row_heights = self.row_heights[:]
            row_heights[self.scaling_row] += extra_height

        # Find the (start, end) positions of each row and column.
        col_xs = []
        last_x = rect.left + self.outside_margin
        for width in col_widths:
            col_xs.append((last_x, last_x + width))
            last_x += width + self.margin
        row_ys = []
        last_y = rect.top - self.outside_margin
        for height in row_heights:
            row_ys.append((last_y, last_y - height))
            last_y -= height + self.margin

        # Now we can loop over the elements and have them rendered.
        for col, row, cols, rows, element in self.elements:
            x_start = col_xs[col][0]
            y_start = row_ys[row][0]
            x_end = col_xs[col+cols-1][1]
            y_end = row_ys[row+rows-1][1]
            element.render(datatypes.Rectangle(
                x_start, y_end, x_end-x_start, y_start-y_end
                ), data)

        # And finally we can draw the rules
        def _get_value(array, index, sign):
            """Returns the value of the index in the given array, where
            the array (like col_xs and row_ys), consists of start-end pairs
            of values."""
            if index <= 0:
                # Special case, it is the start of the first range
                return array[0][0]-self.outside_margin*sign
            elif index >= len(array):
                # Special case, it is the end of the last range
                return array[-1][1]+self.outside_margin*sign
            else:
                # Otherwise it is the blend of a start and end.
                return (array[index-1][1] + array[index][0])*0.5

        for start_col, start_row, end_col, end_row, width, color in self.rules:
            x_start = _get_value(col_xs, start_col, 1)
            y_start = _get_value(row_ys, start_row, -1)
            x_end = _get_value(col_xs, end_col, 1)
            y_end = _get_value(row_ys, end_row, -1)
            data['output'].line(
                x_start, y_start, x_end, y_end,
                stroke=color,
                stroke_width=width
                )
