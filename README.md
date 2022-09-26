# Greeter App

This repo provides a base agent, the Greeter app and a Makefile for setting up a Python-based [NDK](https://learn.srlinux.dev/ndk/intro/) development environment. Read more about the approach at [learn.srlinux.dev](https://learn.srlinux.dev/ndk/guide/env/python/).

## Features

The Greeter app is a demo application that shows the structure of a simple NDK agent and interacts with the state and config tree of an SR Linux container using NDK and gNMI services.

Greeter application performs the following high-level steps:

- Registers itself with the NDK service using Manager service.
- Subscribes to agent's configuration using the Config service.
- When agent's `name` is committed via configuration path `/greeter name`, the agent receives that event and updates its state using Telemetry service and provides a string `Hello {name}, my uptime is {last_booted}` at `/greeter greeting` path where `last_booted` is retrieved from the`/system/information/last-booted` state datastore using gnmi.
  
## Quickstart

You need [conatinerlab](https://containerlab.dev/install/) >= v0.31.0.

Clone the `ndk-dev-environment` project and checkout to `python` branch.

```console
git clone https://github.com/srl-labs/ndk-dev-environment.git && git checkout python
```

Initialize the NDK project:

```console
make
```

Now you have all the components of an NDK app generated.

Build the lab and deploy the demo application:

```console
make redeploy-all
```

The app named `greeter` is now running the `srl1` and `srl2` containerlab nodes. The `name` configuration parameter defined in the YANG model is available and you can explore the logs of the app by reading the log file:

```console
tail -f logs/srl1/stdout/greeter.log
```

The greeter app logs will show "greeter/name not configured" on startup so you will have to modify the `greeter/name` configuration using the SR Linux CLI.

## Modify Agent Configuration

Connect to the SR Linux CLI:

```console
ssh admin@clab-greeter-dev-srl1
```

Once connected switch to the candidate mode:

```console
enter candidate private
```

Change the configuration:

```console
set greeter name agent007
```

Commit the change:

```console
commit now
```

## App Deployment

Build a rpm file to deploy the app on hardware or vm by running this command:

 ```console
make build-app
```

The rpm file is located in /build. Copy the rpm on the SR Linux host and run:

```console
sudo rpm -U myrpm.rpm
```

The app is deployed and the last step is to reload the app-mgr by running this command in the SR Linux CLI:

```console
tools system app-management application app_mgr reload
```

## Test using Robot Framework

[Robot Framework](https://robotframework.org/) can be used to test the agent by running those commands:

### Build Robot Framework docker image

```console
make build-automated-test
```

### Test with dev lab already deployed

```console
make deploy-test-lab
```

```console
make test
```

### Test by deploying dev and test labs

```console
make redeploy_all_and_test
```
