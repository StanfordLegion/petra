#include <stdio.h>

int collatz(int n);

int main()
{
  for (int i = 1; i < 20; i++) {
    printf("collatz(%d): %d\n", i, collatz(i));
  }
  return 0;
}
