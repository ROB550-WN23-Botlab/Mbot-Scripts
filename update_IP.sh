#! /usr/bin/bash
set -e

wait_for_ip() {
    echo "Waiting $TIMEOUT seconds for IP..." &>> $LOG
    count=0
    while [ -z $IP ]; do 
        if [ $count -gt $TIMEOUT ]; then
            echo "Timed out waiting for IP. Exiting." &>> $LOG
            exit 0
        fi
        sleep 1
        IP=$(hostname -I | awk '{print $1}')
        count=$((count+1))
    done
    echo "Got IP after $count seconds." &>> $LOG
}

HOSTNAME=$(hostname)
IP=$(hostname -I | awk '{print $1}')
LOG_PATH="/home/pi/startup_scripts/log"
LOG="$LOG_PATH/update_ip.log"
GIT_USER="pi"
GIT_TOKEN=$(</home/pi/startup_scripts/token.txt)
TIMEOUT=30

date > $LOG
echo "Updating IP" &>> $LOG
echo "Hostname= $HOSTNAME" &>> $LOG
if [ -z $IP ]; then 
    wait_for_ip
fi
echo "IP= $IP" &>> $LOG

cd /home/pi/startup_scripts/mbot-ip
git config --local user.email ""
git config --local user.name "pi"
#git config pull.rebase false
git pull https://$GIT_USER:$GIT_TOKEN@gitlab.eecs.umich.edu/rob550-w23/mbot-ip.git &>> $LOG

echo "Calling python script" &>> $LOG
python3 main.py -hostname $HOSTNAME -ip $IP -log $LOG
echo "Adding..." &>> $LOG
git add data/$HOSTNAME.json &>> $LOG
echo "Committing..." &>> $LOG
git commit -m "Auto update $HOSTNAME IP" &>> $LOG
echo "Pushing..." &>> $LOG
git push https://$GIT_USER:$GIT_TOKEN@gitlab.eecs.umich.edu/rob550-w23/mbot-ip.git &>> $LOG
echo "Done!" &>> $LOG
exit 0
