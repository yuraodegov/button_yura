#include <stdio.h>
#include "button.h"

int simulated_input = 0;

int getInput(int btn)
{
    return simulated_input;
}

int main()
{
    printf("START TEST\n");

    buttonsInitialize();

    // PRESS
    simulated_input = 1;

    for (int i = 0; i < 50; i++)
    {
        buttonHandler();
    }

    // RELEASE
    simulated_input = 0;

    for (int i = 0; i < 50; i++)
    {
        buttonHandler();
    }

    printf("END TEST\n");

    return 0;
}