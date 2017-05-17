# Generate HTML pages with a menu

SRCS += index.md
SRCS += examples.md

BUILD_DIR=.

HTMLS = $(SRCS:%.md=%.html)
.SECONDARY:
TITLES = $(SRCS:%.md=titles.d/%.title)

DEPENDS = header.html footer.html gen_menu.sh

all: $(HTMLS)

titles.d:
	@mkdir titles.d

titles.d/%.title: %.md titles.d
	@grep -m 1 "^#" $< > $@.tmp
	@cmp $@ $@.tmp || cp $@.tmp $@
	@rm -f $@.tmp

%.html: %.md $(DEPENDS) $(TITLES)
	sh gen_menu.sh --header header.html --footer footer.html --page $< -- $(SRCS) > $@

clean:
	rm -f $(HTMLS)
	rm -rf titles.d


# ----------- examples ----------------
#
EXAMPLES_MSQ = $(sort $(wildcard examples/*.msq))
EXAMPLES_PNG = $(EXAMPLES_MSQ:.msq=.png)
EXAMPLES_STEM = $(EXAMPLES_MSQ:.msq=)
MESEQ = ../meseq

%.png: %.msq $(MESEQ)
	$(MESEQ) -o $@ $<

examples.md: $(EXAMPLES_MSQ) $(EXAMPLES_PNG) Makefile
	@echo "# Meseq Examples" > $@
	for f in $(EXAMPLES_STEM); do \
		echo "## $$(basename $$f.msq)" ; \
		echo ; \
		sed -e "s/^/\t/" $$f.msq ; \
		echo "![]($$f.png)" ; \
		echo ; \
	done >> $@
