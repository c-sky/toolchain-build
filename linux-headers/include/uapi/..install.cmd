cmd_/lhome/quxm/trs-quxm/source/linux-headers/include/uapi/.install := /bin/sh scripts/headers_install.sh /lhome/quxm/trs-quxm/source/linux-headers/include/uapi ./include/uapi ; /bin/sh scripts/headers_install.sh /lhome/quxm/trs-quxm/source/linux-headers/include/uapi ./include ; /bin/sh scripts/headers_install.sh /lhome/quxm/trs-quxm/source/linux-headers/include/uapi ./include/generated/uapi ; for F in ; do echo "\#include <asm-generic/$$F>" > /lhome/quxm/trs-quxm/source/linux-headers/include/uapi/$$F; done; touch /lhome/quxm/trs-quxm/source/linux-headers/include/uapi/.install
