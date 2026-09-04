#!/usr/bin/env bash
# Build a native Ruby gem extension on this Windows box.
#
# Two defects in the generated Makefiles break stock `gem install` here:
#   1. Ruby emits MSYS-mangled include paths (/C/Ruby34-x64/...) that native
#      gcc cannot resolve -> "ruby.h: No such file or directory".
#   2. gcc tries to write scratch files into C:\Windows -> permission denied.
#
# This script installs the gem with --ignore-dependencies, repairs the
# generated Makefile (correct topdir/hdrdir + writable TMPDIR), and runs make.
#
# Usage: build_native_gem.sh <gem-name> <gem-version>
set -euo pipefail

GEM="$1"
VER="$2"

export PATH="/c/Ruby34-x64/bin:/c/Ruby34-x64/msys64/ucrt64/bin:/c/Ruby34-x64/msys64/usr/bin:$PATH"
BUILD_TMP="C:/Users/jonna/AppData/Local/Temp/rbuild"
mkdir -p "$BUILD_TMP"
export TMPDIR="$BUILD_TMP" TMP="$BUILD_TMP" TEMP="$BUILD_TMP"

HDR="C:/Ruby34-x64/include/ruby-3.4.0"
ARCHHDR="$HDR/x64-mingw-ucrt"
GEMROOT="C:/Ruby34-x64/lib/ruby/gems/3.4.0/gems/${GEM}-${VER}"

# 1. Install without dependencies (extracts source, skips the broken build).
gem.cmd install "$GEM" -v "$VER" --no-document --ignore-dependencies 2>&1 | tail -3

# 2. Patch every generated Makefile with real Windows include paths.
find "$GEMROOT" -name Makefile -print0 | while IFS= read -r -d '' mk; do
  sed -i "s|^topdir = .*|topdir = $HDR|" "$mk"
  sed -i "s|^hdrdir = .*|hdrdir = $HDR|" "$mk"
  sed -i "s|^arch_hdrdir = .*|arch_hdrdir = $ARCHHDR|" "$mk"
  sed -i "s|^VPATH = .*|VPATH = .|" "$mk"
done

# 3. Run make in each extension dir, then stage the .so.
find "$GEMROOT/ext" -name Makefile -print0 2>/dev/null | while IFS= read -r -d '' mk; do
  d=$(dirname "$mk")
  echo "--- building $d"
  (cd "$d" && make 2>&1 | tail -5)
done

# 4. Copy built artifacts into the gem's lib dir so `require` finds them.
find "$GEMROOT/ext" -name '*.so' -print0 2>/dev/null | while IFS= read -r -d '' so; do
  lib="$GEMROOT/lib"
  mkdir -p "$lib"
  cp "$so" "$lib/"
  echo "staged: $so -> $lib/"
done

# 5. Also stage into the extensions dir if make already handled install.
find "$GEMROOT/ext" -name '*.so' 2>/dev/null | head -5

echo "DONE: $GEM $VER"
