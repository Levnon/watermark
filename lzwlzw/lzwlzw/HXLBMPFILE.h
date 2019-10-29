#pragma once

#include"stdio.h"
#include"math.h"
#include"windows.h"

#ifndef HXLBMPFILEH
#define HXLBMPFILEH

class HXLBMPFILE
{
	BYTE *Imagedata;

public:
	int imagew, imageh;
	int iYRGBnum;//1:»Ò¶È£¬3£º²ÊÉ«
	RGBQUAD palette[256];

	BYTE *pDataAt(int h, int Y0R0G1B2 = 0);
	BOOL AllocateMem();

	BOOL LoadBMPFILE(char *fname);
	BOOL SaveBMPFILE(char *fname);
	HXLBMPFILE();
	~HXLBMPFILE();


};
#endif

