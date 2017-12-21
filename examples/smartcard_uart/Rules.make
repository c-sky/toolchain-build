DEPEND = .dep

SRS = $(wildcard *.S)
SRC = $(wildcard *.c)
OBJFILE = $(SRC:%.c=%.o) $(SRS:%.S=%.o)
#OTHEROBJFILES =

#EXTRAINCDIRS = 
#SUB_DIRS = 
#LLIBS = 
#INCLLIBS
all: subdir $(NAME).o

subdir:
	@for dir in $(SUB_DIRS); do\
		$(MAKE) -C $$dir || exit 1;\
	done

$(NAME).o : $(OBJFILE) $(SUBDIR_FILES) $(OTHEROBJFILES) $(LLIBS)
	$(LD) -r $(LDFLAGS)  -o $(NAME).o  $(OBJFILE) $(OTHEROBJFILES)\
	$(SUBDIR_FILES) $(INCLLIBS) 

%.o:%.c
	$(CC) $(CFLAGS) $(EXTRAFLAGS) $(EXTRAINCDIRS) -o $@  $< 
%.o:%.S
	$(CC) $(CFLAGS) $(EXTRAFLAGS) $(EXTRAINCDIRS) -o $@  $< 

ifneq ($(wildcard .dep),)
include $(DEPEND)
endif

dep:
	$(SHELL) -ec '$(CC) -MM $(CFLAGS) $(EXTRAINCDIRS)  $(SRC) $(SRS) \
	| sed '\''s@\(.*\)\.o[ :]@\1.o:@g'\'' > $(DEPEND)'
	@for dir in $(SUB_DIRS); do\
		$(MAKE) -C $$dir dep;\
	done	
clean:
	rm -rf  *.o
	rm -rf $(CLEANFILES)
	@for dir in $(SUB_DIRS); do\
		$(MAKE) -C $$dir clean;\
	done
.PHONY : debug-make

DEBUG_VARS =  SRS SRC OBJFILE OTHEROBJFILES SUB_DIRS SUBDIR_FILES

#:
#: debug-make -- Print a list of Makefile variables

debug-make:
	@$(foreach var, $(DEBUG_VARS), echo $(var)=$($(var)) ; )
