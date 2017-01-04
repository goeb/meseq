
SRCS = $(wildcard examples/*.msq)
PNGS = $(SRCS:.msq=.png)

all: $(PNGS)

view:
	for i in $(PNGS); do (display $$i &) ; done

%.png: %.msq meseq
	./meseq -o $@ $<

clean:
	$(RM) $(PNGS)
