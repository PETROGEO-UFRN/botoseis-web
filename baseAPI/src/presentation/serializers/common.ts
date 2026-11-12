// *** Dates are sent as RFC 1123 strings in GMT, like Flask's jsonify
export function toHttpDate(date: Date | null): string | null {
  return date ? date.toUTCString() : null
}
