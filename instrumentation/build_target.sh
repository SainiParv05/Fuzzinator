#!/bin/bash
# build_target.sh
# Fuzzinator — Build all vulnerable target programs with coverage instrumentation
#
# Uses clang with:
#   -fsanitize-coverage=trace-pc  — basic block tracing via __sanitizer_cov_trace_pc
#   -fsanitize=address            — AddressSanitizer for crash detection
#
# Usage:
#   bash instrumentation/build_target.sh
#   bash instrumentation/build_target.sh target_name

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TARGET_DIR="$PROJECT_DIR/targets"
INSTR_DIR="$PROJECT_DIR/instrumentation"

# Check for clang
if ! command -v clang &> /dev/null; then
    echo "[ERROR] clang not found. Install with: sudo apt install clang"
    exit 1
fi

echo "======================================="
echo " Fuzzinator — Building Targets"
echo "======================================="
echo ""

CFLAGS="-fsanitize-coverage=trace-pc -fsanitize=address -g -O0 -fno-omit-frame-pointer"
SHM_SRC="$INSTR_DIR/shm_init.c"

# Build each target, or a single requested target
if [ $# -gt 0 ]; then
    TARGETS=("$1")
else
    TARGETS=("target_buffer_overflow" "target_format_string" "target_maze")
fi

for target in "${TARGETS[@]}"; do
    SRC="$TARGET_DIR/${target}.c"
    OUT="$TARGET_DIR/${target}"

    if [ ! -f "$SRC" ]; then
        echo "[SKIP] $SRC not found"
        continue
    fi

    echo "[BUILD] $target"
    clang $CFLAGS "$SRC" "$SHM_SRC" -o "$OUT" -lrt
    echo "  -> $OUT"
done

echo ""
echo "======================================="
echo " Build complete!"
echo "======================================="
echo ""

# Create shared memory bitmap
echo "[INIT] Creating shared memory bitmap..."
python3 -c "
import posixpath, mmap, os
SHM_PATH = '/dev/shm/fuzz_bitmap'
if not os.path.exists(SHM_PATH):
    with open(SHM_PATH, 'wb') as f:
        f.write(b'\\x00' * 65536)
    print('  -> Created /dev/shm/fuzz_bitmap (64 KB)')
else:
    print('  -> /dev/shm/fuzz_bitmap already exists')
"

# Create crashes output directory
mkdir -p "$PROJECT_DIR/data/crashes"
echo "[INIT] Created data/crashes/ directory"

echo ""
echo "Ready to fuzz! Run: python agent/train.py"
