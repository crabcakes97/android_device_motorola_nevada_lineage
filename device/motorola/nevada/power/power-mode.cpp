/*
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

#include <aidl/android/hardware/power/BnPower.h>

#include <android-base/file.h>
#include <android-base/logging.h>

using ::aidl::android::hardware::power::Mode;

namespace aidl::google::hardware::power::impl::pixel {

bool isDeviceSpecificModeSupported(Mode type, bool* _aidl_return) {
    switch (type) {
        case Mode::DOUBLE_TAP_TO_WAKE:
            *_aidl_return = true;
            return true;
        default:
            return false;
    }
}

bool setDeviceSpecificMode(Mode type, bool enabled) {
    switch (type) {
        case Mode::DOUBLE_TAP_TO_WAKE: {
            LOG(INFO) << "Power mode: " << toString(type) << " isDoubleTapEnabled: " << enabled;

            ::android::base::WriteStringToFile(enabled ? "49" : "48", "/sys/devices/virtual/touchscreen/primary/gesture");

            return true;
        }
        default:
            return false;
    }
}

}  // namespace
