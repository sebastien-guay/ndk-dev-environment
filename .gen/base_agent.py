#!/usr/bin/env python
# coding=utf-8

import grpc
import sys
import logging
import signal
import json

from ndk import sdk_service_pb2
from ndk import sdk_service_pb2_grpc
from ndk.sdk_common_pb2 import SdkMgrStatus as sdk_status
from ndk import telemetry_service_pb2_grpc
from ndk import telemetry_service_pb2


class BaseAgent(object):
    def __init__(self, name):
        self.name = name
        self.metadata = [("agent_name", self.name)]
        self.stream_id = None

        signal.signal(signal.SIGTERM, self._handle_sigterm)
        signal.signal(signal.SIGHUP, self._handle_sighup)
        signal.signal(signal.SIGQUIT, self._handle_sigquit)

    def __enter__(self):
        """Handles basic agent registration.

        - Registers the agent with the SDK Manager.
        - Registers the agent with the Telemetry Service.

        Returns:
            self

        Raises:
            Exception: If the agent registration fails.
        """
        self.channel = grpc.insecure_channel(
            "unix:///opt/srlinux/var/run/sr_sdk_service_manager:50053"
        )

        # Create  base service that defines agent registration, unregistration,
        # notification subscriptions, and keepalive messages.
        self.sdk_mgr_client = sdk_service_pb2_grpc.SdkMgrServiceStub(self.channel)
        # Create service for handling notifications.
        self.sdk_notification_client = sdk_service_pb2_grpc.SdkNotificationServiceStub(
            self.channel
        )

        # Create the telemetry service to store state data.
        self.sdk_telemetry_client = (
            telemetry_service_pb2_grpc.SdkMgrTelemetryServiceStub(self.channel)
        )

        # Register agent
        self.sdk_mgr_client.AgentRegister(
            request=sdk_service_pb2.AgentRegistrationRequest(), metadata=self.metadata
        )
        request = sdk_service_pb2.NotificationRegisterRequest(
            op=sdk_service_pb2.NotificationRegisterRequest.Create
        )
        create_subscription_response = self.sdk_mgr_client.NotificationRegister(
            request=request, metadata=self.metadata
        )
        if create_subscription_response.status == sdk_status.kSdkMgrSuccess:
            self.stream_id = create_subscription_response.stream_id
        else:
            logging.warning(f"Failed to create subscription for agent {self.name}")
            raise Exception(f"Failed to create subscription for agent {self.name}")

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Handles agent unregistration.

        Parameters:
            exc_type: Exception type.
            exc_value: Exception value.
            exc_traceback: Exception traceback.
        """
        logging.info("Exit GreeterAgent")
        try:
            self.sdk_mgr_client.AgentUnRegister(
                request=sdk_service_pb2.AgentRegistrationRequest(),
                metadata=self.metadata,
            )
        except grpc._channel._Rendezvous as err:
            logging.info(f"Error when unregistering: {err}")
        self.channel.close()

    def _handle_sigterm(self, *arg):
        logging.info("Handle SIGTERM")
        sys.exit()

    def _handle_sighup(self, *arg):
        logging.info("Handle SIGHUP")
        logging.info("Reload config not implemented")

    def _handle_sigquit(self, *arg):
        logging.info("Handle SIGQUIT")
        logging.info("Stop and dump not implemented")

    def run(self):
        logging.warning("Run() function not implemented")

    def _update_telemetry(self, js_opath, data):
        telemetry_update_request = telemetry_service_pb2.TelemetryUpdateRequest()

        telemetry_info = telemetry_update_request.state.add()
        telemetry_info.key.js_path = js_opath
        telemetry_info.data.json_content = json.dumps(data)
        telemetry_response = self.sdk_telemetry_client.TelemetryAddOrUpdate(
            request=telemetry_update_request, metadata=self.metadata
        )
        logging.info(
            f"Telemetry update result: {telemetry_response.status}"
            f" String: {telemetry_response.error_str}"
        )
