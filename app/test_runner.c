#include <stdio.h>
#include "button.h"

int simulated_input = 1;

int getInput(int btn) {
    return simulated_input;
}

int main() {
    printf("START TEST\n");

    buttonsInitialize();

    // 1. Сначала держим RELEASE
    simulated_input = 1;
    for (int i = 0; i < 50; i++) {
        buttonHandler();
    }

    // 2. Потом PRESS
    simulated_input = 0;
    for (int i = 0; i < 50; i++) {
        buttonHandler();
    }

    // 3. Потом RELEASE
    simulated_input = 1;
    for (int i = 0; i < 50; i++) {
        buttonHandler();
    }

    printf("END TEST\n");

    return 0;
}