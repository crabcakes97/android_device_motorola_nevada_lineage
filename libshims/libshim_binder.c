// vndservice references Parcel::print(TextOutput&) (debug dump), whose
// TextOutput overload was removed from platform libbinder (only the ostream
// overload remains, same as stock). Stock ships the identical dangling
// reference and runs (lazy binding, never called); the stub resolves it
// everywhere and reports success if ever reached (covers void/status_t).
int _ZNK7android6Parcel5printERNS_10TextOutputEj() { return 0; }
