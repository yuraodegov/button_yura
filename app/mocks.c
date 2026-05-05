#include <stdio.h>
#include <stdint.h>

#include "soda_dispenser.h"
#include "input_filter.h"
#include "timer.h"
#include "port.h"

// ===== MOCK TIMER =====
void timerStart(uint32_t* t) {
    *t = 0;
}

int timerTimeOut(uint32_t* t, int period) {
    (*t)++;
    return (*t > period) ? 1 : 0;   // важно: вернуть 1/0
}

// ===== MOCK FILTER =====
void initializeInputFilter(InputFilter* f, int val) {
    f->val = val;
}

void updateInputFilter(InputFilter* f, int val) {
    f->val = val;
}

int getInputFilter(InputFilter* f) {
    return getInput(0);  // напрямую берём simulated_input
}

// ===== MOCK DISPENSER =====
int getDispenserState() {
    return DISPENSER_READY;
}

void SodaCarbonate() {
    printf("SODA CARBONATE\n");
}

void SodaDispenseMs(int ms) {
    printf("DISPENSE %d\n", ms);
}

void stopSodaDispense() {
    printf("STOP DISPENSE\n");
}

// ===== MOCK LEVEL =====
void sodaLevelUpdate() {
    printf("LEVEL UPDATE\n");
}