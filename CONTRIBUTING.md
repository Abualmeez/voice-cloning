# Contributing to Voice Cloning Studio

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Run tests
6. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/voice-cloning.git
cd voice-cloning

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development tools (optional)
pip install pytest black flake8 mypy
```

## Code Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Include type hints where possible
- Validate all user inputs
- Add tests for new features
- Update documentation

## Security

- Never commit secrets or credentials
- Validate file paths to prevent traversal
- Sanitize user inputs
- Run security scanners before PR
- Follow principle of least privilege

## Testing

```bash
# Run tests (when available)
pytest tests/

# Format code
black *.py src/ scripts/

# Lint code
flake8 *.py src/ scripts/

# Type checking
mypy src/
```

## Pull Request Process

1. Update README.md with changes
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md (if exists)
5. Request review from maintainers

## Code Style

- Use descriptive variable names
- Keep functions focused and small
- Comment complex logic
- Use type hints:
  ```python
  def clone_voice(text: str, voice_path: Path) -> Path:
      """Clone voice with given text."""
      ...
  ```

## Commit Messages

Use clear, descriptive commit messages:

```
Add authentication support to web UI

- Implement --auth flag for username/password
- Update documentation with security notes
- Add tests for auth functionality
```

## What to Contribute

### Good First Issues
- Documentation improvements
- Bug fixes
- Additional language support
- UI/UX enhancements

### Feature Requests
- Open an issue first to discuss
- Provide use case and rationale
- Consider backward compatibility

### Bug Reports
Include:
- Operating system and version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## Questions?

Open an issue for discussion before major changes.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
