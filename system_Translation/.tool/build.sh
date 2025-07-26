#!/bin/bash
rm -rf output
mkdir output
rcc --binary -o output/system_Translation.rcc application.qrc
