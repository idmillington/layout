import os.path

import unittest
import layout

class TestVersion(unittest.TestCase):
    def text_version_exists(self):
        assert layout.__version__
        
    def test_version_tuple(self):
        assert layout.__version_info__
        assert len(layout.__version_info__) == 3
        for value in layout.__version_info__:
            assert type(value) == int
            
    def test_versions_match(self):
        string = '.'.join([str(value) for value in layout.__version_info__])
        assert string == layout.__version__

