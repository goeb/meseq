# Command Line

	usage: meseq [-h] [-v] [-f {png,svg}] [-o OUTPUT] [-w WIDTH] file
	
	Process a msq file and generate an image of the message sequence diagram.
	
	positional arguments:
	  file                  msq file
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -v, --verbose         be more verbose
	  -f {png,svg}, --format {png,svg}
	                        format of the generated image (default: png)
	  -o OUTPUT, --output OUTPUT
	                        name of the generated image
	  -w WIDTH, --width WIDTH
	                        width in pixel of the generated image (default: 600)
