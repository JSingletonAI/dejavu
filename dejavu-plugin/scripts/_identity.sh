# Source this file. Sets DEJAVU_RESOLVED_USER_ID.
#
# Resolution priority:
#   1. DEJAVU_USER_ID env var (explicit override)
#   2. $USER, else "default"

_dejavu_resolve_identity() {
  if [ -n "${DEJAVU_USER_ID:-}" ]; then
    printf '%s' "$DEJAVU_USER_ID"
    return
  fi
  printf '%s' "${USER:-default}"
}

DEJAVU_RESOLVED_USER_ID="$(_dejavu_resolve_identity)"
export DEJAVU_RESOLVED_USER_ID
