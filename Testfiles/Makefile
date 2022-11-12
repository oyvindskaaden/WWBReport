FILES		= $(patsubst %.csv,%,$(wildcard */*.csv))

MD_FILES 	= $(patsubst csv/%,%.md,$(FILES))
JSON_FILES 	= $(patsubst csv/%,%.json,$(FILES))

GENERATOR	= ../GenReport.py

all: md json

md: md_clean $(MD_FILES)

json: json_clean $(JSON_FILES)

test: 
	echo $(FILES)
	echo $(MD_FILES)
	echo $(JSON_FILES)

%.md: csv/%.csv
	$(GENERATOR) -f md csv/$*.csv > ./md/$*.md

%.json: csv/%.csv
	$(GENERATOR) -f json csv/$*.csv > ./json/$*.json

clean: md_clean json_clean

%_clean:
	rm -f $*/*.$*