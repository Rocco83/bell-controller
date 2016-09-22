# Bell controller and power management for amplifier of a church

This is the original definition of the HW+SW project.

The raspberry should be turned on 24 hours a day.

## Automatic handling of bell controller

When the cron is reached to run one audio

1. Turn on the relais to turn on the amplifier or what is needed
2. Run the sound
3. Turn off the relais and shutdown the amplifier or what is needed

WARNING: during the automatic cycle the manual way should be disabled.

## Manual handling of bell controller

When needed outside of cron

1. Turn on the amplifier or what is needed. This emulate the automatic turn on.
2. Press the button, that will play the sound
3. Turn off the amplifier or what has been manually turned on

WARNING: during the manual cycle the automatic cycle should be disabled.
