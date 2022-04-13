/* Wiggles P0.2 at 200 Hz, after an initial 1ms wiggle */

#include "cc254x_types.h"
#include "cc254x_map.h"
#include "util.h"

int main(void) {
    init_clock();

    P0DIR |= 0x04;
    P0 ^= 0x04;
    delay_ms(1);
    P0 ^= 0x04;

    while(1) {
        delay_ms(5);
        P0 ^= 0x04;
    }
}
