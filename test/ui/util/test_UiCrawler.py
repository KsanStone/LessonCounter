from unittest import TestCase

from ui.impl.component.Label import Label
from ui.impl.pane.VPane import VPane
from ui.interface.Pane import Pane
from ui.util.UiCrawler import UiCrawler


class TestUiCrawler(TestCase):

    def setUp(self):
        self.test_ui = VPane()
        self.test_ui.append(Label("a"))
        self.test_ui.append(Label("b"))
        nest_pane = VPane()
        nest_pane.append(Label("c"))
        nest_pane.append(Label("d"))
        nest_nest_pane = VPane()
        nest_nest_pane.append(Label("e"))
        nest_nest_pane.append(Label("f"))
        nest_pane.append(nest_nest_pane)
        self.test_ui.append(nest_pane)

    def test_crawl(self):
        iter_result = list(UiCrawler(self.test_ui))
        self.assertEqual(len(iter_result), 8)
        self.assertEqual(iter_result[0].text, "a")
        self.assertEqual(iter_result[1].text, "b")
        self.assertIsInstance(iter_result[2], Pane)
        self.assertEqual(iter_result[3].text, "c")
        self.assertEqual(iter_result[4].text, "d")
        self.assertIsInstance(iter_result[5], Pane)
        self.assertEqual(iter_result[6].text, "e")
        self.assertEqual(iter_result[7].text, "f")
