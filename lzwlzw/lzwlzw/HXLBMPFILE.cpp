#include"stdafx.h"
#include"HXLBMPFILE.h"
#pragma warning(disable:4996)
HXLBMPFILE::HXLBMPFILE()
{
	Imagedata = NULL;
	for (int i = 0; i < 256; i++)
	{
		palette[i].rgbBlue = palette[i].rgbGreen = palette[i].rgbRed = i;
		/*if (i >= 0 && i <= 63)
		{
		palette[i].rgbBlue = 255;
		palette[i].rgbGreen = 254 - 4 * i;
		palette[i].rgbRed = 0;
		}
		if (i >= 64 && i <= 127)
		{
		palette[i].rgbBlue = 510 - 4 * i;
		palette[i].rgbGreen = 4 * i - 254;
		palette[i].rgbRed = 0;
		}
		if (i >= 128 && i <= 191)
		{
		palette[i].rgbBlue = 0;
		palette[i].rgbGreen = 255;
		palette[i].rgbRed = 4 * i - 510;
		}
		if (i >= 192 && i <= 255)
		{
		palette[i].rgbBlue = 0;
		palette[i].rgbGreen = 1022 - 4 * i;
		palette[i].rgbRed = 255;
		}*/ //�Ҷ�ͼ��Ϊ��ɫͼ

		palette[i].rgbReserved = 0;
	}

	iYRGBnum = 0;
	imagew = imageh = 0;
}
HXLBMPFILE::~HXLBMPFILE()
{
	if (Imagedata)delete[]Imagedata;
}

BYTE *HXLBMPFILE::pDataAt(int h, int Y0R0G1B2)
{
	if (iYRGBnum <= Y0R0G1B2)return NULL;

	int w = imagew * h + Y0R0G1B2 * imagew*imageh;

	return Imagedata + w;
}

BOOL HXLBMPFILE::AllocateMem()
{
	int w = imagew * imageh*iYRGBnum;

	if (Imagedata)
	{
		delete[]Imagedata; Imagedata = NULL;
	}

	Imagedata = new BYTE[w];

	if (Imagedata) memset(Imagedata, 0, w);
	return(Imagedata != NULL);
}

BOOL HXLBMPFILE::LoadBMPFILE(char*cFilename)
{
	FILE *f;
	if (strlen(cFilename) < 1)return FALSE;

	f = fopen(cFilename, "r+b");
	if (f == NULL)return FALSE;

	BITMAPFILEHEADER fh;
	BITMAPINFOHEADER ih;

	fread(&fh, sizeof(BITMAPFILEHEADER), 1, f);
	if (fh.bfType != 0x4d42) { fclose(f); return FALSE; }//"BM

	fread(&ih, sizeof(BITMAPINFOHEADER), 1, f);
	if ((ih.biBitCount != 8) && (ih.biBitCount != 24))
	{
		fclose(f);
		return FALSE;
	}

	iYRGBnum = ih.biBitCount / 8;
	imagew = ih.biWidth;
	imageh = ih.biHeight;

	if (!AllocateMem()) { fclose(f); return FALSE; }

	if (iYRGBnum == 1)fread(palette, sizeof(RGBQUAD), 256, f);
	fseek(f, fh.bfOffBits, SEEK_SET);
	int w4b = (imagew*iYRGBnum + 3) / 4 * 4, i, j;
	BYTE *ptr;

	ptr = new BYTE[w4b];
	if (iYRGBnum == 1)
	{
		for (i = imageh - 1; i >= 0; i--)
		{
			fread(ptr, w4b, 1, f);
			memmove(pDataAt(i), ptr, imagew);
		}
	}
	if (iYRGBnum == 3)
	{
		for (i = imageh - 1; i >= 0; i--)
		{
			fread(ptr, w4b, 1, f);
			for (j = 0; j < imagew; j++)
			{
				*(pDataAt(i, 0) + j) = *(ptr + j * 3 + 2);
				*(pDataAt(i, 1) + j) = *(ptr + j * 3 + 1);
				*(pDataAt(i, 2) + j) = *(ptr + j * 3 + 0);
			}
		}
	}
	delete[]ptr;
	fclose(f);
	return TRUE;

}
BOOL HXLBMPFILE::SaveBMPFILE(char*cFilename)
{
	if (!Imagedata)return FALSE;
	FILE *f;
	if (strlen(cFilename) < 1)return FALSE;
	f = fopen(cFilename, "w+b"); if (f == NULL)return FALSE;

	BITMAPFILEHEADER fh; BITMAPINFOHEADER ih;
	memset(&ih, 0, sizeof(BITMAPINFOHEADER));

	fh.bfType = 0x4d42;
	fh.bfReserved1 = fh.bfReserved2 = 0;
	fh.bfOffBits = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) + ((iYRGBnum == 1) ? 256 * sizeof(RGBQUAD) : 0);
	ih.biSize = 40; ih.biPlanes = 1;
	ih.biWidth = imagew; ih.biHeight = imageh;
	ih.biBitCount = 8 * iYRGBnum;

	int w4b = (imagew*iYRGBnum + 3) / 4 * 4;
	ih.biSizeImage = ih.biHeight*w4b;
	fh.bfSize = fh.bfOffBits + ih.biSizeImage;

	fwrite(&fh, sizeof(BITMAPFILEHEADER), 1, f);
	fwrite(&ih, sizeof(BITMAPINFOHEADER), 1, f);
	if (iYRGBnum == 1)fwrite(palette, sizeof(RGBQUAD), 256, f);

	BYTE* ptr; int i, j;
	ptr = new BYTE[w4b];
	memset(ptr, 0, w4b);
	if (iYRGBnum == 1)
	{
		for (i = ih.biHeight - 1; i >= 0; i--)
		{
			memmove(ptr, pDataAt(i), ih.biWidth);
			fwrite(ptr, w4b, 1, f);
		}
	}
	if (iYRGBnum == 3)
	{
		for (i = ih.biHeight - 1; i >= 0; i--)
		{
			for (j = 0; j < ih.biWidth; j++)
			{
				*(ptr + j * 3 + 0) = *(pDataAt(i, 2) + j);
				*(ptr + j * 3 + 1) = *(pDataAt(i, 1) + j);
				*(ptr + j * 3 + 2) = *(pDataAt(i, 0) + j);
			}
			fwrite(ptr, w4b, 1, f);
		}
	}
	delete[]ptr;
	fclose(f);
	return TRUE;
}