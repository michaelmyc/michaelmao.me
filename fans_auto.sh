export DISPLAY=:0
export XAUTHORITY=/var/run/lightdm/root/:0

NUM_GPUS=$(nvidia-settings -q gpus | sed -n '2 p' | sed 's@^[^0-9]*\([0-9]\+\).*@\1@')
let NUM_GPUS--
for i in $(seq 0 $NUM_GPUS)
do
    nvidia-settings -a "[gpu:$i]/GPUFanControlState=0"
done
