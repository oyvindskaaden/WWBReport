FILES		= $(patsubst %.csv,%,$(wildcard *.csv))

MD_FILES 	= $(patsubst %,%.md,$(FILES))
JSON_FILES 	= $(patsubst %,%.json,$(FILES))

GENERATOR	= ../GenReport.py

#bash recompile
all: clean $(MD_FILES) $(JSON_FILES)

test: 
	echo $(FILES)

%.md: %.csv
	$(GENERATOR) -f md $*.csv > ./md/$*.md

%.json: %.csv
	$(GENERATOR) -f json $*.csv > ./json/$*.json

clean: 
	rm -f json/*.json
	rm -f md/*.md