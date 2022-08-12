name: "{{ getenv "APPNAME" }}-test"

topology:
  nodes:
    test1:
      kind: linux
      image: {{ getenv "APPNAME" }}-tests
      binds:
        - "../:/mnt"
        - "../../lab/clab-{{ getenv "APPNAME" }}-dev/ca:/ca"