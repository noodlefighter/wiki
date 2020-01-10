

---



> via: https://stackoverflow.com/questions/2917881/how-to-implement-a-timeout-in-read-function-call

```
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/select.h>

int main(void)
{
  fd_set set;
  struct timeval timeout;
  int rv;
  char buff[100];
  int len = 100;
  int filedesc = open( "dev/ttyS0", O_RDWR );

  FD_ZERO(&set); /* clear the set */
  FD_SET(filedesc, &set); /* add our file descriptor to the set */

  timeout.tv_sec = 0;
  timeout.tv_usec = 10000;

  rv = select(filedesc + 1, &set, NULL, NULL, &timeout);
  if(rv == -1)
    perror("select"); /* an error accured */
  else if(rv == 0)
    printf("timeout"); /* a timeout occured */
  else
    read( filedesc, buff, len ); /* there was data to read */
}
```

