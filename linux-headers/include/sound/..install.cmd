cmd_/lhome/quxm/trs-quxm/source/linux-headers/include/sound/.install := /bin/sh scripts/headers_install.sh /lhome/quxm/trs-quxm/source/linux-headers/include/sound ./include/uapi/sound asequencer.h asoc.h asound.h asound_fm.h compress_offload.h compress_params.h emu10k1.h firewire.h hdsp.h hdspm.h sb16_csp.h sfnt_info.h snd_sst_tokens.h tlv.h usb_stream.h; /bin/sh scripts/headers_install.sh /lhome/quxm/trs-quxm/source/linux-headers/include/sound ./include/sound ; /bin/sh scripts/headers_install.sh /lhome/quxm/trs-quxm/source/linux-headers/include/sound ./include/generated/uapi/sound ; for F in ; do echo "\#include <asm-generic/$$F>" > /lhome/quxm/trs-quxm/source/linux-headers/include/sound/$$F; done; touch /lhome/quxm/trs-quxm/source/linux-headers/include/sound/.install
