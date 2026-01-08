#!/bin/bash
# Pre-publication security checklist

set -e

echo "=== Voice Cloning Project - Pre-Publish Security Check ==="
echo ""

ERRORS=0
WARNINGS=0

# 1. Check for voice samples
echo "[1/8] Checking for voice samples in git..."
if git ls-files 2>/dev/null | grep -E "\.wav$|\.mp3$" > /dev/null; then
    echo "❌ FAIL: Audio files found in git"
    git ls-files | grep -E "\.wav$|\.mp3$"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ PASS: No audio files tracked"
fi

# 2. Check for absolute paths
echo "[2/8] Checking for internal paths..."
if grep -r "/home/doge" . --exclude-dir=.git --exclude=pre-publish-check.sh 2>/dev/null | grep -v "Binary file"; then
    echo "❌ FAIL: Internal paths found"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ PASS: No internal paths"
fi

# 3. Check for .env files
echo "[3/8] Checking for .env files..."
if git ls-files 2>/dev/null | grep "\.env$" > /dev/null; then
    echo "❌ FAIL: .env file tracked"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ PASS: No .env files tracked"
fi

# 4. Check for TODO/FIXME
echo "[4/8] Checking for TODO/FIXME..."
if grep -r "FIXME\|TODO" *.py src/ scripts/ 2>/dev/null | grep -v "Binary file"; then
    echo "⚠️  WARNING: TODO/FIXME found (review before publish)"
    WARNINGS=$((WARNINGS + 1))
else
    echo "✓ PASS: No TODO/FIXME found"
fi

# 5. Check file permissions
echo "[5/8] Checking file permissions..."
bad_perms=0
if [ -d .git ]; then
    find . -name "*.py" -perm 600 2>/dev/null | grep -v venv | grep -v ".git" && bad_perms=1
    if [ $bad_perms -eq 1 ]; then
        echo "⚠️  WARNING: Some Python files have restrictive permissions"
        WARNINGS=$((WARNINGS + 1))
    else
        echo "✓ PASS: File permissions look good"
    fi
else
    echo "⚠️  WARNING: Not a git repository, skipping permission check"
fi

# 6. Verify .gitignore
echo "[6/8] Checking .gitignore coverage..."
if [ ! -f .gitignore ]; then
    echo "❌ FAIL: .gitignore missing"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ PASS: .gitignore exists"
fi

# 7. Check for large files
echo "[7/8] Checking for large files..."
if find . -type f -size +50M 2>/dev/null | grep -v ".git\|venv\|models" | grep .; then
    echo "⚠️  WARNING: Large files found (may cause GitHub issues)"
    WARNINGS=$((WARNINGS + 1))
else
    echo "✓ PASS: No large files found"
fi

# 8. Check for required files
echo "[8/8] Checking for required files..."
required_files=("LICENSE" "README.md" "SECURITY.md" ".gitignore" "Dockerfile" "requirements.txt")
missing_files=0
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ MISSING: $file"
        missing_files=$((missing_files + 1))
    fi
done

if [ $missing_files -eq 0 ]; then
    echo "✓ PASS: All required files present"
else
    echo "❌ FAIL: $missing_files required files missing"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "=== Summary ==="
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo "✅ All checks passed! Safe to publish."
    else
        echo "⚠️  Checks passed with $WARNINGS warnings. Review warnings before publishing."
    fi
    exit 0
else
    echo "❌ Found $ERRORS critical issues. Fix before publishing."
    exit 1
fi
