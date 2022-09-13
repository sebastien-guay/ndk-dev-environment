from pygnmi.client import gNMIclient
from robot.api.deco import keyword

host = ("clab-{{ getenv "APPNAME" }}-dev-srl1", 57400)
cert = "/ca/srl1/srl1.pem"
enc = "json_ietf"


class srl:
    def __init__(self):
        self.gc = gNMIclient(
            target=host,
            username="admin",
            password="admin",
            insecure=False,
            debug=False,
            path_cert=cert,
        )
        self.gc.__enter__()
    
    @keyword("Start Agent")
    def start_agent(self):
        m = [("/tools/system/app-management/application[name={{ getenv "APPNAME" }}]", {"start": ""})]
        self.gc.set(update=m, encoding=enc)
    
    @keyword("Stop Agent")
    def stop_agent(self):
        m = [("/tools/system/app-management/application[name={{ getenv "APPNAME" }}]", {"stop": ""})]
        self.gc.set(update=m, encoding=enc)

    @keyword("Get Agent Status")
    def get_agent_status(self):
        result = self.gc.get(
            path=["/system/app-management/application[name={{ getenv "APPNAME" }}]/state"],
            encoding=enc,
        )
        return result["notification"][0]["update"][0]["val"]

    @keyword("Set Agent Name")
    def set_name(self, name):
        m = [("/{{ getenv "APPNAME" }}", {"name":f"{name}"})]
        self.gc.set(update=m, encoding=enc)

    @keyword("Get Greeting")
    def get_greeting(self):
        result = self.gc.get(path=["/{{ getenv "APPNAME" }}/greeting"], encoding=enc)
        print(f"result is: {result}")
        # return True
        return result["notification"][0]["update"][0]["val"]
