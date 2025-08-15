#!/bin/bash
rm -rf output
mkdir output
rcc --binary -o output/sidebar_Example.rcc application.qrc
