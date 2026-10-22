#!/bin/sh
# Install the guard as a pre-commit hook for this clone. Re-run after cloning.
set -e
cd "$(dirname "$0")/.."
printf '#!/bin/sh\nexec python3 scripts/check_no_data.py\n' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
echo "pre-commit guard installed"
