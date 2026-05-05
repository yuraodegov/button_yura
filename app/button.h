#ifndef BUTTON_H
#define BUTTON_H

#include <stdint.h>

/* ===== CONFIG ===== */

#define TOTAL_INPUTS 3

#define BUTTON_1 0
#define BUTTON_2 1
#define BUTTON_3 2

/* ===== TIMING ===== */

#define BUTTON_DOUBLE_CLICK_EXPIRED 50
#define BUTTON_WAIT_FOR_RLEASE 10
#define BUTTON_LONG_CLICK_PERIOD 20

#define BUTTON_DEBOUNCE_FILTER 1

#define TIMER_TIMEOUT 1

/* ===== API ===== */

void buttonsInitialize(void);
void buttonHandler(void);

#endif