#include <stdio.h>
#include "button.h"

int simulated_input = 0;

// mock GPIO input
int getInput(int btn)
{
    return simulated_input;
}

int main()
{
    printf("START TEST\n");

    buttonsInitialize();

    // =========================
    // FIRST CLICK
    // =========================

    simulated_input = 1;

    for (int i = 0; i < 20; i++)
    {
        buttonHandler();
    }

    simulated_input = 0;

    for (int i = 0; i < 5; i++)
    {
        buttonHandler();
    }

    // =========================
    // SECOND CLICK
    // =========================

    simulated_input = 1;

    for (int i = 0; i < 20; i++)
    {
        buttonHandler();
    }

    simulated_input = 0;

    for (int i = 0; i < 20; i++)
    {
        buttonHandler();
    }

    // =========================
    // WAIT FOR FSM
    // =========================

    for (int i = 0; i < 50; i++)
    {
        buttonHandler();
    }

    printf("END TEST\n");

    return 0;
}