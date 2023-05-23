SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
USER=$(whoami)

sudo su -c "$SCRIPT_DIR/pipe_listen.sh $USER" > /dev/null &
