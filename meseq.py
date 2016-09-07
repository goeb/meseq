#! /usr/bin/env python
# coding: utf-8
import cairo
import math
import sys
import os


STEP = None

ALIGN_BOTTOM = 1 << 1
ALIGN_CENTER = 1 << 2

ARROW_NORMAL = 1 << 3
ARROW_LOST   = 1 << 4

ARROW_HEAD_LEFT = 1
ARROW_HEAD_RIGHT = 2

class SequenceDiagram(object):

    def __init__(self, filename, matrix, pixWidth):
        global STEP

        self.matrix = matrix
        nActors = len(matrix.rows[-1])
        nMessages = len(matrix.rows)

        nxTiles = 3 * nActors + 1
        STEP = 1.0 * pixWidth / nxTiles
        width = pixWidth;
        nyTiles = nMessages + 2
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

        self.draw()

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

    def draw(self):

        self.init()

        y = 0
        for row in self.matrix.rows:
            y += STEP
            for i in range(len(row)):
                x = 2*STEP + i * STEP * 3
                node = row[i]

                if node is None:
                    pass

                elif node.type == NT_ACTOR:
                    self.box(x, y, node.options['label'])

                elif node.type == NT_MSG_SEND:
                    if node.actorSrc == node.actorDest:
                        # message to self
                        y1 = STEP + STEP * node.arrival.y
                        self.messageToSelf(x, y, y1, node.options['label'])

                    else:
                        x1 = 2*STEP + node.arrival.x * STEP * 3
                        y1 = STEP + STEP * node.arrival.y
                        self.arrow(x, y, x1, y1, node.options['label'])

                elif node.type == NT_MSG_LOST:
                    xArrival = self.matrix.getIndex(node.actorDest)
                    x1 = 2 * STEP + xArrival * STEP * 3
                    y1 = y
                    self.arrow(x, y, x1, y1, node.options['label'], ARROW_LOST)

                elif node.type == NT_BOX:
                    self.boxWithRoundSides(x, y, node.options['label'])

                elif node.type == NT_TERMINATE:
                    self.cross(x, y)

                elif node.type == NT_CREATE:
                    x1 = STEP + node.arrival.x * STEP * 3
                    y1 = STEP + STEP * node.arrival.y
                    self.arrow(x, y, x1, y1, node.options['label'])

                else:
                    pass

                if node is not None:
                    if node.type in [ NT_LIFELINE, NT_MSG_RECV, NT_MSG_SEND, NT_MSG_LOST, NT_CREATE ]:
                        self.lifeLine(x, y-STEP/2, y+STEP/2)
                    elif node.type == NT_TERMINATE:
                        self.lifeLine(x, y-STEP/2, y)


class Demo2(SequenceDiagram):
    def draw(self):

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
NT_ACTOR     = 'actor'
NT_MSG_SEND  = 'send-message'
NT_MSG_RECV  = 'recv-message'
NT_MSG_LOST  = 'lost-message'
NT_CREATE    = 'create'
NT_BOX       = 'box'
NT_BIDIRECTIONAL = "bidirectional"
NT_TERMINATE = 'terminate'
NT_REF_NOTE  = 'ref_note'
NT_COLON     = 'colon'
NT_LIFELINE  = 'lifeline'

class Node:
    def __init__(self, type):
        self.type = type
        self.actorSrc = None
        self.actorDest = None
        self.options = { 'label': '' }
        self.id = None # used for 'goto'

    def __repr__(self):
        return '<%s:%s->%s(%s)>' % (self.type, self.actorSrc, self.actorDest, self.options['label'])

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

        currentLine += line

        if len(line) and line[-1] == '\\':
            # concatenate the next line
            pass
        else:
            outLines.append(currentLine)
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

def tokenParseActors(tokens):
    """Expected tokens:
    actorid [ '=' actorLabel ] ...
    """
    actors = {}
    actorid = None
    gotEqual = False
    for token in tokens:
        if token == '=':
            if actorid is None:
                die("tokenParseActors Invalid = without actorid: %s" % tokens)
            gotEqual = True
        elif gotEqual:
            actors[actorid] = token
            actorid = None
            gotEqual = False
        elif actorid is None:
            actorid = token
        else:
            # previous token was actor id without label
            actors[actorid] = actorid
            actorid = token

    if actorid is not None:
        actors[actorid] = actorid

    return actors


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

    if token2 is not None:
        options['label'] = token2

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
    src = line[0]
    dest = line[2]
    if line[1] == '->': node = Node(NT_MSG_SEND)
    elif line[1] == '<-':
        node = Node(NT_MSG_SEND)
        # reverse src and dest
        src, dest = dest, src
    elif line[1] == '-x': node = Node(NT_MSG_LOST)
    elif line[1] == 'x-':
        node = Node(NT_MSG_LOST)
        src, dest = dest, src
    elif line[1] == '-*': node = Node(NT_CREATE)
    elif line[1] == '<=>': node = Node(NT_BIDIRECTIONAL)
    elif line[1] == '-box': node = Node(NT_BOX)
    else:
        die('Invalid message line: %s' % line)

    node.actorSrc = src
    if node.type != NT_BOX:
        node.actorDest = dest
    else:
        node.options['label'] = dest
    # parse the options
    options = tokenParseKeyEqualValue(line[3:])
    node.options.update(options)

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

    initialActors = {}
    for line in dataTokens['init']:
        if line[0] == 'actors':
            initialActors = tokenParseActors(line[1:])
            
        else:
            die('Invalid declaration in init: %s' % line)

    if len(initialActors) == 0:
        die('No initial actor')

    # parse section 'scenario'
    lifeline = []
    for line in dataTokens['scenario']:
        lifeline.append(tokenParseScenarioLine(line))

    return initialActors, lifeline

