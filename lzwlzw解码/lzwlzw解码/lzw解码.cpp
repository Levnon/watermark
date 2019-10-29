// ConsoleApplication2.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include"HXLBMPFILE.h"
#pragma warning(disable:4996)
using namespace std;
int *encode;                            //编码结果数组
BYTE*decode;                            //解码结果数组
int num = 0;
#define length 29
struct Node {
	int sign;					        //前缀的标号
	BYTE c[15];						    //当前灰度BYTE数组
	int n = 1;                          //当前灰度BYTE数组中有多少个值
};
struct Node KDA[1024];                  //字典1024项


void duquKDA()//读取字典
{
	FILE *fp;
	fp = fopen("my_KDA.dat", "rb");
	for (int i = 0; i < 1024; i++)
		fread(&KDA[i], sizeof(KDA[i]), 1, fp);
	fclose(fp);
}

void duquBianma()//读取编码结果
{
	FILE *fp;
	fp = fopen("cwx_encode.txt", "r");
	int i = 0;
	while (!feof(fp))
		fscanf(fp, "%d", &encode[i++]);//逐个将文件中的数据放入数组中
	num = i - 1;                            //n为数组中数据个数
	fclose(fp);
}

void jieya(int *jiemashuzu)           //解码过程
{
	
	int t = 0;
	for (int i = 0; i < num; i++)
	{
		for (int j = 0; j < KDA[jiemashuzu[i]].n; j++)
		{
			printf("%d ", KDA[jiemashuzu[i]].c[j]);
			decode[t] = KDA[jiemashuzu[i]].c[j];
			t++;
		}
	}
}

void shuchutupian()
{
	HXLBMPFILE bf;
	bf.imagew = length;
	bf.imageh = length;
	bf.iYRGBnum = 1;
	bf.AllocateMem();
	int t = 0;
	for (int i = 0; i < length; i++)
	{
		for (int j = 0; j < length; j++)
			bf.pDataAt(i)[j] = decode[t++];
	}
	char p[100] = "new.bmp";
	bf.SaveBMPFILE(p);
	printf("\n\nprogram ends!\n\n");
}

int main()
{
	encode = (int*)malloc(length *length * sizeof(int));
	decode = (BYTE*)malloc(length *length * sizeof(BYTE));
	duquKDA();
	duquBianma();
	jieya(encode);
	shuchutupian();
	return 0;
}

