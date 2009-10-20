""" Control Widgets.  Presently comprises a Vertical Slider Demo.

    Copyright (C) 2008 - Luke Kenneth Casson Leighton <lkcl@lkcl.net>

"""

from pyjamas import Factory
import math
from pyjamas import DOM
from FocusWidget import FocusWidget
from MouseListener import MouseHandler
from pyjamas.ui import Event
from pyjamas.ui import Focus
from pyjamas.ui import KeyboardListener

from TextBox import TextBox

class Control(FocusWidget, MouseHandler):

    def __init__(self, element, min_value, max_value,
                       start_value=None, step=None,
                       **kwargs):

        self.min_value = min_value
        self.max_value = max_value
        if start_value is None:
            start_value = min_value
        if step is None:
            step = (self.max_value - self.min_value) / 20
        self.step = step
        self.value = start_value
        self.valuechange_listeners = []
        self.dragging = False
        self.drag_enabled = False
        
        if not kwargs.has_key("TabIndex"): kwargs['TabIndex'] = 0
        FocusWidget.__init__(self, element, **kwargs)
        MouseHandler.__init__(self)

    def onFocus(self, sender):
        pass

    def onLostFocus(self, sender):
        pass

    def onClick(self, sender=None):
        pass

    def processValue(self, value):
        """ rounds and limits the value to acceptable range
        """
        value = math.floor((value - self.min_value) / self.step)
        value = (value * self.step) + self.min_value
        value = max(value, self.min_value)
        value = min(value, self.max_value)
        return value

    def setValue(self, new_value, notify=1):

        old_value = self.value
        self.value = new_value

        if not notify:
            return

        for listener in self.valuechange_listeners:
            listener.onControlValueChanged(self, old_value, new_value)

    def addControlValueListener(self, listener):
        self.valuechange_listeners.append(listener)

    def removeControlValueListener(self, listener):
        self.valuechange_listeners.remove(listener)

    def moveControl(self, x, y):
        pass

    def onClick(self, sender=None):
        self.setFocus(True);
        # work out the relative position of cursor
        event = DOM.eventGetCurrentEvent()
        mouse_x = DOM.eventGetClientX(event) 
        mouse_y = DOM.eventGetClientY(event) 
        self.moveControl(mouse_x - self.getAbsoluteLeft(),
                         mouse_y - self.getAbsoluteTop())

    def onMouseMove(self, sender, x, y):
        if not self.dragging:
            return
        self.moveControl(x, y)
        
    def onLoseFocus(self, sender):
        self.dragging = False
        DOM.releaseCapture(self.getElement())
        VerticalDemoSlider.onLoseFocus(self, sender)

    def onMouseDown(self, sender, x, y):
        # regardless of drag_enabled, onMouseDown must prevent
        # default, in order to avoid losing focus.
        DOM.eventPreventDefault(DOM.eventGetCurrentEvent());
        if not self.drag_enabled:
            return
        self.dragging = True
        DOM.setCapture(self.getElement())
        self.moveControl(x, y)

    def onMouseUp(self, sender, x, y):
        self.dragging = False
        DOM.releaseCapture(self.getElement())

    def onMouseEnter(self, sender):
        pass
    def onMouseLeave(self, sender):
        pass

    def onKeyDown(self, sender, keycode, modifiers):
        if keycode == KeyboardListener.KEY_UP:
            DOM.eventPreventDefault(DOM.eventGetCurrentEvent());
            new_value = self.processValue(self.value + self.step)
            self.setControlPos(new_value)
            self.setValue(new_value)
        elif keycode == KeyboardListener.KEY_DOWN:
            DOM.eventPreventDefault(DOM.eventGetCurrentEvent());
            new_value = self.processValue(self.value - self.step)
            self.setControlPos(new_value)
            self.setValue(new_value)

    def onKeyUp(self, sender, keycode, modifiers):
        pass

    def onKeyPress(self, sender, keycode, modifiers):
        pass

Factory.registerClass('pyjamas.ui.Control', Control)

