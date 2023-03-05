

---

ANSI-C & POSIX

## memmove

与memcpy区别在于允许from和to区域重叠时的行为是可预期的, 不会出现错误.

size为0时行为未定义.



## dup2实现重定向



把标准输出重定向到fd：

```
int fd = open("output.txt", O_RDWR|O_CREAT, 0666);
int replaced = dup2(fd, STDOUT_FILENO);
```



## printf格式

| 型                     | フォーマット |
| :--------------------- | :----------- |
| ssize_t                | %zd          |
| size_t                 | %zu          |
| int_max_t              | %jd          |
| intmax_t               | %ju          |
| signed char            | %hhd         |
| unsigned char          | %hhu         |
| short int              | %hd          |
| unsigned short int     | %hu          |
| int                    | %d           |
| unsigned int           | %u           |
| long int               | %ld          |
| unsigned long int      | %lu          |
| long long int          | %lld         |
| unsigned long long int | %llu         |



## getopt()

```
	#include <unistd.h>
	
    const char *optstring = "f:b:m:h";
	int opt;
    while ((opt = getopt(argc, argv, optstring)) != -1) {
        printf("opt = %c\n", opt);  // 命令参数，亦即 -a -b -c -d
        printf("optarg = %s\n", optarg); // 参数内容
        printf("optind = %d\n", optind); // 下一个被处理的下标值
        printf("argv[optind - 1] = %s\n\n",  argv[optind - 1]); // 参数内容

		switch (opt) {
		case 'f':
			FreqKHz = atoi(optarg);
			printf("option freq=%d\n", FreqKHz);
			break;
		case 'b':
			BandWidthKHz = atoi(optarg);
			printf("option band=%d\n", BandWidthKHz);
			break;
		case 'm':
			if (0 == strcmp(optarg, "dvbc")) {
				mode = DTV_MODE_DVBC;
			}
			else if (0 == strcmp(optarg, "dtmb")) {
				mode = DTV_MODE_DTMB;
			}
			else {
				printf("unknown mode %s", optarg);
			}
			printf("option band=%s\n", optarg);
			break;
		default:
			printf("error optopt: %c\n", optopt);
			printf("error opterr: %d\n", opterr);
		}
    }
```



## getopt_long()

参考：[25.2.4 Example of Parsing Long Options with `getopt_long`](https://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Option-Example.html)

getopt()的加强版，同时支持长短参数，当匹配到长参数时，会返回`struct option`项中的val值；

使用短参数时，和getopt()一样要传入optstring，如下面例子中的`-h`，需要传一个`h`。

```
#include <getopt.h>


static void print_usage(const char *prog)
{
	printf("usage: %s [Options]\n\n", prog);
	printf(
		"Options:\n"
		"  --dump-video=<file>          dump video stream to file\n"
		"  -h                           print help\n"
	);
}

#define ARG_DUMP_VIDEO    1
static struct option long_options[] = {
	{"dump-video", required_argument, 0, ARG_DUMP_VIDEO},
	{"help",       no_argument,       0, 'h'},
	{0, 0, 0, 0}
};

int main(int argc, char **argv)
{	
	int c, opt_index = 0;

	while (1) {
		c = getopt_long(argc, argv, "h", long_options, &opt_index);
		if (c == -1)
        	break;

		switch (c) {
			case ARG_DUMP_VIDEO:
				printf("dump-video!!! %s\n", optarg);
				break;
			case 'h':
				print_usage(argv[0]);
				exit(0);
				break;
			default:
				exit(1);
				break;
		}
	}
```

