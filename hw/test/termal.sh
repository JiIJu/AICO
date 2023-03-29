sudo vim /sys/class/thermal/thermal_zone0/trip_point_4_temp
sudo sed -i 's/45000/65000/' /sys/class/thermal/thermal_zone0/trip_point_4_temp