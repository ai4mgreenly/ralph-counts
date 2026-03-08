INSTALL_DIR := $(HOME)/.local/share/ralph-counts
BIN_DIR := $(HOME)/.local/bin

.PHONY: install

install:
	mkdir -p $(INSTALL_DIR)
	rm -rf $(INSTALL_DIR)/serve.py $(INSTALL_DIR)/index.html $(INSTALL_DIR)/favicon.ico
	cp serve.py index.html favicon.ico $(INSTALL_DIR)/
	mkdir -p $(BIN_DIR)
	printf '#!/bin/sh\nexec python3 ~/.local/share/ralph-counts/serve.py "$$@"\n' > $(BIN_DIR)/ralph-counts
	chmod +x $(BIN_DIR)/ralph-counts
