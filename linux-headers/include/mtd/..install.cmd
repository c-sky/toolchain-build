cmd_/lhome/quxm/trs-quxm/source/linux-headers/include/mtd/.install := /bin/sh scripts/headers_install.sh /lhome/quxm/trs-quxm/source/linux-headers/include/mtd ./include/uapi/mtd inftl-user.h mtd-abi.h mtd-user.h nftl-user.h ubi-user.h; /bin/sh scripts/headers_install.sh /lhome/quxm/trs-quxm/source/linux-headers/include/mtd ./include/mtd ; /bin/sh scripts/headers_install.sh /lhome/quxm/trs-quxm/source/linux-headers/include/mtd ./include/generated/uapi/mtd ; for F in ; do echo "\#include <asm-generic/$$F>" > /lhome/quxm/trs-quxm/source/linux-headers/include/mtd/$$F; done; touch /lhome/quxm/trs-quxm/source/linux-headers/include/mtd/.install
