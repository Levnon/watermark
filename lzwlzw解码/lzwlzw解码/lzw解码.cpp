// ConsoleApplication2.cpp: �������̨Ӧ�ó������ڵ㡣
//

#include "stdafx.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include"HXLBMPFILE.h"
#pragma warning(disable:4996)
using namespace std;
int *encode;                            //����������
BYTE*decode;                            //����������
int num = 0;
#define length 29
struct Node {
	int sign;					        //ǰ׺�ı��
	BYTE c[15];						    //��ǰ�Ҷ�BYTE����
	int n = 1;                          //��ǰ�Ҷ�BYTE�������ж��ٸ�ֵ
};
struct Node KDA[1024];                  //�ֵ�1024��


void duquKDA()//��ȡ�ֵ�
{
	FILE *fp;
	fp = fopen("my_KDA.dat", "rb");
	for (int i = 0; i < 1024; i++)
		fread(&KDA[i], sizeof(KDA[i]), 1, fp);
	fclose(fp);
}

void duquBianma()//��ȡ������
{
	FILE *fp;
	fp = fopen("cwx_encode.txt", "r");
	int i = 0;
	while (!feof(fp))
		fscanf(fp, "%d", &encode[i++]);//������ļ��е����ݷ���������
	num = i - 1;                            //nΪ���������ݸ���
	fclose(fp);
}

void jieya(int *jiemashuzu)           //�������
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

