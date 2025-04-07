#!/bin/bash
rm -rf output
mkdir output
rcc --binary -o output/xovi_Settings_Example.rcc application.qrc
