#include "nrf_delay.h"
#include "nrf_gpio.h"

#define PIN 6

int main(void)
{
    nrf_gpio_cfg_output(PIN); // Configure pin as output

    nrf_gpio_pin_toggle(PIN);
    nrf_delay_ms(1);
    nrf_gpio_pin_toggle(PIN);

    while(1) {
        nrf_delay_ms(5);
        nrf_gpio_pin_toggle(PIN);
    }
}
