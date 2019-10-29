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

struct lzwNode {
	int sign;					        //ǰ׺�ı��
	BYTE c[15];						    //��ǰ�Ҷ�BYTE����
	int n = 1;                          //��ǰ�Ҷ�BYTE�������ж��ٸ�ֵ
};
struct lzwNode KDA[1024];                  //�ֵ�1024��

int n = 256, P = -1, f = 0;             //n���ֵ�Ŀǰ�ж�����
BYTE **shuzu;                           //������ĻҶ�BYTE����
_int16 *encode;                            //����������
int num = 0;

void Init(HXLBMPFILE*bmpfile) {
	for (int i = 0; i < 1024; i++)     //�ֵ�ǰ׺ȫ����ʼ��-1
		KDA[i].sign = -1;
	encode = (_int16*)malloc(bmpfile->imagew*bmpfile->imageh * sizeof(_int16));
	shuzu = (BYTE **)malloc(bmpfile->imagew*bmpfile->imageh * sizeof(BYTE*));
	printf("\n\nԭʼ���أ�\n");
	int t = 0;
	for (int i = 0; i < bmpfile->imagew; i++)           //�Ѵ���������ص����shuzu����
	{
		for (int j = 0; j < bmpfile->imageh; j++)
		{
			shuzu[t] = (BYTE *)malloc(15 * sizeof(BYTE));
			shuzu[t][0] = bmpfile->pDataAt(i)[j];
			printf("%d ", shuzu[t][0]);
			t++;
		}
	}
	printf("\n\n�ʵ�:\n");
	printf("����  ����ֵ��\n");
	for (int i = 0; i < 256; i++)        //ǰ256���ֵ�����Ӧ�Ҷ�����
	{
		KDA[i].sign = -1;
		KDA[i].c[0] = i;
		printf("%10d  %d\n", KDA[i].c[0], i);
	}
}

int bijiao(BYTE* a, BYTE* b, int n)
{
	for (int i = 0; i < n; i++)
	{
		if (a[i] != b[i])
			return 0;
	}
	return 1;
}

void panduan(BYTE *m, int t, int count, HXLBMPFILE*bmpfile)
{//mΪ�µ���Ҫ�����
	if (n < 1024)
	{
		int flag = 0;//������ʶ�Ƿ����ֵ���
		for (int i = 0; i < n; i++)
		{                                  //�ж��Ƿ����ֵ��д�����ͬ�Ĵ���
			if (KDA[i].n == count && bijiao(KDA[i].c, m, (KDA[i].n)) == 1)//���ֵ���
			{
				P = i;
				flag = 1;
				break;
			}
		}
		//������񡱣���
		//�������ǰǰ׺P�����ֵ���������
			//�ڽ�P��C��ӵ��ʵ��У�
			//�� ��ǰ׺P = C(�����ڵ�P������һ���ַ�C);
		if (flag == 0)                     //�������������ֵ䣬���ǰ׺��Ӧ���ֲ�����ǰ׺����
		{
			KDA[n].sign = P;
			KDA[n].n = count;
			for (int j = 0; j < count; j++)
				KDA[n].c[j] = m[j];
			printf("%10d\t\t", n);
			for (int j = 0; j < count; j++)
				printf("%d ", KDA[n].c[j]);
			printf("\n");
			encode[num++] = P;
			n++;
			if (t < bmpfile->imagew*bmpfile->imageh)
				panduan(shuzu[t], t, 1, bmpfile);
		}
		else  // ������ǡ��� ����C��չP������P=P��C��                           //�ֵ��Ѵ��������ǰ׺��Ӧ����
		{//�ж������ַ������Ƿ�������Ҫ����
			// ������ǡ����ͷ��ص�����2��
			//(2) ������� �� �ѵ�ǰǰ׺P�����������������; �� ������
				
			if (t + 1 < bmpfile->imagew*bmpfile->imageh)
			{
				m[KDA[P].n] = shuzu[t + 1][0];
				panduan(m, t + 1, KDA[P].n + 1, bmpfile);
			}
			else
				encode[num++] = P;
		}
	}
	if (f == 0)
		f = t;
}


void xunzhao(BYTE *m, int t, int count, HXLBMPFILE*bmpfile)
{
	int flag = 0;
	for (int i = 0; i < n; i++)
	{
		if (KDA[i].n == count && bijiao(KDA[i].c, m, (KDA[i].n)) == 1)  //�ֵ��Ѵ���
		{
			P = i;
			flag = 1;
			break;
		}
	}

	if (flag == 0)                 //�����������ǰ׺��
	{
		encode[num++] = P;
		if (t < bmpfile->imagew*bmpfile->imageh)
			xunzhao(shuzu[t], t, 1, bmpfile);
	}
	else                           
	{
		if (t + 1 < bmpfile->imagew*bmpfile->imageh)
		{
			m[KDA[P].n] = shuzu[t + 1][0];
			xunzhao(m, t + 1, KDA[P].n + 1, bmpfile);
		}
		else
			encode[num++] = P;
	}
}

void Encode(HXLBMPFILE*bmpfile)                       //�������
{
	Init(bmpfile);
	panduan(shuzu[0], 0, 1, bmpfile);
	if (f + 1 < bmpfile->imagew*bmpfile->imageh)
		xunzhao(shuzu[f], f, 1, bmpfile);
	printf("\n������Ϊ��\n");
	for (int i = 0; i < num; i++)
		printf("%d ", encode[i]);
}



void shuchuEncode()
{
	FILE *fp;
	fp = fopen("cwx_encode.txt", "w");//���ļ��Ա�д������
	for (int i = 0; i < num; i++)  //׼��Ҫд���ļ�������
	{

		fprintf(fp, "%d\n", encode[i]);
	}
	fclose(fp);
}

void shuchuKDA()
{
	FILE *fp;
	fp = fopen("my_KDA.dat", "wb");
	for (int i = 0; i < n; i++)
		//fprintf(fp, "%d\n", KDA[i].c);
		fwrite(&KDA[i], sizeof(KDA[i]), 1, fp);

	printf("\nprogram ends!\n\n");
	fclose(fp);
}

int main()
{
	char c[50] = "my.bmp";
	HXLBMPFILE bmpfile;
	if (!bmpfile.LoadBMPFILE(c))exit(0);

	Encode(&bmpfile);
	free(shuzu);
	
	shuchuEncode();
	shuchuKDA();
	return 0;
}

