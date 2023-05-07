trap ctrl_c INT

function ctrl_c() {
	sudo killall memcached
	killall precise-listen
	echo "Killing Program"
	exit -1
}
#Move to correct file system and enable prereqs
. /home/pi/mycroft-precise/env/bin/activate
cd /home/pi/mycroft-precise/precise/scripts
memcached -u nobody &

killall screen
/usr/bin/screen -L -dms shifting gatttool -I -b 00:A0:50:BD:38:21 #include the address here
/usr/bin/screen -s shifting -X logfile results.txt
/usr/bin/screen -s shifting -X logfile flush 1

sleep 3

#launch models for processing audio
echo "Starting First Model"
precise-listen /home/pi/mycroft-precise/precise-data/hey-mycroft.pb -t -b &
sleep 15
echo "Starting Second Model"
precise-listen /home/pi/mycroft-precise/precise-data/christopher-precise.pb -b -s 0.75 -l 1 &

while [ true ]
do
	sleep 1
done
