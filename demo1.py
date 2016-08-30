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
        self.arrow(0.6, 0.61, 0.4, 0.61, "response")

    def box(self, x, y, text):

        self.cr.rectangle(x, y, 0.5, 0.5)
        self.cr.stroke()



    def arrow(self, x0, y0, x1, y1, text):

        print "arrow(", x0, y0, x1, y1, ")"
        angle = math.atan((y1-y0)/(x1-x0))
        print "angle=", angle
        size = math.sqrt((y1-y0)**2 + (x1-x0)**2)

        self.cr.save()

        self.cr.translate(x0, y0)

        self.cr.arc(0, 0, 0.005, 0, 2 * math.pi)
        self.cr.fill()

        self.cr.rotate(angle) # TODO do not rotate text more than pi

        self.cr.move_to(0, 0)
        self.cr.line_to(size, 0)
        self.cr.stroke()

        # pointer
        x1 = size
        y1 = 0
        arrowSize = 0.03 # hypothenuse
        angle = math.pi / 6
        x2 = x1 - arrowSize * math.cos(angle)
        y2 = y1 - arrowSize * math.sin(angle)
        self.cr.move_to(x1, y1)
        self.cr.line_to(x2, y2)
        self.cr.move_to(x1, y1)
        x3 = x1 - arrowSize * math.cos(angle)
        y3 = y1 + arrowSize * math.sin(angle)
        self.cr.line_to(x3, y3)
        self.cr.stroke()
        

        # text
        self.cr.set_font_size(0.05)
        fascent, fdescent, fheight, fxadvance, fyadvance = self.cr.font_extents()
        xbearing, ybearing, width, height, xadvance, yadvance = self.cr.text_extents(text)


        x = size / 2 - width / 2
        y = - fdescent
        print "show_text: ", x, y
        self.cr.move_to(x, y)
        self.cr.show_text(text)


        self.cr.restore()


if __name__ == '__main__':
    size = 600
    Demo1('demo1', size, size)
