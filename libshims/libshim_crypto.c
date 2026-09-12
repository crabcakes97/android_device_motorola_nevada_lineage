#include <openssl/stack.h>

// Stock hs20-osu-client was built against OpenSSL 1.0-era BoringSSL and calls
// sk_dup(), which platform BoringSSL renamed to OPENSSL_sk_dup(). Same
// semantics; forward to the rename. (CBS_init() comes from libcrypto_shim.)
OPENSSL_STACK *sk_dup(const OPENSSL_STACK *sk) {
    return OPENSSL_sk_dup(sk);
}
