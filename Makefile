UV := uv run
PYTHON := python -W ignore -m
RUN := $(UV) $(PYTHON)

all: download analyze

download:
	@$(RUN) src.download

analyze:
	@$(RUN) src.analyze org-report
	@$(RUN) src.analyze new-repos-by-month

clean:
	rm -rf data/
	mkdir -p data/extracted
	mkdir -p data/transformed

.PHONY: all download analyze
