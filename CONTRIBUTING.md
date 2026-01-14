# Contributing Guidelines

Thank you for your interest in contributing to this project.  
This document outlines the conventions and workflow used throughout the repository to ensure clarity, consistency, and maintainability.

Although this is primarily a personal project, the following guidelines reflect professional development practices and help maintain a clean and understandable history.

---

## 1. Commit Message Standards

This project follows a semantic commit style inspired by Conventional Commits.

### **Format**
<type>(<scope>): <short description>

### **Allowed Types**
- **feat** — New feature or functionality  
- **fix** — Bug fix or behavior correction  
- **refactor** — Internal changes that do not alter behavior  
- **test** — Adding or modifying tests  
- **docs** — Documentation updates  
- **style** — Formatting, naming, or non-functional changes  
- **chore** — Maintenance, tooling, or dependency updates  

### **Scopes**
Use a scope to indicate the area affected:
- **player** — Playback logic  
- **playlist** — Track navigation, loading, indexing  
- **ui** — Tkinter UI, images, labels  
- **core** — Utilities, resource loading, shared logic  
- **tests** — Test suite structure or fixtures  

### **Examples**
feat(player): add shuffle mode
fix(ui): correct label color update on pause
refactor(core): simplify resource_path logic
test(playlist): add boundary test for last track
docs: update README with usage instructions

---

## 2. Branching Strategy

For small changes, commits directly to `main` are acceptable.  
For larger features or refactors, use short‑lived branches:
feature/shuffle-mode
refactor/ui-load-image
fix/player-state-transition

Merge back into `main` once the feature is stable and tests pass.

---

## 3. Testing Guidelines

All new features or bug fixes should include corresponding tests when applicable.

### **Test Principles**
- Tests should be isolated and deterministic  
- UI and VLC interactions must be mocked  
- Fixtures should handle heavy setup  
- Each test should focus on a single behavior  

### **Running Tests**
pytest -q

All tests must pass before merging.

---

## 4. Code Style

- Follow Python’s PEP8 style guide  
- Keep functions small and focused  
- Avoid duplicating logic across UI and player modules  
- Prefer pure functions where possible  
- Use descriptive names for variables and methods  

---

## 5. Adding New Features

When adding a new feature:

1. Create a dedicated branch  
2. Write or update tests first (TDD encouraged but not required)  
3. Implement the feature  
4. Ensure all tests pass  
5. Write a clear commit message  
6. Update documentation if needed  

---

## 6. UI and Resource Handling

- All images should be loaded through `load_image()`  
- Paths must be resolved using `resource_path()`  
- UI updates should be centralized and consistent  
- Avoid embedding absolute paths in code  

---

## 7. Pull Requests (Optional)

If using PRs for your own workflow:

- Keep them small and focused  
- Include a summary of changes  
- Reference related commits or tests  
- Ensure CI (if configured) passes  

---

## 8. Project Philosophy

This project serves as:
- A learning environment  
- A showcase of professional workflow  
- A hybrid QA/Dev practice ground  
- A portfolio piece demonstrating testing, refactoring, and UI design  

Consistency and clarity are prioritized over speed.

---

Thank you for helping maintain a clean and professional codebase.



