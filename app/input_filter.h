#ifndef INPUT_FILTER_H
#define INPUT_FILTER_H

typedef struct {
    int val;
} InputFilter;

void initializeInputFilter(InputFilter* f, int val);
void updateInputFilter(InputFilter* f, int val);
int getInputFilter(InputFilter* f);

#endif