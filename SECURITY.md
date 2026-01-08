# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **Do NOT** open a public issue
2. Email details to: [Create an issue on GitHub with "SECURITY" tag]
3. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours.

## Security Best Practices

### For Users

- Keep dependencies updated
- Use authentication in production
- Don't expose web UI to public internet without reverse proxy
- Validate all voice sample sources
- Use strong passwords if enabling auth

### For Contributors

- Run security scanners before PR
- Never commit secrets or credentials
- Use path validation for file operations
- Sanitize user inputs
- Follow principle of least privilege

## Known Security Considerations

- Voice cloning can be misused for impersonation
- Web UI has no built-in authentication by default
- Generated audio files should be handled responsibly
- Model downloads from internet (verify source)

## Security Features

This project implements:
- Path traversal protection for file operations
- Input validation (max text length: 10,000 chars)
- Non-root Docker container user
- Optional Gradio authentication
- Network binding warnings

## Security Scanning

For maintainers:
- Use Trivy for container scanning
- Check dependencies with `pip-audit`
- Review code with security linters

## Responsible Disclosure

We appreciate responsible disclosure of security issues. We will:
- Acknowledge your report within 48 hours
- Provide regular updates on progress
- Credit you in security advisories (unless you prefer anonymity)
- Work with you to understand and fix the issue
