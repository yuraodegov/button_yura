#ifndef TIMER_H
#define TIMER_H

#include <stdint.h>

typedef uint32_t Timer;

void timerStart(uint32_t* t);
int timerTimeOut(uint32_t* t, int period);

#endif