# {{ getenv "APPNAME" }} agent configuration file
{{ getenv "APPNAME" }}:
  path: /usr/local/bin
  launch-command: /usr/local/bin/{{ getenv "APPNAME" }}
  search-command: python3 /opt/{{ getenv "APPNAME" }}/main.py
  yang-modules:
    names: ["{{ getenv "APPNAME" }}"]
    source-directories:
      - "/opt/{{ getenv "APPNAME" }}/yang"