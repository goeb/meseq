# Examples
## 01_basic.msq

	
	# This is a comment
	
	[init]
	actor a Alice
	actor b Bob
	
	[scenario]
	a -> b SYN
	a <- b SYN,ACK
	a -> b ACK
	
![](examples/01_basic.png)

## 02_create_actor.msq

	[init]
	actor a Alice
	
	[scenario]
	a -* b label=create actor_label=Bob
	a -> b stop
	b + end
	
![](examples/02_create_actor.png)

## 03_box.msq

	[init]
	actor a Alice
	actor ""
	actor b Bob
	
	[scenario]
	b -box ready
	a -> b SYN
	b -box "computing...\n(step 1)"
	a -box waiting...
	b -box "computing...\n(step 2)"
	a <- b SYN,ACK
	a -> b ACK
	
![](examples/03_box.png)

## 04_multilines.msq

	[init]
	actor a Alice\n(9ca230838602)
	actor ""
	actor b Bob
	
	[scenario]
	a -> b "SYN\nSeq=0, Len=0\nMSS=1460, Win=29200"
	a <- b SYN,ACK
	a -> b ACK
	
![](examples/04_multilines.png)

## 05_double_arrow.msq

	[init]
	actor a Alice
	actor b Bob
	actor c Charlie
	actor d David
	actor e Emily
	
	[scenario]
	:
	c <-> b Exchange\nkeys
	d <-> e Exchange\nkeys
	a <-> d Exchange\nkeys
	:
	
![](examples/05_double_arrow.png)

## 06_return_arrow.msq

	[init]
	actor a Alice
	actor b Clock
	actor c Charlie
	
	[scenario]
	:
	a -< b Get\ntime
	b >- c Get\ntime
	:
	
![](examples/06_return_arrow.png)

## 07_message_lost.msq

	[init]
	actor a Alice
	actor ""
	actor ""
	actor b Bob
	
	[scenario]
	a -x b SYN
	a -> b SYN
	
![](examples/07_message_lost.png)

## 09_crossing.msq

	[init]
	actor a Alice
	actor ""
	actor ""
	actor b Bob
	
	[scenario]
	a -> b msg-x goto=L1
	a <- b msg-y goto=L1
	:L1
![](examples/09_crossing.png)

## 10_timeout.msq

	[init]
	actor a Alice
	actor ""
	actor ""
	actor b Bob
	
	[scenario]
	a -> b hello
	b -box ignore
	a -> a timeout\n6s
	a -> b "I said hello!"
	
![](examples/10_timeout.png)

## 14_alignment.msq

	[init]
	actor a Alice
	actor ""
	actor ""
	actor b Bob
	
	[scenario]
	b -box "halign=left\nverify\n in the\ndatabase\n..." halign=left
	a -box "default halign\n(halign=center)\ntwo\nthree"
	
	a -box "halign=center_left\nchecklist:\n\
	1. one\n2. two\n3. three" halign=center_left
	
	b -box "align right\nabc\ndefghi" halign=right
	:
	
![](examples/14_alignment.png)

## 15_layout.msq

	[init]
	actor a Alice
	actor ""
	actor ""
	actor b Bob
	
	[scenario]
	a -> b SYN
	a <- b SYN,ACK
	:
	:
	:
	a -> b ACK
	
![](examples/15_layout.png)

## 16_decoration.msq

	[init]
	actor a Alice color=blue
	actor b Bob
	font-family helvetica
	font-size 130%
	font-style bold
	
	[scenario]
	a -> b SYN color=666 # grey
	a <- b SYN,ACK font-size=2
	a -> b ACK
	b -* c actor_bgcolor=orange actor_label=Charlie
	b -box waiting... bgcolor=yellow
	:
	
![](examples/16_decoration.png)

## 17_utf8.msq

	[init]
	actor a Alice
	actor b Bérénice
	
	[scenario]
	a -> b "où vas-tu ?"
	a <- b "au théâtre"
![](examples/17_utf8.png)

## 20_include.msq

	[init]
	actor a Alice
	
	[scenario]
	-include step_init
	-include step_do_transaction
	-include step_do_transaction
	-include step_do_transaction
	
	-include 20_include_1.msqi
	
	[step_init]
	a -* b create actor_label=Bob
	
	[step_do_transaction]
	a -> b "do step"
	a <- b "ok"
![](examples/20_include.png)