class VerticalDemoSlider(Control):

    def __init__(self, min_value, max_value, start_value=None, step=None,
                       **kwargs):

        if not kwargs.has_key("StyleName"): kwargs['StyleName'] = "gwt-VerticalSlider"

        element = Focus.createFocusable()
        DOM.setStyleAttribute(element, "position", "relative")
        DOM.setStyleAttribute(element, "overflow", "hidden")

        self.handle = DOM.createDiv()
        DOM.appendChild(element, self.handle)

        DOM.setStyleAttribute(self.handle, "border", "1px")
        DOM.setStyleAttribute(self.handle, "width", "100%")
        DOM.setStyleAttribute(self.handle, "height", "10px")
        DOM.setStyleAttribute(self.handle, "backgroundColor", "#808080")

        Control.__init__(self, element, min_value, max_value, start_value, step,
                               **kwargs)

        self.addClickListener(self)
        self.addFocusListener(self)
        self.addMouseListener(self)

    def onFocus(self, sender):
        self.addStyleName("gwt-VerticalSlider-focussed")

    def onLostFocus(self, sender):
        self.removeStyleName("gwt-VerticalSlider-focussed")

    def moveControl(self, mouse_x, mouse_y):

        handle_height = DOM.getIntAttribute(self.handle, "offsetHeight")
        widget_height = self.getOffsetHeight()
        height_range = widget_height - 10 # handle height is hard-coded
        relative_y = mouse_y - (handle_height / 2)
        if relative_y < 0:
            relative_y = 0
        if relative_y >= height_range:
            relative_y = height_range

        relative_y = height_range - relative_y # turn round (bottom to top)

        val_diff = self.max_value - self.min_value
        new_value = ((val_diff * relative_y) / height_range) + self.min_value
        new_value = self.processValue(new_value)

        self.setControlPos(new_value)
        self.setValue(new_value)

    def setControlPos(self, value):

        widget_height = self.getOffsetHeight()
        height_range = widget_height - 10 # handle height is hard-coded
        val_diff = self.max_value - self.min_value
        relative_y = height_range * (value - self.min_value) / val_diff

        # limit the position to be in the widget!
        if relative_y < 0:
            relative_y = 0
        if relative_y >= height_range:
            relative_y = height_range

        relative_y = height_range - relative_y # turn round (bottom to top)

        # move the handle
        DOM.setStyleAttribute(self.handle, "top", "%dpx" % relative_y)
        DOM.setStyleAttribute(self.handle, "position", "absolute")

Factory.registerClass('pyjamas.ui.VerticalDemoSlider', VerticalDemoSlider)

class VerticalDemoSlider2(VerticalDemoSlider):

    def __init__(self, min_value, max_value, start_value=None, **kwargs):

        VerticalDemoSlider.__init__(self, min_value, max_value, start_value,
                                    **kwargs)
        self.addKeyboardListener(self)
        self.drag_enabled = True

Factory.registerClass('pyjamas.ui.VerticalDemoSlider2', VerticalDemoSlider2)

class InputControl(Control):

    def __init__(self, min_value, max_value, start_value=None, step=None,
                       **kwargs):

        if not kwargs.has_key("StyleName"): kwargs['StyleName'] = "gwt-InputControl"
        self.input = TextBox()
        self.input.addKeyboardListener(self)
        #element = DOM.createDiv()
        element = self.input.getElement() # YUK!!!
        Control.__init__(self, element, min_value, max_value, start_value, step,
                               **kwargs)

        self.addClickListener(self)
        self.addFocusListener(self)
        self.addKeyboardListener(self)

    def onFocus(self, sender):
        self.addStyleName("gwt-InputControl-focussed")

    def onLostFocus(self, sender):
        self.removeStyleName("gwt-InputControl-focussed")

    def setControlPos(self, value):

        self.input.setText(value)

    def onKeyPress(self, sender, keycode, modifiers):
        if keycode == KeyboardListener.KEY_ENTER:
            DOM.eventPreventDefault(DOM.eventGetCurrentEvent());
            txt = self.input.getText()
            if not txt:
                return
            new_value = float(txt)
            new_value = self.processValue(new_value)
            self.setControlPos(new_value)
            self.setValue(new_value)
        else:
            Control.onKeyPress(self, sender, keycode, modifiers)


Factory.registerClass('pyjamas.ui.InputControl', InputControl)