class SequenceGraph:
    def __init__(self):
        self.labels = {}
        self.rows = []
        self.activeActors = []
        self.pendingMessages = []
        self.gotoLabels = {}

    def setGotoLabel(self, id):
        self.gotoLabels[id] = len(self.rows) - 1 # index of the last row (== current row)

    def addActiveActor(self, actor):

        for i in range(len(self.activeActors)):
            if self.activeActors[i] is None:
                self.activeActors[i] = actor
                return

        self.activeActors.append(actor)

    def removeActor(self, actorId):
        for i in range(len(self.activeActors)):
            if self.activeActors[i] is not None:
                if self.activeActors[i].actorSrc == actorId:
                    self.activeActors[i] = None
                    return


    def getNewRow(self):
        return [ None for row in self.activeActors ]

    def getIndex(self, actorid):
        for i in range(len(self.activeActors)):
            if self.activeActors[i] is not None:
                if self.activeActors[i].actorSrc == actorid:
                    return i
        return None

    def init(self, initialActors):
        for a in initialActors:
            node = Node(NT_ACTOR)
            node.actorSrc = a
            node.options['label'] = initialActors[a]
            self.addActiveActor(node)

        self.rows = [ self.activeActors[:] ]

    def getCurrentRow(self):
        """Return a reference to the last row."""
        return self.rows[-1]

    def updateLifeline(self):
        """Update last row with lifelines."""
        row = self.rows[-1]
        for i in range(len(self.activeActors)):
            if self.activeActors[i] is not None:
                if row[i] is None:
                    row[i] = Node(NT_LIFELINE)


    def place(self, node, preventTouch = False):
        currentRow = self.getCurrentRow()
        index = self.getIndex(node.actorSrc)
        if index is None:
            die('Cannot place on unknown actor: %s' % node.actorSrc)

        if index == len(currentRow):
            # case of a newly create actor
            currentRow.append(None)

        if currentRow[index] is not None:
            # this row is busy, take the next one
            self.updateLifeline()
            self.rows.append(self.getNewRow())
            currentRow = self.getCurrentRow()

        if preventTouch:
            # check if the row just above has a NT_BOX or NT_ACTOR
            if len(self.rows) > 1 and len(self.rows[-2]) > index:
                nodeAbove =  self.rows[-2][index]
                if nodeAbove is not None and nodeAbove.type in [ NT_BOX, NT_ACTOR ]:
                    # add a row
                    self.updateLifeline()
                    self.rows.append(self.getNewRow())
                    currentRow = self.getCurrentRow()

        currentRow[index] = node
        node.x = index
        node.y = len(self.rows) - 1
        
    def queue(self, node):
        self.pendingMessages.append(node)

    def placePending(self, flushAll = False):
        i = 0
        while i < len(self.pendingMessages):
            node = self.pendingMessages[i]

            if node.options.has_key('goto'):
                gotoId = node.options['goto']
                # in the past, so the node can be placed
                if self.gotoLabels.has_key(gotoId): gotoId = None

            else:
                gotoId = None

            if flushAll or gotoId is None:
                # place the node immediately
                self.place(node)
                self.pendingMessages.pop(i)
            else:
                i += 1 # keep it for later

            
def computeGraph(initialActors, data):
    graph = SequenceGraph()
    # init first row, with initial actors

        
    graph.init(initialActors)

    # go through the lifeline
    for nod in data:
        if nod.type in [ NT_MSG_SEND, NT_MSG_LOST ]:

            graph.place(nod)

            # Do the recv part
            if nod.type == NT_MSG_SEND:
                recvNode = Node(NT_MSG_RECV)
                recvNode.actorSrc = nod.actorDest
                if nod.options.has_key('goto'):
                    recvNode.options['goto'] = nod.options['goto']
                nod.arrival = recvNode
                graph.queue(recvNode)

        elif nod.type == NT_BIDIRECTIONAL:
            otherNode

        elif nod.type == NT_CREATE:
            # TODO check if the arrow may conflict with other message on the row
            # TODO check if id of the new one already exists

            graph.place(nod)

            # place new actor
            newActor = Node(NT_ACTOR)
            newActor.actorSrc = nod.actorDest
            if nod.options.has_key('actorLabel'):
                newActor.options['label'] = nod.options['actorLabel']
            else:
                newActor.options['label'] = newActor.actorSrc

            nod.arrival = newActor
            graph.addActiveActor(newActor)

            graph.place(newActor)
            
        elif nod.type == NT_BOX:
            # insert a row if previous node is a NT_BOX or NT_ACTOR
            # so that they do not touch each other
            graph.place(nod, preventTouch=True)

        elif nod.type == NT_TERMINATE:
            graph.place(nod)
            graph.removeActor(nod.actorSrc)

        elif nod.type == NT_COLON:
            graph.setGotoLabel(nod.id)

        # Look if some pending messages can be received
        graph.placePending()

    # flush pending messages
    graph.placePending(flushAll=True)
        
    return graph
            
        

def generateImage(name, matrix):
    pixWidth = 600
    SequenceDiagram(name, matrix, pixWidth)

def main():
    if len(sys.argv) != 2:
        print "Usage: meseq.py <file>"
        sys.exit(1)

    filename = sys.argv[1]
    f = open(filename)
    inputData = f.read()

    initialActors, data = mscParse(inputData)
    print 'initialActors=', initialActors
    print 'data=', data
    matrix = computeGraph(initialActors, data)
    print "matrix=", matrix.rows
    generateImage(os.path.basename(filename), matrix)

if __name__ == '__main__':
    main()
