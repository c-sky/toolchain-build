

ENTRY(__start)

MEMORY
{
	INST   : ORIGIN = 0x00000000 , LENGTH = 0x00020000    /* ROM */
	DATA   : ORIGIN = 0x00400000 , LENGTH = 0x00004000    /* RAM */
	EEPROM : ORIGIN = 0x00600000 , LENGTH = 0x00010000
}

PROVIDE (__stack =  0x00404000 - 0x8);

SECTIONS
{
    .text : {
		. = ALIGN(0x4) ;
		*crt0.o(.exp_table)
		__stext = . ;
		*(.text)
		*(.text*)
		*(.text.*)
		*(.gnu.warning)
		*(.stub)
		*(.gnu.linkonce.t*)
		*(.glue_7t)
		*(.glue_7)
		*(.jcr)
		*(.init)
		*(.fini)
		
		/* This is special code area at the end of the normal
		   text section.  It contains a small lookup table at
		   the start followed by the code pointed to by entries
		   in the lookup table.  
		 */
		. = ALIGN (4) ;
		PROVIDE(__ctbp = .);
		*(.call_table_data)
		*(.call_table_text)
		
		. = ALIGN(0x10) ;
		__etext = . ;
    } > INST

    .rodata : {
		. = ALIGN(0x4) ;
		__srodata = .;
		*(.rdata)
		*(.rdata*)
		*(.rdata1)
		*(.rdata.*)
		*(.rodata)
		*(.rodata1)
		*(.rodata*)
		*(.rodata.*)
		*(.rodata.str1.4)
		. = ALIGN(0x10) ;
		__erodata = .;
    } > DATA

    .data : {
		. = ALIGN(0x4) ;
		__sdata = . ;
		__data_start = . ;
		data_start = . ;
		*(.got.plt)
		*(.got)
		FILL(0) ;
		. = ALIGN(0x20) ; 
		LONG(-1)
		. = ALIGN(0x20) ;
		*(.gnu.linkonce.r*)
		*(.data)
		*(.data*)
		*(.data1)
		*(.data.*)
		*(.gnu.linkonce.d*)
		*(.data1)
		*(.gcc_except_table)
		*(.gcc_except_table*)
		*(.sdata) 
		*(.sdata.*)
		*(.gnu.linkonce.s.*)
		*(__libc_atexit)
		*(__libc_subinit)
		*(__libc_subfreeres)
		*(.note.ABI-tag)
		
		. = ALIGN(0x10) ; 
		__edata = . ;
	} > DATA

    .bss : {
		. = ALIGN(0x4) ;
		__sbss = ALIGN(0x4) ;
		__bss_start = . ;
		*(.dynsbss)
		*(.sbss)
		*(.sbss.*)
		*(.scommon)
		*(.dynbss)
		*(.bss)
		*(.bss.*)
		*(COMMON)
		. = ALIGN(0x10) ;
		__ebss = . ;
		__end = . ;
		end = . ;
	} > DATA
	  
	.eh_frame           : ONLY_IF_RO { KEEP (*(.eh_frame)) } > DATA
    .gcc_except_table   : ONLY_IF_RO { *(.gcc_except_table .gcc_except_table.*) } > DATA
    .eh_frame           : ONLY_IF_RW { KEEP (*(.eh_frame)) }
    .gcc_except_table   : ONLY_IF_RW { *(.gcc_except_table .gcc_except_table.*) }
    .eh_frame_hdr       : { *(.eh_frame_hdr) }

	.preinit_array		:
	{
		PROVIDE_HIDDEN (__preinit_array_start = .);
		KEEP (*(.preinit_array))
		PROVIDE_HIDDEN (__preinit_array_end = .);
	}
	.init_array			:
	{
		PROVIDE_HIDDEN (__init_array_start = .);
		KEEP (*(SORT(.init_array.*)))
		KEEP (*(.init_array))
		PROVIDE_HIDDEN (__init_array_end = .);
	}
	.fini_array			:
	{
		PROVIDE_HIDDEN (__fini_array_start = .);
		KEEP (*(.fini_array))
		KEEP (*(SORT(.fini_array.*)))
		PROVIDE_HIDDEN (__fini_array_end = .);
	} 
	 
	.ctors :
	{
		/* gcc uses crtbegin.o to find the start of
			the constructors, so we make sure it is
			first.  Because this is a wildcard, it
			doesn't matter if the user does not
			actually link against crtbegin.o; the
			linker won't look for a file to match a
			wildcard.  The wildcard also means that it
			doesn't matter which directory crtbegin.o
			is in.  */
		KEEP (*crtbegin.o(.ctors))
		KEEP (*crtbegin?.o(.ctors))
		/* We don't want to include the .ctor section from
			the crtend.o file until after the sorted ctors.
			The .ctor section from the crtend file contains the
			end of ctors marker and it must be last */
		KEEP (*(EXCLUDE_FILE (*crtend.o *crtend?.o ) .ctors))
		KEEP (*(SORT(.ctors.*)))
		KEEP (*(.ctors))
	} > DATA
	.dtors :
	{
		KEEP (*crtbegin.o(.dtors))
		KEEP (*crtbegin?.o(.dtors))
		KEEP (*(EXCLUDE_FILE (*crtend.o *crtend?.o ) .dtors))
		KEEP (*(SORT(.dtors.*)))
		KEEP (*(.dtors))
	} > DATA

	.junk 0 : { *(.rel*) *(.rela*) }
	/* Stabs debugging sections.    */
	.stab 0 : { *(.stab) }
	.stabstr 0 : { *(.stabstr) }
	.stab.excl 0 : { *(.stab.excl) }
	.stab.exclstr 0 : { *(.stab.exclstr) }
	.stab.index 0 : { *(.stab.index) }
	.stab.indexstr 0 : { *(.stab.indexstr) }
	.comment 0 : { *(.comment) }
  /* DWARF debug sections.
     Symbols in the DWARF debugging sections are relative to the beginning
     of the section so we begin them at 0.  */
  /* DWARF 1 */
	.debug          0 : { *(.debug) }
	.line           0 : { *(.line) }
  /* GNU DWARF 1 extensions */
	.debug_srcinfo  0 : { *(.debug_srcinfo) }
	.debug_sfnames  0 : { *(.debug_sfnames) }
  /* DWARF 1.1 and DWARF 2 */
	.debug_aranges  0 : { *(.debug_aranges) }
	.debug_pubnames 0 : { *(.debug_pubnames) }
  /* DWARF 2 */
	.debug_info     0 : { *(.debug_info .gnu.linkonce.wi.*) }
	.debug_abbrev   0 : { *(.debug_abbrev) }
	.debug_line     0 : { *(.debug_line) }
	.debug_frame    0 : { *(.debug_frame) }
	.debug_str      0 : { *(.debug_str) }
	.debug_loc      0 : { *(.debug_loc) }
	.debug_macinfo  0 : { *(.debug_macinfo) }
  /* SGI/MIPS DWARF 2 extensions */
	.debug_weaknames 0 : { *(.debug_weaknames) }
	.debug_funcnames 0 : { *(.debug_funcnames) }
	.debug_typenames 0 : { *(.debug_typenames) }
	.debug_varnames  0 : { *(.debug_varnames) }
  /* DWARF 3 */
	.debug_pubtypes 0 : { *(.debug_pubtypes) }
	.debug_ranges   0 : { *(.debug_ranges) }
	.gnu.attributes 0 : { KEEP (*(.gnu.attributes)) }
	/DISCARD/ : { *(.note.GNU-stack) *(.gnu_debuglink) *(.gnu.lto_*) }
}
