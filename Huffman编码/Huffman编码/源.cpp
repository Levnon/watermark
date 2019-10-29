#include <iostream>

/* run this program using the console pauser or add your own getch, system("pause") or input loop */
#include<stdio.h>
#include<math.h>
#include<windows.h>


struct HuffNode {
	int myparents;//�ڵ��Ӧ�ĸ��׽ڵ��±�
	int lchild, rchild;//�ڵ��Ӧ�������ӽڵ�
	char bits[256];//�ڵ��Ӧ�Ĺ�������������
	unsigned char b;//�ֽ�ֵ
	int pinlv;//�ֽڳ���Ƶ��
}HuffTreeNode[1024];//.Huffman������

void ccccreate(HuffNode a[], int n, int m)
{
	int i, j;
	int min, ptr = 1000;
	for (i = n; i < m; i++)//�������������ĺ�n-1�����
	{
		min = 66666666;//Ԥ������Ȩֵ���������ֵ�������
		for (j = 0; j < i; j++)
		{
			if (HuffTreeNode[j].myparents != -1)
				continue;
			if (min > HuffTreeNode[j].pinlv)
			{
				ptr = j;
				min = HuffTreeNode[j].pinlv;
				continue;
			}
		}
		HuffTreeNode[i].pinlv = HuffTreeNode[ptr].pinlv;
		HuffTreeNode[ptr].myparents = i;//�ҵ�����
		HuffTreeNode[i].lchild = ptr;//����Ȩֵ
		min = 66666666;
		for (j = 0; j < i; j++)
		{
			if (HuffTreeNode[j].myparents != -1)
				continue;
			if (min > HuffTreeNode[j].pinlv)
			{
				ptr = j;
				min = HuffTreeNode[j].pinlv;
				continue;
			}
		}
		HuffTreeNode[i].pinlv += HuffTreeNode[ptr].pinlv;
		HuffTreeNode[i].rchild = ptr;
		HuffTreeNode[ptr].myparents = i;
	}

}

void yayasuo()
{
	FILE *myfile1, *myfile2;
	char *filename;
	filename = new char[255];
	myfile1 = fopen("1.bmp", "rb");
	if (myfile1 == NULL)
	{
		system("pause");
		return;
	}
	unsigned char c;	int filelen = 0;
	while (!feof(myfile1))
	{
		fread(&c, 1, 1, myfile1);
		HuffTreeNode[c].pinlv++;
		filelen++;
	}
	filelen--;	int length1 = filelen;
	HuffTreeNode[c].pinlv--;
	for (int i = 0; i < 512; i++)
	{
		if (HuffTreeNode[i].pinlv != 0) {
			HuffTreeNode[i].b = (char)i;//ǿ������ת��
		}
		else
		{
			HuffTreeNode[i].b = 0;
		}
		HuffTreeNode[i].myparents = -1;
		HuffTreeNode[i].lchild = HuffTreeNode[i].rchild = -1;
	}
	HuffNode tttt;
	int s;
	int j, q;
	for (q = 0; q <= 255; ++q)
	{
		s = q;
		for (j = q + 1; j <= 256; ++j)
			if (HuffTreeNode[j].pinlv > HuffTreeNode[s].pinlv)
				s = j;
		if (s != q)
		{
			tttt = HuffTreeNode[q];
			HuffTreeNode[q] = HuffTreeNode[s];
			HuffTreeNode[s] = tttt;
		}
	}
	int i, n, m;
	for (i = 0; i < 256; i++)
		if (HuffTreeNode[i].pinlv == 0)
			break;//һ������ȨֵΪ0�����涼Ϊ0
	n = i;
	m = 2 * n - 1;
	ccccreate(HuffTreeNode, n, m);
	int bian;
	for (i = 0; i < n; i++)//Ϊÿһ��Ҷ�ӽ�����
	{
		bian = i;
		HuffTreeNode[i].bits[0] = 0;
		while (HuffTreeNode[bian].myparents != -1)
		{
			j = bian;
			bian = HuffTreeNode[bian].myparents;
			if (HuffTreeNode[bian].lchild == j) {
				j = strlen(HuffTreeNode[i].bits);
				memmove(HuffTreeNode[i].bits + 1, HuffTreeNode[i].bits, j + 1);
				HuffTreeNode[i].bits[0] = '0';
			}
			else
			{
				j = strlen(HuffTreeNode[i].bits);
				memmove(HuffTreeNode[i].bits + 1, HuffTreeNode[i].bits, j + 1);
				HuffTreeNode[i].bits[0] = '1';
			}
		}
	}
	myfile2 = fopen("cwx.txt", "wb");//���ļ�����д��
	if (myfile2 == NULL)
	{
		system("pause");
	}
	fseek(myfile1, 0, SEEK_SET);
	fwrite(&filelen, sizeof(int), 1, myfile2);
	fseek(myfile2, 8, SEEK_SET);
	char buffer[512];
	buffer[0] = 0;
	int xin = 0;
	int ptr = 8;
	while (!feof(myfile1))
	{
		c = fgetc(myfile1);
		bian ++;
		for (i = 0; i < n; i++)
		{
			if (c == HuffTreeNode[i].b)
				break;
		}
		strcat(buffer, HuffTreeNode[i].bits);
		j = strlen(buffer);
		c = 0;
		while (j >= 8)
		{
			for (i = 0; i < 8; i++)
			{
				if (buffer[i] == '1')
					c = (c << 1) | 1;
				else
					c = c << 1;
			}
			fwrite(&c, 1, 1, myfile2);
			ptr++;
			strcpy(buffer, buffer + 8);
			j = strlen(buffer);
		}
		if (bian == filelen)
			break;
	}
	if (j > 0)
	{
		strcat(buffer, "00000000");
		for (i = 0; i < 8; i++)
		{
			if (buffer[i] == '1')
				c = (c << 1) | 1;
			else
				c = c << 1;
		}
		fwrite(&c, 1, 1, myfile2);
		ptr++;
	}
	fseek(myfile2, 4, SEEK_SET);
	fwrite(&ptr, sizeof(int), 1, myfile2);
	fseek(myfile2, ptr, SEEK_SET);
	fwrite(&n, sizeof(int), 1, myfile2);
	for (i = 0; i < n; i++)
	{
		fwrite(&(HuffTreeNode[i].b), 1, 1, myfile2);
		c = strlen(HuffTreeNode[i].bits);
		fwrite(&c, 1, 1, myfile2);
		j = strlen(HuffTreeNode[i].bits);
		if (j % 8 != 0)
		{
			for (xin = j % 8; xin < 8; xin++)
				strcat(HuffTreeNode[i].bits, "0");//011 00000
		}
		while (HuffTreeNode[i].bits[0] != 0)
		{
			c = 0;
			for (j = 0; j < 8; j++)
			{
				if (HuffTreeNode[i].bits[j] == '1')
					c = (c << 1) | 1;
				else
					c = c << 1;
			}
			strcpy(HuffTreeNode[i].bits, HuffTreeNode[i].bits + 8);
			fwrite(&c, 1, 1, myfile2);
		}
	}
	int length2 = ptr--;
	double div = ((double)length1 - (double)length2) / (double)length1;	fclose(myfile1);
	fclose(myfile2);
}


	int main()
	
	{
		  
			yayasuo();
		
}	