UV := uv run
PYTHON := python -W ignore -m
RUN := $(UV) $(PYTHON)

all: download analyze

download:
	@$(RUN) src.download org-repos
	@$(RUN) src.download org-members

analyze:
	@$(RUN) src.analyze org-report
	@$(RUN) src.analyze new-repos-by-month

clean:
	rm -rf data/extracted/orgs/*.json
	rm -rf data/extracted/org-members/*.json
	mkdir -p data/transformed/*.csv

.PHONY: all download analyze
