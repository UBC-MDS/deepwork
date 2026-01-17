# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Implemented `prioritize_tasks()` function for ranking tasks by priority
  - Supports "weighted" method combining importance, effort, and deadline urgency
  - Supports "deadline" method prioritizing by deadline proximity
  - Configurable weights for the weighted method
  - Input validation with descriptive error messages
- Added comprehensive unit tests for `prioritize_tasks()` function
- Added pandas dependency to pyproject.toml

### Changed

- Refactored `prioritize_tasks()` with helper functions for improved maintainability

## [0.1.0] - (1979-01-01)

- First release
