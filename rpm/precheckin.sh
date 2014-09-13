#!/bin/sh

cp weston.spec weston-rpi.spec
sed -i 's@Name:\s*weston$@Name: weston-rpi@g' weston-rpi.spec
