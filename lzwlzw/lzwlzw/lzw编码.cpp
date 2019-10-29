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

struct lzwNode {
	int sign;					        //前缀的标号
	BYTE c[15];						    //当前灰度BYTE数组
	int n = 1;                          //当前灰度BYTE数组中有多少个值
};
struct lzwNode KDA[1024];                  //字典1024项

int n = 256, P = -1, f = 0;             //n：字典目前有多少项
BYTE **shuzu;                           //待处理的灰度BYTE数组
_int16 *encode;                            //编码结果数组
int num = 0;

void Init(HXLBMPFILE*bmpfile) {
	for (int i = 0; i < 1024; i++)     //字典前缀全部初始化-1
		KDA[i].sign = -1;
	encode = (_int16*)malloc(bmpfile->imagew*bmpfile->imageh * sizeof(_int16));
	shuzu = (BYTE **)malloc(bmpfile->imagew*bmpfile->imageh * sizeof(BYTE*));
	printf("\n\n原始像素：\n");
	int t = 0;
	for (int i = 0; i < bmpfile->imagew; i++)           //把待处理的像素点存入shuzu数组
	{
		for (int j = 0; j < bmpfile->imageh; j++)
		{
			shuzu[t] = (BYTE *)malloc(15 * sizeof(BYTE));
			shuzu[t][0] = bmpfile->pDataAt(i)[j];
			printf("%d ", shuzu[t][0]);
			t++;
		}
	}
	printf("\n\n词典:\n");
	printf("串表：  码字值：\n");
	for (int i = 0; i < 256; i++)        //前256个字典由相应灰度生成
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
{//m为新的需要编码的
	if (n < 1024)
	{
		int flag = 0;//用来标识是否在字典中
		for (int i = 0; i < n; i++)
		{                                  //判断是否在字典中存在相同的串码
			if (KDA[i].n == count && bijiao(KDA[i].c, m, (KDA[i].n)) == 1)//在字典中
			{
				P = i;
				flag = 1;
				break;
			}
		}
		//如果“否”，则
		//①输出当前前缀P的码字到码字流；
			//②将P＋C添加到词典中；
			//③ 令前缀P = C(即现在的P仅包含一个字符C);
		if (flag == 0)                     //不存在则扩充字典，输出前缀相应码字并更新前缀单词
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
		else  // 如果“是”， 则用C扩展P，即让P=P＋C；                           //字典已存在则更新前缀相应码字
		{//判断输入字符流中是否还有码字要编码
			// 如果“是”，就返回到步骤2；
			//(2) 如果“否” ① 把当前前缀P的码字输出到码字流; ② 结束。
				
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
		if (KDA[i].n == count && bijiao(KDA[i].c, m, (KDA[i].n)) == 1)  //字典已存在
		{
			P = i;
			flag = 1;
			break;
		}
	}

	if (flag == 0)                 //不存在则输出前缀的
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

void Encode(HXLBMPFILE*bmpfile)                       //编码过程
{
	Init(bmpfile);
	panduan(shuzu[0], 0, 1, bmpfile);
	if (f + 1 < bmpfile->imagew*bmpfile->imageh)
		xunzhao(shuzu[f], f, 1, bmpfile);
	printf("\n编码结果为：\n");
	for (int i = 0; i < num; i++)
		printf("%d ", encode[i]);
}



void shuchuEncode()
{
	FILE *fp;
	fp = fopen("cwx_encode.txt", "w");//打开文件以便写入数据
	for (int i = 0; i < num; i++)  //准备要写入文件的数组
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

