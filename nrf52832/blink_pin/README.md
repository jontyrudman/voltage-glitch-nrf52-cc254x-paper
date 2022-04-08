# Blink Pin

## Compiling

1. Download the [GNU Arm Embedded Toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads) (you'll need `arm-none-eabi-gcc`).
2. Download and extract the [nRF5 SDK](https://www.nordicsemi.com/Products/Development-software/nRF5-SDK/Download).
3. Modify the `GNU_INSTALL_ROOT` line in `nRF5_SDK_x_x/components/toolchain/gcc/Makefile.posix` to point to the directory containing `arm-none-eabi-gcc`.
4. Place the `blink_pin` directory in the extracted `nRF5_SDK_x_x` directory.
5. Navigate to `nRF5_SDK_x_x/blink_pin/nrf52832_armgcc_nobl` and run `make`.

## Flashing

Assumes that you're using OpenOCD with an ST-LINK V2 and are in the directory from step 5 of "Compiling".

Run:

```
openocd -f interface/stlink.cfg -f target/nrf52.cfg -c 'init;halt;nrf51 mass_erase;program _build/blink_pin_nrf52832.hex verify reset;exit'
```
