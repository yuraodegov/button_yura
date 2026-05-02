#include <stdio.h>
#include <time.h>

#define LONG_PRESS_THRESHOLD 1.0
#define DOUBLE_CLICK_WINDOW 0.5

#typedef enum {
    IDLE,
    PRESSED
} State;

typedef struct {
    State state;
    double press_time;
    double last_release_time;
} Button;

double now() {
    return (double)clock() / CLOCKS_PER_SEC;
}

void init_button(Button* btn) {
    btn->state = IDLE;
    btn->press_time = 0;
    btn->last_release_time = 0;
}

void handle_event(Button* btn, const char* action) {
    double t = now();

    if (strcmp(action, "press") == 0) {
        btn->state = PRESSED;
        btn->press_time = t;
        printf("PRESS\n");
        return;
    }

    if (strcmp(action, "release") == 0) {
        if (btn->state != PRESSED) {
            printf("ERROR: invalid state\n");
            return;
        }

        double duration = t - btn->press_time;
        btn->state = IDLE;

        if (duration >= LONG_PRESS_THRESHOLD) {
            printf("LONG_CLICK (%.2f sec)\n", duration);
            return;
        }

        if ((t - btn->last_release_time) <= DOUBLE_CLICK_WINDOW) {
            btn->last_release_time = 0;
            printf("DOUBLE_CLICK\n");
            return;
        }

        btn->last_release_time = t;
        printf("SHORT_CLICK (%.2f sec)\n", duration);
    }
}