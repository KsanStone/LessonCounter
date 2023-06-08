from unittest import TestCase

from ui.application.ApplicationManager import ApplicationManager
from ui.impl.component.Label import Label
from ui.impl.component.TextField import TextField
from ui.impl.pane.VPane import VPane
from ui.interface.Pane import Pane


class TestApplicationManager(TestCase):

    def setUp(self):
        test_ui = VPane()
        test_ui.append(Label("a"))
        test_ui.append(Label("b"))
        self.nest_pane = VPane()
        self.nest_pane.append(Label("c"))
        self.nest_pane.append(Label("d"))
        nest_nest_pane = VPane()
        nest_nest_pane.append(Label("e"))
        nest_nest_pane.append(Label("f"))
        self.nest_pane.append(nest_nest_pane)
        test_ui.append(self.nest_pane)
        self.manager = ApplicationManager(test_ui, None)

    def test_advance_focus(self):
        self.assertIsNone(self.manager.get_focused())
        self.manager.advance_focus()
        self.assertIsNone(self.manager.get_focused())

        field1 = TextField()
        field2 = TextField()
        if isinstance(self.manager.root, Pane):
            self.manager.root.append(field1)
        self.nest_pane.append(field2)

        self.assertIsNone(self.manager.get_focused())
        self.manager.advance_focus()
        self.assertEqual(self.manager.get_focused(), field2)
        self.manager.advance_focus()
        self.assertEqual(self.manager.get_focused(), field1)
        self.manager.advance_focus()
        self.assertEqual(self.manager.get_focused(), field2)




