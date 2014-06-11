Writeup for secuinside 2014 reversing 100 findkey
-------------------------------------------------
I couln't have enough time to solve this probem before the ctf ends, 
so i can't check the flag is right. 

### Description 
*I can't remember :-(* <br>
*something like 'find the key ...'*

### analysis 
```
user@ubuntuvm:~/main/ctf/secuinside2014/findkey$ ./findkey_b2191f33d95fa6d2d0718efdbc78f8ae 
need 2 arguments
user@ubuntuvm:~/main/ctf/secuinside2014/findkey$ ./findkey_b2191f33d95fa6d2d0718efdbc78f8ae 1 2
key 1 = 1
0 is differnce
Wrong password
user@ubuntuvm:~/main/ctf/secuinside2014/findkey$ 
```

This program requires 2 argments. After some analysis, it turns out
- 1st arguemnt : key strings 
- 2nd arguemnt : chars order 

if i find out right keyword chars and right order of chars, 
i can get the flag. 

##### 1-stage (find out key chars)
function of checking first argument looks like this 

```c
  for ( i = 0; i <= 55; ++i )
  {
    v7 = 0LL;
    for ( j = 0; ; ++j )
    {
      v4 = strlen((&str_table)[4 * i]);
      v2 = which_small(&a2, &v4);
      if ( *(_DWORD *)v2 <= j )
        break;
      v7 += (&str_table)[4 * i][j] * (signed int)*(_BYTE *)(j + a1);
    }
    if ( v7 != result_table[i] )
    {
      printf("%d is differnce\n", i);
      return 0;
    }
  }
```

Each char of input strings converted to integer and multiplied each char of one of 55 strings(0x804F0A0). 
And the sum of them should equal to value of result_table (0x804F180)
so i can get multivariable linear equation. 
For example, for the first string "No pain, No gain - gogil", i can get this equation. 

```
x0*78 + x1*111 + x2*32 + x3*112 + x4*97 + x5*105 + x6*110 + x7*44 + x8*32 + 
x9*78 + x10*111 + x11*32 + x12*103 + x13*97 + x14*105 + x15*110 + x16*32 + 
x17*45 + x18*32 + x19*103 + x20*111 + x21*103 + x22*105 + x23*108 = 0x00029344 // "No pain, No gain - gogil"
```
After solving this eqaution, i got this key char list which is the first argument of the program.

```
user@ubuntuvm:~/main/ctf/secuinside2014/findkey$ ./findkey_b2191f33d95fa6d2d0718efdbc78f8ae '3 lroea5 r  tfmh0wl1y15on 3y! 4n 50r,30wv3r !4kwi' 1
key 1 = 3 lroea5 r  tfmh0wl1y15on 3y! 4n 50r,30wv3r !4kwi
Wrong password
```

###### 2-stage (find out order)
Next stage is finding out right order to reorder first argument string. 
Second argument is converted to 49 integers like this.  

```python 
n = 49 # 0x31
user_input = 'what?'
user_input = [int(user_input[i:i+4]) for i in range(0, len(user_input), 4)]
for index in range(n) :
        v = 0
        for i in range(len(user_input)) :
                v = (10000 * v + user_input[i]) %n
        integer_list.append(v) 
        print v, 
        # expected : 8, 4, 45, 9, 12, 26, 15, 10, 35, 17, 39, 14, 36, 32, 29, 37, 1, 0, 47, 5, 42, 11, 27, 46, 13, 31, 30, 19, 48, 23, 18, 6, 44, 22, 28, 34, 43, 41, 33, 25, 7, 38, 16, 20, 3, 24, 40, 2, 21

        v = 0
        for i in range(len(user_input)) :
                v = 10000 * (v%n) + user_input[i]
                user_input[i] = v/n
```

and checked each value like this.

```c
  for ( i = 0; i < n_copy; ++i )                
  {
    count = 0;
    for ( j = 0; j < i; ++j )
    {
      v3 = *(_DWORD *)getvalue_by_index(&struct1, j);
      if ( v3 > *(_DWORD *)getvalue_by_index(&struct1, i) )
        ++count;
    }
    if ( tbl_countcheck[i] != count ) // tbl_countcheck = 0x804F280
    {
      v4 = 0;
      goto FREE_RETURN;
    }
  }
```  

The right order is easily found by this code 
```python
# 0x804F280
table = [0, 1, 0, 1, 1, 1, 2, 4, 1, 3, 
1, 6, 2, 4, 5, 2, 16, 17, 0, 16, 
2, 14, 9, 1, 15, 9, 10, 14, 0, 15, 
17, 27, 4, 17, 14, 10, 5, 7, 13, 21, 
35, 9, 28, 25, 42, 23, 8, 45, 27]

numbers = range(n)
numbers.reverse()
ans = [0]*n
for i in range(n-1, -1, -1): 
	num = numbers[table[i]]
	ans[i]=num
	numbers.remove(num)
order = ans
```
and i got this 

```
[8, 4, 45, 9, 12, 26, 15, 10, 35, 17, 39, 14, 36, 32, 29, 37, 1, 0, 47, 5, 42, 11, 27, 46, 13, 31, 30, 19, 48, 23, 18, 6, 44, 22, 28, 34, 43, 41, 33, 25, 7, 38, 16, 20, 3, 24, 40, 2, 21]
```

### Find the key  

And now i got 2nd argument, 
and finally i got the flag. :-) 

```
root@ubuntuvm:/home/user/main/ctf/secuinside2014/findkey# python findkey.py
[+] Stage-1 ... 
[>] 1st argument :  3 lroea5 r  tfmh0wl1y15on 3y! 4n 50r,30wv3r !4kwi
[+] Stage-2 ... 
[>] 2nd argument :  28367585747398446017812492718893415428463369378432457345198085366128794480569061784
[+] run program ... 
key 1 = 3 lroea5 r  tfmh0wl1y15on 3y! 4n 50r,30wv3r !4kwi
The flag is : 'w0w! 1nv3r51on arr4y i5 4we50m3 f0r th3 k3y, lol!'
root@ubuntuvm:/home/user/main/ctf/secuinside2014/findkey# 
```

source code : [https://github.com/mayfly74/ctf-writeup/blob/master/secuinside_2014_quals/findkey_reversing100/findkey.py]

*Sorry for my poor English.* 

