.PHONY: help setup install run update-all run-cabrera update-cabrera clean test publish

# Colors for terminal output
BLUE := \033[0;34m
GREEN := \033[0;32m
RESET := \033[0m

help: ## Show this help message
	@echo "$(BLUE)Basketball Statistics Scraper - Available Commands$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'

setup: ## Initial setup - create virtual environment
	@echo "$(BLUE)Creating virtual environment...$(RESET)"
	python3 -m venv venv
	@echo "$(GREEN)Virtual environment created!$(RESET)"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run 'make install' to install dependencies"
	@echo "  2. Edit config.yaml to configure your clubs and teams"
	@echo "  3. Copy .env.example to .env and configure database credentials"

install: ## Install dependencies
	@echo "$(BLUE)Installing dependencies...$(RESET)"
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo "$(GREEN)Dependencies installed!$(RESET)"

update-all: ## Update all clubs configured in config.yaml
	@echo "$(BLUE)Updating all configured clubs...$(RESET)"
	./venv/bin/python update_all.py

run-cabrera: ## Quick run for CB Cabrera (club 59)
	@echo "$(BLUE)Running scraper for CB Cabrera...$(RESET)"
	./venv/bin/python club_scraper.py 59 tot

update-cabrera: ## Quick update for CB Cabrera (skip downloads, only generate reports)
	@echo "$(BLUE)Updating reports for CB Cabrera...$(RESET)"
	./venv/bin/python club_scraper.py 59 --skip-downloads tot

run-club: ## Run for specific club (usage: make run-club CLUB_ID=59)
	@if [ -z "$(CLUB_ID)" ]; then \
		echo "Error: Please specify CLUB_ID"; \
		echo "Usage: make run-club CLUB_ID=59"; \
		exit 1; \
	fi
	@echo "$(BLUE)Running scraper for club $(CLUB_ID)...$(RESET)"
	./venv/bin/python club_scraper.py $(CLUB_ID) tot

run-team: ## Run for specific team (usage: make run-team CLUB_ID=59 TEAM_ID=79391)
	@if [ -z "$(CLUB_ID)" ] || [ -z "$(TEAM_ID)" ]; then \
		echo "Error: Please specify both CLUB_ID and TEAM_ID"; \
		echo "Usage: make run-team CLUB_ID=59 TEAM_ID=79391"; \
		exit 1; \
	fi
	@echo "$(BLUE)Running scraper for team $(TEAM_ID) in club $(CLUB_ID)...$(RESET)"
	./venv/bin/python team_scraper.py $(CLUB_ID) $(TEAM_ID) tot

publish: ## Generate and publish web dashboard
	@echo "$(BLUE)Generating web dashboard...$(RESET)"
	./venv/bin/python publish_web.py

serve: ## Start local web server for dashboard
	@echo "$(BLUE)Starting web server...$(RESET)"
	./venv/bin/python web_dashboard.py

test-config: ## Test configuration loading
	@echo "$(BLUE)Testing configuration...$(RESET)"
	./venv/bin/python config_loader.py

clean: ## Clean generated files and caches
	@echo "$(BLUE)Cleaning temporary files...$(RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete
	@echo "$(GREEN)Cleanup complete!$(RESET)"

clean-all: clean ## Clean everything including virtual environment
	@echo "$(BLUE)Removing virtual environment...$(RESET)"
	rm -rf venv
	@echo "$(GREEN)Complete cleanup done!$(RESET)"

backup: ## Create backup of current scripts
	@echo "$(BLUE)Creating backup...$(RESET)"
	mkdir -p backup_$$(date +%Y%m%d_%H%M%S)
	cp *.py config.yaml requirements.txt backup_$$(date +%Y%m%d_%H%M%S)/
	@echo "$(GREEN)Backup created!$(RESET)"
