#include <iostream>

/* run this program using the console pauser or add your own getch, system("pause") or input loop */
#include<stdio.h>
#include<math.h>
#include<windows.h>

struct HuffNode {
	unsigned char b;//字节值
	int count;//字节出现频率
	long parent;//节点对应的父亲节点下标
	long lch, rch;//节点对应的左右子节点
	char bits[256];//节点对应的哈夫曼编码数组
}HuffTreeNode[512];//.Huffman树的存储结构定义




void jieyasuo()
{


	char buf[512];//定义缓冲区，保存字节的huffman编码
	buf[0] = 0;//初始为'\0'
	char filename[255], outputfile[255], bx[255];
	unsigned char c;
	long i, j, m, n, f, p, l;
	long flength;
	FILE *ifp, *ofp;


	//以二进制只读方式打开.huf文件，ifp指向该文件
	ifp = fopen("cwx.txt", "rb");
	if (ifp == NULL)
	{
		printf("\n\t文件打开失败！\n\n");
		system("pause");
		return;
	}
	printf("\t将在当前目录下解压，请您输入解压缩后的文件名包括拓展名: ");

	//以二进制写方式打开outpufile文件,ofp指向该文件
	ofp = fopen("2.bmp", "wb");
	if (ofp == NULL)
	{
		printf("\n\t解压缩文件打开失败！\n\n");
		system("pause");
		return;
	}
	//读取文件信息
	fread(&flength, sizeof(long), 1, ifp);//读取未压缩时源文件长度
	fread(&f, sizeof(long), 1, ifp);//读取压缩文件的长度，位于第4个字节处
	fseek(ifp, f, SEEK_SET);//将文件指针定位到存储节点总数的位置
	fread(&n, sizeof(long), 1, ifp);//读取节点数
	//重构Huffman树及Huffman编码
	for (i = 0; i < n; i++)//构造Huffman树的n个叶子结点
	{
		fread(&HuffTreeNode[i].b, 1, 1, ifp);//读取一个字节，得到huffman树的一个节点
		fread(&c, 1, 1, ifp);//读取字符对应的哈夫曼编码长度
		p = (long)c;
		HuffTreeNode[i].count = p;//count由保存结点权值改为保存结点的编码长度
		HuffTreeNode[i].bits[0] = 0;//初始编码为'\0'
		if (p % 8 > 0)
			m = p / 8 + 1;//字节数
		else
			m = p / 8;
		for (j = 0; j < m; j++)
		{
			fread(&c, 1, 1, ifp);//每次取出一个字节
			f = c;
			_itoa(f, buf, 2);//将f转换为二进制表示的字符串
			f = strlen(buf);//long变成二进制时，如不足8位，而不足8位则补0
			for (l = 8; l > f; l--)
			{
				strcat(HuffTreeNode[i].bits, "0");//先在哈夫曼树结点编码补0
			}
			strcat(HuffTreeNode[i].bits, buf);//补足0后连接已转好的01字符串
		}
		HuffTreeNode[i].bits[p] = 0;//设置结束符
	}
	HuffNode tmp;
	for (i = 0; i < n; i++)//根据哈夫曼编码的长短，对结点进行排序，编码短的在前面
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
	p = strlen(HuffTreeNode[n - 1].bits);//编码的最大长度
	fseek(ifp, 8, SEEK_SET);//定位文件指针存放原文件哈夫曼编码的位置
	m = 0;
	bx[0] = 0;//每次处理的解码的字符串
	while (1)//通过哈夫曼编码的长短，依次解码，从原来的位存储还原到字节存储
	{
		while (strlen(bx) < (unsigned int)p)//bx保存最长编码的01串，有可能是一个字符，也uoukeneng是多个字符
		{
			fread(&c, 1, 1, ifp);//取一个字符,转换成二进制01
			f = c;
			_itoa(f, buf, 2);
			f = strlen(buf);
			for (l = 8; l > f; l--)//在单字节内对相应位置补0
			{
				strcat(bx, "0");
			}
			strcat(bx, buf);
		}
		for (i = 0; i < n; i++)
		{
			if (memcmp(HuffTreeNode[i].bits, bx, HuffTreeNode[i].count) == 0)//找到编码
				break;
		}
		//比较成功后，需继续往后判断bx对应的其他字符
		strcpy(bx, bx + HuffTreeNode[i].count);
		c = HuffTreeNode[i].b;//得到匹配后的哈夫曼编码对应的字符
		fwrite(&c, 1, 1, ofp);//将得到的字符写入目标文件
		m++;
		if (m == flength)
			break;//flength是原文件长度
	}
	fclose(ifp);//关闭
	fclose(ofp);
	printf("\n\t解压缩文件成功！\n");
	if (m == flength)//对解压缩后文件和原文件相同性比较进行判断（根据文件大小）
		printf("\t解压缩文件与原文件相同!\n\n");
	else
		printf("\t解压缩文件与原文件不同!\n\n");
	return;
}

int main()

{

	
	jieyasuo();
}