#! /usr/bin/env python

import cairo
import math
import sys


STEP = None

ALIGN_BOTTOM = 1 << 1
ALIGN_CENTER = 1 << 2

ARROW_NORMAL = 1 << 3
ARROW_LOST   = 1 << 4

ARROW_HEAD_LEFT = 1
ARROW_HEAD_RIGHT = 2

class Diagram(object):

    def __init__(self, filename, nActors, nMessages, pixWidth):
        global STEP

        nxTiles = 2 + 4 * nActors
        STEP = 1.0 * pixWidth / nxTiles
        width = pixWidth;
        nyTiles = nMessages * 2
        height = nyTiles * STEP

        print "width=", width, ", height=", height, ", STEP=", STEP

        self.surface = cairo.SVGSurface(filename + '.svg', width, height)
        cr = self.cr = cairo.Context(self.surface)

        #cr.scale(width/100.0, height/100.0)
        cr.set_line_width(STEP/40)

        # draw white background
        cr.rectangle(0, 0, width, height)
        cr.set_source_rgb(1, 1, 1)
        cr.fill()

        self.draw_dest()

        cr.set_line_width( max(cr.device_to_user_distance(2, 2)) )
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(0, 0, width, height)
        cr.stroke()

        self.surface.write_to_png(filename + '.png')
        cr.show_page()
        self.surface.finish()

    def init(self):
        self.cr.set_source_rgba(0, 0, 0)
        self.cr.set_line_width(STEP/40)
        self.cr.select_font_face('Georgia', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

    def cross(self, x, y):
        # draw an 'x'
        self.cr.save()
        self.cr.translate(x, y)
        self.cr.rotate(math.pi/4)

        size = STEP/5
        self.cr.move_to(-size, 0)
        self.cr.line_to(size, 0)

        self.cr.move_to(0, -size)
        self.cr.line_to(0, size)

        self.cr.stroke()

        self.cr.restore()

    def dot(self, x, y):

        self.cr.arc(x, y, STEP/20, 0, 2 * math.pi)
        self.cr.fill()


    def boxWithLifeLine(self, x, y, text):
        
        self.box(x, y, text)

        BOX_HEIGHT = STEP * 1
        # the life line
        y0 = y + BOX_HEIGHT/2
        self.cr.move_to(x, y0)
        self.cr.line_to(x, y0 + BOX_HEIGHT/2)
        self.cr.stroke()


    def boxWithRoundSides(self, x, y, text):
        # the box
        width = w = STEP * 2
        height = h = STEP * 1

        # white background
        self.cr.set_source_rgb(1, 1, 1)
        self.cr.rectangle(x-w/2, y-h/2, w, h)
        self.cr.fill()
    
        self.cr.set_source_rgb(0, 0, 0)

        radius = STEP
        angle = math.acos(height/2/radius)
        self.cr.arc(x, y, radius, -angle/2, angle/2)
        self.cr.stroke()
        self.cr.arc(x, y, radius, math.pi-angle/2, math.pi+angle/2)
        self.cr.stroke()

        # draw the horizontal lines
        dy = radius * math.sin(angle)
        self.cr.move_to(x-dy, y-height/2)
        self.cr.line_to(x+dy, y-height/2)

        self.cr.move_to(x-dy, y+height/2)
        self.cr.line_to(x+dy, y+height/2)
        self.cr.stroke()

        # the text
        self.text(x, y, text)

    def box(self, x, y, text):
        """Draw a box around (x, y), with centered text."""

        # the box
        width = w = STEP * 2
        height = h = STEP * 1

        self.cr.rectangle(x-w/2, y-h/2, w, h)
        self.cr.stroke()

        # the text
        self.text(x, y, text)

    
    def lifeLine(self, x, y0, y1):

        self.cr.move_to(x, y0)
        self.cr.line_to(x, y1)
        self.cr.stroke()

    def text(self, x, y, text, flags = ALIGN_CENTER):
        """Write some text centered on (x, y)."""
        self.cr.set_font_size(STEP/4)
        fascent, fdescent, fheight, fxadvance, fyadvance = self.cr.font_extents()
        xbearing, ybearing, width, height, xadvance, yadvance = self.cr.text_extents(text)

        xRef = x - width / 2

        if flags == ALIGN_BOTTOM:
            yRef = y - height / 2
        else: # centered
            yRef = y + fdescent

        self.cr.move_to(xRef, yRef)
        self.cr.show_text(text)

    def arrow(self, x0, y0, x1, y1, text, flags = ARROW_NORMAL):

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

        if flags == ARROW_LOST: size = STEP

        self.cr.save()

        self.cr.translate(x0, y0)

        # a small dot for the starting point of the arrow
        self.dot(0, 0)

        self.cr.rotate(angle)

        # the main line of the arrow
        self.cr.move_to(0, 0)
        xHead = size * sign

        self.cr.line_to(xHead, 0)
        self.cr.stroke()

        yHead = 0

        if flags == ARROW_NORMAL:
            # head of the arrow
            if sign > 0: flag = ARROW_HEAD_RIGHT
            else: flag = ARROW_HEAD_LEFT
            self.arrowHead(xHead, yHead, flag)
        elif flags == ARROW_LOST:
            # draw an 'x'
            self.cross(xHead, yHead)

        else:
            print "error, invalid flag:", flags
        

        # text
        x = xHead / 2
        y = 0
        self.text(x, y, text, ALIGN_BOTTOM)

        self.cr.restore()


    def createActor(self, x0, y0, x1, y1, text):
        self.arrow(x0, y0, x1, y1, text)

    def arrowHead(self, x, y, flags):
        arrowSize = STEP/4 # hypothenuse
        hAngle = math.pi / 6

        if flags == ARROW_HEAD_RIGHT: sign = 1
        else: sign = -1

        x2 = x - arrowSize * math.cos(hAngle) * sign
        y2 = y - arrowSize * math.sin(hAngle)
        self.cr.move_to(x, y)
        self.cr.line_to(x2, y2)

        x3 = x - arrowSize * math.cos(hAngle) * sign
        y3 = y + arrowSize * math.sin(hAngle)
        self.cr.move_to(x, y)
        self.cr.line_to(x3, y3)
        self.cr.stroke()


    def messageToSelf(self, x0, y0, y1, text):

        self.cr.move_to(x0, y0)
        self.cr.line_to(x0 + STEP, y0)
        self.cr.line_to(x0 + STEP, y1)
        self.cr.line_to(x0, y1)

        self.arrowHead(x0, y1, ARROW_HEAD_LEFT)

        # set text
        self.text(x0 + STEP*1.5, y0+STEP*0.5, text)


class Demo2(Diagram):
    def draw_dest(self):

        self.init()

        # Host1
        HOST1 = STEP * 2
        self.boxWithLifeLine(HOST1, STEP, "Host 1")
        self.lifeLine(HOST1, STEP * 2, STEP * 20)

        # Example.com
        EXAMPLE_COM = HOST1 + STEP * 5
        self.boxWithLifeLine(EXAMPLE_COM, STEP, "example.com")
        self.lifeLine(EXAMPLE_COM, STEP * 2, STEP * 20)

        TIME = STEP * 2
        self.arrow(HOST1, TIME, EXAMPLE_COM, TIME+STEP*2, "seq=23")
        TIME += STEP
        self.messageToSelf(HOST1, TIME, TIME+STEP*8, "timer")
        TIME += STEP
        self.arrow(HOST1, TIME, EXAMPLE_COM, TIME+STEP*2, "seq=24")
        self.arrow(EXAMPLE_COM, TIME+STEP, HOST1, TIME+STEP*3, "ack=23", ARROW_LOST)
        TIME += STEP
        TIME += STEP
        self.arrow(EXAMPLE_COM, TIME+STEP, HOST1, TIME+STEP*3, "ack=24")
        self.arrow(HOST1, TIME, EXAMPLE_COM, TIME+STEP*2, "seq=25")

        TIME += STEP
        TIME += STEP
        TIME += STEP
        TIME += STEP
        TIME += STEP
        TIME += STEP
        OTHER = EXAMPLE_COM + STEP*5
        self.createActor(HOST1, TIME, OTHER-STEP, TIME, "create")
        self.boxWithLifeLine(OTHER, TIME, "other host")
        TIME += STEP
        self.lifeLine(OTHER, TIME, TIME + STEP * 3)
        TIME += STEP
        self.boxWithRoundSides(OTHER, TIME, "do something")
        TIME += STEP
        self.arrow(OTHER, TIME, HOST1, TIME, "done")
        TIME += STEP
        self.cross(OTHER, TIME)

# Node types
NT_ACTOR     = 1
NT_MSG       = 2
NT_BOX       = 3
NT_TERMINATE = 4
NT_REF_NOTE  = 5
NT_COLON     = 6
NT_NONE      = 100
class Node:
    def __init__(self, type):
        self.type = type
        self.actorSrc = None
        self.actorDest = None
        self.options = {}
        self.msgVerb = None

    def setOption(self, key, value):
        self.options[key] = value

class Matrix:
    pass

def parseCommandLine():
    pass

def readInput(file):
    pass

class MscDescription:
    def __init__(self):
        self.lines = []

def die(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)

def mscConsolidateLines(data):
    lines = data.splitlines()
    outLines = []
    concatenate = False
    currentLine = ''

    for line in lines:

        if concatenate: currentLine += line
	else: currentLine = line

        if len(line) and line[-1] == '\\':
            # concatenate the next line
            concatenate = True
        else:
            outLines.append(currentLine)
            concatenate=  False
            currentLine = ''

    if len(line) and line[-1] == '\\':
        die('Invalid char \'\\\' on last line')

    return outLines

def mscParseSectionName(line):
    try:
        section = line[1:].split(']')[0]
        return section
    except:
        die('Invalid section declaration: %s' % line)

ReservedTokens = [ '=', ':' ]

def mscParseTokens(line):
    """Return the list of the tokens of the line."""
    # TODO escape \"
    # states
    ST_READY = 0
    ST_IN_TOKEN = 1
    ST_IN_TOKEN_IN_DQUOTE = 2

    state = ST_READY
    tokens = []
    currentToken = None
    for i in range(len(line)):
        c = line[i]
        if state == ST_READY:
            if c.isspace(): continue
            if c == '#': break # rest of the line is a comment
            if c in ReservedTokens:
                tokens.append(c)
                continue
                
            if c == '"':
                state = ST_IN_TOKEN_IN_DQUOTE
                currentToken = ''
            else:
                state = ST_IN_TOKEN
                currentToken = c

        elif state == ST_IN_TOKEN:
            if c in ReservedTokens:
                tokens.append(currentToken)
                tokens.append(c)
                state = ST_READY
                continue
            if c.isspace():
                tokens.append(currentToken)
                state = ST_READY
                currentToken = None
                continue
            if c == '"': state = ST_IN_TOKEN_IN_DQUOTE
            else: currentToken += c

        elif state == ST_IN_TOKEN_IN_DQUOTE:
            if c == '"': state = ST_IN_TOKEN
            else: currentToken += c
           
    # append last token
    if currentToken is not None: tokens.append(currentToken)
    
    return tokens

def tokenParseKeyEqualValue(line):
    token1 = None
    token2 = None
    options = {}
    originalLine = line[:]
    while len(line) > 0:
        tok = line.pop(0)
        if tok == '=':

            if token2 is None:
                die('Invalid = in line: %s' % originalLine)

            if token1 is not None:
                options['label'] = token1

            token1 = token2
            token2 = tok

        elif token1 is None and token2 is None:
            token2 = tok

        elif token2 == '=':
            if token1 is None:
                die('Invalid a=b wihout a, in line: %s' % originalLine)
            key = token1
            value = tok
            options[key] = value
            token1 = None
            token2 = None
        elif token1 is None and token2 is not None:
            token1 = token2
            token2 = tok
        else:
            die('unexpected error in line: %s' % originalLine)

    return options

def tokenParseScenarioLine(line):
    """Return a Node()."""

    if line[0] == ':':
        node = Node(NT_COLON)
        if len(line) == 2:
            node.id = line[1]
        elif len(line) > 2:
            die('Invalid goto-label, len=%d' % len(line))
        return node

    elif len(line) >= 2 and line[1] == '+':
        node = Node(NT_TERMINATE)
        node.actorSrc = line[0]
        return node

    elif len(line) < 3:
        die('Invalid scenario line: %s' % line)

    # message 
    if line[1] in [ '->', '-*', '-x' ] :
        node = Node(NT_MSG)
        node.msgVerb = line[1]
    elif line[1] == '-box':
        node = Node(NT_BOX)
    else:
        die('Invalid message line: %s' % line)

    node.actorDest = line[2]
    # parse the options
    options = tokenParseKeyEqualValue(line[3:])
    node.options = options

    return node


def mscParse(data):
    lines = mscConsolidateLines(data)
    dataTokens = {}
    currentSection = ''
    mscdesc = MscDescription()
    for line in lines:
        line = line.strip()
        if len(line) == 0: continue
        elif line[0] == '#': continue
        elif line[0] == '[':
            currentSection = mscParseSectionName(line)
            dataTokens[currentSection] = []
        else:
            tokens = mscParseTokens(line)
            dataTokens[currentSection].append(tokens)

    initialActors = []
    for line in dataTokens['init']:
        if line[0] == 'actors':
            initialActors = tokenParseKeyEqualValue(line[1:])
            
        else:
            die('Invalid declaration in init: %s' % line)

    if len(initialActors) == 0:
        die('No initial actor')

    # parse section 'scenario'
    lifeline = []
    for line in dataTokens['scenario']:
        lifeline.append(tokenParseScenarioLine(line))

    return initialActors, lifeline

            
def computeGraph(initialActors, data):
    pass

def generateImage(matrix):
    pixWidth = 600
    print "demo2"
    Demo2('demo2', 3, 10, pixWidth)
    pass

def main():
    args = parseCommandLine()
    #inputData = readInput(args.input)
    inputData = """
[init]
actors host1="Host 1" excom="example.com"

[scenario]
    host1 -> excom "seq=23"
    host1 -> host1 "timer"   goto=timer_expiry
    host1 -> excom "seq=24"  goto=a
    excom -x host1 "ack=23"  goto=b x = c fff = erer
    :a
    host1 -> excom "seq=25"  goto=b
    excom -> host1 "ack=24"  goto=c
    :b
    :c
    :
    :timer_expiry

    host1 -* other "create" actor="other host"
    other -box "do something"
    other -> host1 "done"
    other +

    """
    initialActors, data = mscParse(inputData)
    print 'initialActors=', initialActors
    print 'data=', data
    matrix = computeGraph(initialActors, data)
    generateImage(matrix)

if __name__ == '__main__':
    main()
