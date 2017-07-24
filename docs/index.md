
# Meseq Overview

Meseq is a free and open-source generator of message sequence charts. Meseq is a general purpose tool for illustrating real-life scenarios. 

Although (and because) it is not aimed at UML-like modeling nor bound to any programming paradigm, Meseq is suited to engineering design, and all domains where exchange of information matters.

## Inputs

- a text `msq` file

Example:

    [init]
    actor a Alice
    actor b Bob
    
    [scenario]
    a -> b SYN
    a <- b SYN,ACK
    a -> b ACK



## Outputs

- an image

![](examples/01_basic.png)


## Download

Meseq v1.1 (direct link): [https://github.com/goeb/meseq/raw/v1.1/meseq](https://github.com/goeb/meseq/raw/v1.1/meseq)

On Github.com: [https://github.com/goeb/meseq](https://github.com/goeb/meseq)

Git clone: `git clone https://github.com/goeb/meseq.git`
