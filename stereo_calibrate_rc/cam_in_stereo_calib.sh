#!/usr/bin/env bash

c_lred=91
c_lgreen=92
c_dflt=0
data_folder=data/

cleanup() {
    exit 0
}
trap cleanup 0 1 2 3 15

take_images() {
    local cam_left="$1"
    local cam_right="$2"
    python cam_in.py $cam_left $cam_right
    return $?
}

images_available_for_calib() {
    total_images=$(ls -l ${data_folder} |wc -l)
    return ${total_images}
}
calib_cam() {
    ./stereo_calib
    return $?
}

print_help() {
  echo '************************************************************'
  echo 'Usage: '
  echo './cam_in_stereo_calib.sh <Index:cam_left> <Index:cam_right>'
  echo '************************************************************'
}

########
# Main #
########

# Take indexes of both stereo cameras as user input
cam_left="$1"
cam_right="$2"

# Return error if user input not detected
if [ "$cam_left" == "" ]; then
  print_help
  exit 1
fi
if [ "$cam_right" == "" ]; then
  print_help
  exit 1
fi
#
# Capture images from both the stereo cameras
#
take_images $cam_left $cam_right
rc=$?
if [ $rc -ne 0 ]; then
    echo -e "\e[${c_lred}mTaking pictures failed\e[${c_dflt}m"
    exit 1
fi

images_available_for_calib
total_images=$?
if [ $total_images -lt 40 ]; then
    echo -e "\e[${c_lred}mNot enough images for calibration \e[${c_dflt}m"
    exit 1
fi

calib_cam
rc=$?
if [ $rc -ne 0 ]; then
    echo -e "\e[${c_lred}mStereo calibration failed\e[${c_dflt}m"
    exit 1
fi

echo -e "\e[${c_lgreen}mStereo calibration  successful\e[${c_dflt}m"

exit 0
