cmd_/lhome/quxm/trs-quxm/source/linux-headers/include/linux/isdn/.install := /bin/sh scripts/headers_install.sh /lhome/quxm/trs-quxm/source/linux-headers/include/linux/isdn ./include/uapi/linux/isdn capicmd.h; /bin/sh scripts/headers_install.sh /lhome/quxm/trs-quxm/source/linux-headers/include/linux/isdn ./include/linux/isdn ; /bin/sh scripts/headers_install.sh /lhome/quxm/trs-quxm/source/linux-headers/include/linux/isdn ./include/generated/uapi/linux/isdn ; for F in ; do echo "\#include <asm-generic/$$F>" > /lhome/quxm/trs-quxm/source/linux-headers/include/linux/isdn/$$F; done; touch /lhome/quxm/trs-quxm/source/linux-headers/include/linux/isdn/.install
