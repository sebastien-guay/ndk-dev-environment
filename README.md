## Greeter App
This repo provides a base agent, the Greeter app and a Makefile for setting up a python based [NDK](https://learn.srlinux.dev/ndk/intro/) development environment. Read more about the approach at [learn.srlinux.dev](https://learn.srlinux.dev/ndk/guide/env/python/).

### Features
The Greeter app demonstrates how agent can interact with the whole state and config tree of SR Linux using local gNMI access and the NDK.
- It subscribes to configuration using the NDK.
- It retrieves the "name" from the configuration notification and update the uptime status with a hardcoded value of 8:00 using a telemetry client.
- It gets the uptime using gNMI. The gNMI client is locally connecting using Unix Domain Socket.
- It logs "Hello myname, my uptime is 8:00"​. 

### Quickstart
Clone the `greeter-app-python` branch.

Initialize the NDK project:

```
make
```

Now you have all the components of an NDK app generated.

Build the lab and deploy the demo application:

```
make redeploy-all
```

The app named `greeter` is now running on `srl1`. The 'name' configuration parameter defined in the YANG model is available and you can explore the logs of the app by reading the log file:

```
tail -f logs/srl1/stdout/greeter.log
```

The greeter app logs will show "greeter/name not configured" on startup so you will have to modify the "greeter/name configuration using the SR Linux CLI. 

### Modify App configuration
Connect to the SR Linux CLI:
```
ssh admin@clab-greeter-dev-srl1
```
Once connected switch to the candiate mode:
```
enter candidate private
```

Change the configuration:
```
set greeter name myname
```

Commit the change:
```
commit now
```

The greeter log will show this log:

"hello myname, my uptime is 8:00"