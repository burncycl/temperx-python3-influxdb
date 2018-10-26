# 2018/10 BuRnCycL
# Makefile to script a bunch of manual steps. Assumption this is being built on Raspberry Pi 3 or apt package based system.

TEMPERED_LIB = TEMPered
WATCHDOG_DIR = watchdog
WATCHDOG_SCRIPT = tempMonWatchdog.sh
USR_LOCAL_SBIN = /usr/local/sbin
SCRIPT = temperatureMon.py

all: dep build


dep:
	@sudo apt install -y python3 git make cmake libhidapi-libusb0 libhidapi-dev libhidapi-hidraw0 libusb-dev libusb-1.0-0

build:
	@cd ./$(TEMPERED_LIB) && cmake CMakeLists.txt && make

install:
	@cp -R $(TEMPERED_LIB) $(USR_LOCAL_SBIN)/$(TEMPERED_LIB)
	@cp ./$(WATCHDOG_DIR)/$(WATCHDOG_SCRIPT) $(USR_LOCAL_SBIN)/$(WATCHDOG_SCRIPT)
	@cp ./$(SCRIPT) $(USR_LOCAL_SBIN)
	@chmod u+x $(USR_LOCAL_SBIN)/$(SCRIPT)
	@chmod u+X $(USR_LOCAL_SBIN)/$(WATCHDOG_SCRIPT)
	$(info Installed to ${USR_LOCAL_SBIN}/${SCRIPT})

uninstall:
	rm -rf ${USR_LOCAL_SBIN}/${SCRIPT}
	rm -rf $(USR_LOCAL_SBIN)/$(WATCHDOG_SCRIPT)
	rm -rf $(USR_LOCAL_SBIN)/$(TEMPERED_LIB)
