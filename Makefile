SHELL := /usr/bin/env bash

.PHONY: install install-claude install-codex

install:
	./install.sh --both

install-claude:
	./install.sh --claude

install-codex:
	./install.sh --codex
