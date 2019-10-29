#include <iostream>

/* run this program using the console pauser or add your own getch, system("pause") or input loop */
#include<stdio.h>
#include<math.h>
#include<windows.h>

struct HuffNode {
	unsigned char b;//�ֽ�ֵ
	int count;//�ֽڳ���Ƶ��
	long parent;//�ڵ��Ӧ�ĸ��׽ڵ��±�
	long lch, rch;//�ڵ��Ӧ�������ӽڵ�
	char bits[256];//�ڵ��Ӧ�Ĺ�������������
}HuffTreeNode[512];//.Huffman���Ĵ洢�ṹ����




void jieyasuo()
{


	char buf[512];//���建�����������ֽڵ�huffman����
	buf[0] = 0;//��ʼΪ'\0'
	char filename[255], outputfile[255], bx[255];
	unsigned char c;
	long i, j, m, n, f, p, l;
	long flength;
	FILE *ifp, *ofp;


	//�Զ�����ֻ����ʽ��.huf�ļ���ifpָ����ļ�
	ifp = fopen("cwx.txt", "rb");
	if (ifp == NULL)
	{
		printf("\n\t�ļ���ʧ�ܣ�\n\n");
		system("pause");
		return;
	}
	printf("\t���ڵ�ǰĿ¼�½�ѹ�����������ѹ������ļ���������չ��: ");

	//�Զ�����д��ʽ��outpufile�ļ�,ofpָ����ļ�
	ofp = fopen("2.bmp", "wb");
	if (ofp == NULL)
	{
		printf("\n\t��ѹ���ļ���ʧ�ܣ�\n\n");
		system("pause");
		return;
	}
	//��ȡ�ļ���Ϣ
	fread(&flength, sizeof(long), 1, ifp);//��ȡδѹ��ʱԴ�ļ�����
	fread(&f, sizeof(long), 1, ifp);//��ȡѹ���ļ��ĳ��ȣ�λ�ڵ�4���ֽڴ�
	fseek(ifp, f, SEEK_SET);//���ļ�ָ�붨λ���洢�ڵ�������λ��
	fread(&n, sizeof(long), 1, ifp);//��ȡ�ڵ���
	//�ع�Huffman����Huffman����
	for (i = 0; i < n; i++)//����Huffman����n��Ҷ�ӽ��
	{
		fread(&HuffTreeNode[i].b, 1, 1, ifp);//��ȡһ���ֽڣ��õ�huffman����һ���ڵ�
		fread(&c, 1, 1, ifp);//��ȡ�ַ���Ӧ�Ĺ��������볤��
		p = (long)c;
		HuffTreeNode[i].count = p;//count�ɱ�����Ȩֵ��Ϊ������ı��볤��
		HuffTreeNode[i].bits[0] = 0;//��ʼ����Ϊ'\0'
		if (p % 8 > 0)
			m = p / 8 + 1;//�ֽ���
		else
			m = p / 8;
		for (j = 0; j < m; j++)
		{
			fread(&c, 1, 1, ifp);//ÿ��ȡ��һ���ֽ�
			f = c;
			_itoa(f, buf, 2);//��fת��Ϊ�����Ʊ�ʾ���ַ���
			f = strlen(buf);//long��ɶ�����ʱ���粻��8λ��������8λ��0
			for (l = 8; l > f; l--)
			{
				strcat(HuffTreeNode[i].bits, "0");//���ڹ������������벹0
			}
			strcat(HuffTreeNode[i].bits, buf);//����0��������ת�õ�01�ַ���
		}
		HuffTreeNode[i].bits[p] = 0;//���ý�����
	}
	HuffNode tmp;
	for (i = 0; i < n; i++)//���ݹ���������ĳ��̣��Խ��������򣬱���̵���ǰ��
	{
		for (j = i + 1; j < n; j++)
		{
			if (strlen(HuffTreeNode[i].bits) > strlen(HuffTreeNode[j].bits))
			{
				tmp = HuffTreeNode[i];
				HuffTreeNode[i] = HuffTreeNode[j];
				HuffTreeNode[j] = tmp;
			}
		}
	}
	p = strlen(HuffTreeNode[n - 1].bits);//�������󳤶�
	fseek(ifp, 8, SEEK_SET);//��λ�ļ�ָ����ԭ�ļ������������λ��
	m = 0;
	bx[0] = 0;//ÿ�δ���Ľ�����ַ���
	while (1)//ͨ������������ĳ��̣����ν��룬��ԭ����λ�洢��ԭ���ֽڴ洢
	{
		while (strlen(bx) < (unsigned int)p)//bx����������01�����п�����һ���ַ���Ҳuoukeneng�Ƕ���ַ�
		{
			fread(&c, 1, 1, ifp);//ȡһ���ַ�,ת���ɶ�����01
			f = c;
			_itoa(f, buf, 2);
			f = strlen(buf);
			for (l = 8; l > f; l--)//�ڵ��ֽ��ڶ���Ӧλ�ò�0
			{
				strcat(bx, "0");
			}
			strcat(bx, buf);
		}
		for (i = 0; i < n; i++)
		{
			if (memcmp(HuffTreeNode[i].bits, bx, HuffTreeNode[i].count) == 0)//�ҵ�����
				break;
		}
		//�Ƚϳɹ�������������ж�bx��Ӧ�������ַ�
		strcpy(bx, bx + HuffTreeNode[i].count);
		c = HuffTreeNode[i].b;//�õ�ƥ���Ĺ����������Ӧ���ַ�
		fwrite(&c, 1, 1, ofp);//���õ����ַ�д��Ŀ���ļ�
		m++;
		if (m == flength)
			break;//flength��ԭ�ļ�����
	}
	fclose(ifp);//�ر�
	fclose(ofp);
	printf("\n\t��ѹ���ļ��ɹ���\n");
	if (m == flength)//�Խ�ѹ�����ļ���ԭ�ļ���ͬ�ԱȽϽ����жϣ������ļ���С��
		printf("\t��ѹ���ļ���ԭ�ļ���ͬ!\n\n");
	else
		printf("\t��ѹ���ļ���ԭ�ļ���ͬ!\n\n");
	return;
}

int main()

{

	
	jieyasuo();
}