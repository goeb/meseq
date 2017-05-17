
SRCS = $(wildcard *.msq)
PNGS = $(SRCS:.msq=.png)
MESEQ = ../../meseq

all: $(PNGS)

view:
	for i in $(PNGS); do (display $$i &) ; done

%.png: %.msq $(MESEQ)
	$(MESEQ) -o $@ $<

clean:
	$(RM) $(PNGS)
