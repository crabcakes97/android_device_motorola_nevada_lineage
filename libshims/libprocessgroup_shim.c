// Provides SetTaskProfiles(), removed from libprocessgroup, which the
// stock camera HAL (vendor/lib64/mt6835/libcam.hal3a.v3.so) still references.
// Plain C linkage matches the blob's undefined symbol exactly; on AArch64
// all arguments arrive in registers so any prototype shape is ABI-safe.
int SetTaskProfiles(int tid, const char **profiles, int use_fd) {
    (void)tid;
    (void)profiles;
    (void)use_fd;
    return 0;
}
