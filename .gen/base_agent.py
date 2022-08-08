#!/usr/bin/env python
# coding=utf-8

import grpc
import sys
import logging
import signal
import json

from ndk import sdk_service_pb2
from ndk import sdk_service_pb2_grpc
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
        self.channel = grpc.insecure_channel("unix:///opt/srlinux/var/run/sr_sdk_service_manager:50053")

        self.sdk_mgr_client = sdk_service_pb2_grpc.SdkMgrServiceStub(self.channel)
        self.sdk_notification_client = sdk_service_pb2_grpc.SdkNotificationServiceStub(self.channel)
        
        self.sdk_telemetry_client = telemetry_service_pb2_grpc.SdkMgrTelemetryServiceStub(self.channel)
        
        self.sdk_mgr_client.AgentRegister(request=sdk_service_pb2.AgentRegistrationRequest(), metadata=self.metadata)

        request=sdk_service_pb2.NotificationRegisterRequest(op=sdk_service_pb2.NotificationRegisterRequest.Create)
        create_subscription_response = self.sdk_mgr_client.NotificationRegister(request=request, metadata=self.metadata)
        self.stream_id = create_subscription_response.stream_id

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        logging.info("Exit GreeterAgent")
        try:
            self.sdk_mgr_client.AgentUnRegister(request=sdk_service_pb2.AgentRegistrationRequest(), metadata=self.metadata)
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
        telemetry_response = self.sdk_telemetry_client.TelemetryAddOrUpdate(request=telemetry_update_request, metadata=self.metadata)
        logging.info(f"Telemetry update result: {telemetry_response.status} String: {telemetry_response.error_str}")