#ifndef SODA_DISPENSER_H
#define SODA_DISPENSER_H

#define DISPENSER_READY 0
#define DISPENSER_FILL_WATER_FULL 1

int getDispenserState();
void SodaCarbonate();
void SodaDispenseMs(int ms);
void stopSodaDispense();

#endif