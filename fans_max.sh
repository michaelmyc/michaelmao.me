export DISPLAY=:0
export XAUTHORITY=/var/run/lightdm/root/:0

NUM_FANS=$(nvidia-settings -q fans | sed -n '2 p' | sed 's@^[^0-9]*\([0-9]\+\).*@\1@')
let NUM_FANS--
for i in $(seq 0 $NUM_FANS)
do
    nvidia-settings -a "[fan:$i]/GPUTargetFanSpeed=100"
done
