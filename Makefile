SHELL := /usr/bin/env bash

.PHONY: install install-claude install-codex test

install:
	./install.sh --both

install-claude:
	./install.sh --claude

install-codex:
	./install.sh --codex

test:
	python3 -m unittest discover -s tests -p 'test_*.py' -v
