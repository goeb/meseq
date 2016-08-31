#! /usr/bin/env python
import cairo
import math

class Diagram(object):
    def __init__(self, filename, width, height):
        self.surface = cairo.SVGSurface(filename + '.svg', width, height)
        cr = self.cr = cairo.Context(self.surface)

        cr.scale(width, height)
        cr.set_line_width(0.01)

        # draw white background
        cr.rectangle(0, 0, 1, 1)
        cr.set_source_rgb(1, 1, 1)
        cr.fill()

        self.draw_dest()

        cr.set_line_width( max(cr.device_to_user_distance(2, 2)) )
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(0, 0, 1, 1)
        cr.stroke()

        self.surface.write_to_png(filename + '.png')
        cr.show_page()
        self.surface.finish()

class Demo1(Diagram):
    def draw_dest(self):
        text = 'request'

        self.cr.set_source_rgba(0, 0, 0)
        self.cr.set_line_width(0.003)
        self.px = max(self.cr.device_to_user_distance(1, 1))
        self.cr.select_font_face('Georgia', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)



        self.arrow(0.25, 0.5, 0.4, 0.51, text)

        self.arrow(0.4, 0.51, 0.6, 0.61, "response")
        self.arrow(0.6, 0.71, 0.4, 0.71, "response")

        self.box(0.2, 0.2, "toto")

    def dot(self, x, y):

        self.cr.arc(x, y, 0.005, 0, 2 * math.pi)
        self.cr.fill()


    def box(self, x, y, text):
        """Draw a box around (x, y), with text and a starting life-line."""

        #self.dot(x, y)

        # the box
        width = w = 0.15
        height = h = 0.07

        self.cr.rectangle(x-w/2, y-h/2, w, h)
        self.cr.stroke()

        # the text
        self.text(x, y, text)

        # the starting life-line
    

    def text(self, x, y, text):
        """Write some text centered on (x, y)."""
        self.cr.set_font_size(0.03)
        fascent, fdescent, fheight, fxadvance, fyadvance = self.cr.font_extents()
        xbearing, ybearing, width, height, xadvance, yadvance = self.cr.text_extents(text)

        xRef = x - width / 2
        yRef = y + fdescent

        self.cr.move_to(xRef, yRef)
        self.cr.show_text(text)

    def arrow(self, x0, y0, x1, y1, text):

        print "arrow(", x0, y0, x1, y1, ")"

        if x1 == x0:
            print "error, arrow"
            return

        elif x1 < x0:
            sign = -1 # indicate that the arrow is from right to left

        else:
            sign = 1

        angle = math.atan((y1-y0)/(x1-x0))

        print "angle=", angle
        size = math.sqrt((y1-y0)**2 + (x1-x0)**2)

        self.cr.save()

        self.cr.translate(x0, y0)

        # a small dot for the starting point of the arrow
        self.dot(0, 0)

        self.cr.rotate(angle) # TODO do not rotate text more than pi

        # the main line of the arrow
        self.cr.move_to(0, 0)
        xHead = size * sign

        self.cr.line_to(xHead, 0)
        self.cr.stroke()

        # head of the arrow
        yHead = 0
        arrowSize = 0.03 # hypothenuse
        hAngle = math.pi / 6
        x2 = xHead - arrowSize * math.cos(hAngle) * sign
        y2 = yHead - arrowSize * math.sin(hAngle)
        self.cr.move_to(xHead, yHead)
        self.cr.line_to(x2, y2)
        self.cr.move_to(xHead, yHead)
        x3 = xHead - arrowSize * math.cos(hAngle) * sign
        y3 = yHead + arrowSize * math.sin(hAngle)
        self.cr.line_to(x3, y3)
        self.cr.stroke()
        

        # text
        self.cr.set_font_size(0.03)
        fascent, fdescent, fheight, fxadvance, fyadvance = self.cr.font_extents()
        xbearing, ybearing, width, height, xadvance, yadvance = self.cr.text_extents(text)


        x = xHead / 2 - width / 2
        y = - fdescent
        print "show_text: ", x, y
        self.cr.move_to(x, y)
        self.cr.show_text(text)


        self.cr.restore()


if __name__ == '__main__':
    size = 600
    Demo1('demo1', size, size)
