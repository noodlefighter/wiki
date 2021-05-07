
## ubuntu服务器开启自动更新

> via: https://www.techrepublic.com/article/how-to-enable-automatic-security-updates-for-ubuntu-server/

Log in to your Ubuntu server and install the unattended upgrade package with the command:

```
 sudo apt-get install unattended-upgrades -y
```

Once that's done, install the update-notifier-common package for automatic reboots with the command: 

```
sudo apt-get install update-notifier-common -y
```

Next, edit the 50unattended-upgrades file with the command: 

```
sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
```

By default, security updates are enabled, so you don't have to bother with that section. You might, however, want to enable automatic reboots. 

Scroll down to that section and you can define if automatic reboots are taken care of immediately or at a specific time. To enable automatic reboots, remove the leading // characters from the line Unattended-Upgrade::Automatic-Reboot "false"; and change false to true. 

You can then do the same for the Unattended-Upgrade::Automatic-Reboot "false" line and set it to the time you wish for the automatic reboot to occur (so it doesn't happen during productivity hours). 

And that's all there is to enabling automatic security updates for Ubuntu Server. Even if you don't opt to enable the automatic reboots, you should at least make sure to enable the automatic update feature and then issue the command cat /var/run/reboot-required to see if a reboot is required. If so, you'll see System Restart Required listed. Reboot your machine and enjoy those updates.