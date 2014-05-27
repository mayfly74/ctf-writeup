turdedo는 defcon ctf 2014 quals 문제이다. 
(대회가 끝나고 문제풀이를 마무리하여서 실제 대회서버에서 확인하지는 못하였다)

<Description> 
What a crappy protocol turdedo_5f55104b1d60779dbe8dcf5df2b186ad.2014.shallweplayaga.me:3544 
http://services.2014.shallweplayaga.me/turdedo_5f55104b1d60779dbe8dcf5df2b186ad

<Analysis> 
1.  udp 3544 포트에 알 수 없는 프로토콜을 이용한 서비스가 돌고 있음  
2.  프로토콜을 잘 맞추어서 접속하면 shell을 띄울 수 있다.
3.  shell을 띄우면 간단한 몇 가지 명령을 내릴 수 있는데, 그 중에서 echo 명령에 format strings bug가 있다.
4.  echo 명령을 실행하기 전에 %n을 filter 해서 %_ 로 모두 변경한다. 

<공격방향> 
1. 프로토콜 맞추어서 shell을 띄우기
2. %n filter 우회

<Protocol> 
1. Message format 
message format은 아래와 같다. 

    1) flag = 0x11 (normal)
        +-------+-------+-------+-------+-------+-------+-------+-------+ 0x00
        |          D/C                  | m_size        | flag  |  D/C  | ; flag = 0x11
        +-------+-------+-------+-------+-------+-------+-------+-------+
        |                                                               | 
        |                               sender ip                       | 0x10
        |                                                               |
        +-------+-------+-------+-------+-------+-------+-------+-------+ 
        |                                                               |
        |                               dest ip                         | 0x20
        |                                                               |
        +-------+-------+-------+-------+-------+-------+-------+-------+

        +-------+-------+-------+-------+-------+-------+-------+-------+
        |       D/C     |      PORT     |       size    |       D/C     | 
        +-------+-------+-------+-----|-+-------+-------+-------+-------+
        +                             |

    2) flag = 0x21 (fragmented)
        +-------+-------+-------+-------+-------+-------+-------+-------+ 0x00
        |          D/C                  | m_size        | flag  |  D/C  | ; flag = 0x21
        +-------+-------+-------+-------+-------+-------+-------+-------+
        |                                                               | 
        |                               sender ip                       | 0x10
        |                                                               |
        +-------+-------+-------+-------+-------+-------+-------+-------+ 
        |                                                               |
        |                               dest ip                         | 0x20
        |                                                               |
        +-------+-------+-------+-------+-------+-------+-------+-------+

        +-------+-------+-------+-------+-------+-------+-------+-------+
        |  0x11 |   D/C |    frgmt *    |       size    |       D/C     | ; if flag = 0x21 : PORT else : frgmt
        +-------+-------+-------+--|----+-------+-------+-------+-------+
        +                          |   
        [ MESSAGE ]                |                                                                           
                                   |                   /-----> is_last_packet (last bit)
                                   |    +-------+------|+          
                                   \->  |              *|                                                          
                                        +-------+-------+
                                                         
                                        |<------------->|
                                           frgmt & 0xf8 ------> size                         
2. 3-way handshaking
message format에 맞추어 SYN메시지를 보내면 
SYNACK 뒤에 random number를 보낸다. 
이 number를 ACK와 함께 보내면 handshaking이 완료되고 shell을 띄워 준다.   

    <Client>                           <Server>
        |                                 |                                                  
  [SYN] | ------------------------------> |  
        | <------------------------------ | [SYSACK]
  [ACK] | ------------------------------> |  
        |                                 |                                                  
 

3. shell 
shell 에서는 아래와 같은 명령어를 실행시킬 수 있다. 

server%  help
Available commands:
uname
ls
cat
pwd
echo
exit
server%  

예를 들어 ls 명령의 경우 popen()함수를 통해 명령어를 실행해 준다. 

    if ( !v33 )
    {
      streamc = popen("ls", "r");
      if ( streamc )
      {
        fread(ptr, 1u, 0x270Fu, streamc);
        pclose(streamc);
      }
      if ( strlen(ptr) <= 0x2706 )
      {
        v36 = &ptr[strlen(ptr)];
        *(_DWORD *)v36 = *(_DWORD *)"server% ";
        *((_DWORD *)v36 + 1) = *(_DWORD *)"er% ";
        v36[8] = aServer[8];
      }
      if ( send_msg(ptr, strlen(ptr), a1) != strlen(ptr) )
        exit(0);
      goto LABEL_90;
    }


echo 명령에 아래와 같이 format string 버그가 있다. 

    v60 = (int)"echo ";
    do
    {
      if ( !v58 )
        break;
      v54 = *(_BYTE *)v59 < *(_BYTE *)v60;
      v55 = *(_BYTE *)v59 == *(_BYTE *)v60;
      v59 = (int *)((char *)v59 + 1);
      ++v60;
      --v58;
    }
    while ( v55 );
    if ( !(v54 | v55) == v54 )
    {
      snprintf(ptr, 9999u, v72);
      if ( send_msg(ptr, 0x2710u, a1) != 10000 )
        exit(0);
    }

그렇지만 아래와 같이 %n을 %_로 변경해버리기 때문에 exploit이 쉽지 않다. 

  strcpy(s, "dDiouxXfegEasc[p");
  for ( i = 0; i < a4; ++i )
  {
    if ( *(_BYTE *)(a3 + i) == '%' )
    {
      v6 = 1;
    }
    else if ( v6 && *(_BYTE *)(a3 + i) == 'n' )
    {
      *(_BYTE *)(a3 + i) = '_';
      v6 = 0;
    }
    else if ( v6 && strchr(s, *(_BYTE *)(a3 + i)) )
    {
      v6 = 0;
    }
  }

4. connection info table  0x804e170 (0x54 84 bytes)
내부적으로 connection을 관리하는 table은 아래와 같은 구조로 되어 있다. 

        +-------+-------+-------+-------+-------+-------+-------+-------+ 0x00
        |                                                               |
        |-------+-------+-------+-------+-------------------------------+
        |           rand()              |                               |
        +-------+-------+-------+-------+                               | 0x10
        |                             addr                              |
        |                               +-------+-------+-------+-------+ 
        |                               |                               |
        +-------+-------+-------+-------+-------+-------+-------+-------+ 0x20
        |                                                               |
        |                               sender ip                       |
        |                                                               |
        +-------+-------+-------+-------+-------+-------+-------+-------+ 0x30
        |                                                               |
        |                               dest ip                         |
        |                                                               |
        +-------+-------+-------+-------+-------+-------+-------+-------+ 0x40
        |      msg      |     PORT      |             rand()            | 
        +-------+-------+-------+-------+-------+-------+-------+-------+
        |            time(0)            | state |                       |
        +-------+-------+-------+-------+-------+-------+-------+-------+ 0x50
        |           ptr                 |
        +-------+-------+-------+-------+

<%n filter bypassing> 
1. Fragmentation info table 0x804e160 (0x34 52 bytes)
%n filter를 우회하기 위해서 fragmented 된 패킷을 받을 경우 사이즈가 16보다 작으면 
filter 함수를 거치지 않는다는 것을 활용한다. 

      if ( ntohs(*(_WORD *)(buff + 4)) > 0x10u )
      {
        v7 = ntohs(*(_WORD *)(buff + 4));
        n_filter(buff + 48, v8, buff + 48, v7 - 8);
      }

fragmented 된 패킷은 buffer에 우리가 지정한 곳에 사이즈만큼 복사되었다가, 
끝을 알려주는 마지막 bit를 set 해서 보내면 조합된 패킷으로 처리한다.  

        +-------+-------+-------+-------+-------+-------+-------+-------+ 0x00
    /---|-----* size    |       D/C     |                               | 
    |   +-------+-------+-------+-------+                               | 
    |   |                                send ip                        |   
    |   |                               +-------+-------+-------+-------+ 0x10
    |   |                               |                               |
    |   +-------+-------+-------+-------                                | 
    |   |                             dest ip                           |
    |   |                               +-------+-------+-------+-------+ 0x20
    |   |                               |               buffer *--------|-----------\
    |   +-------+-------+-------+-------+-------+-------+-------+-------+           |
    |   |  v_length-40  |      D/C      |           time(0)             |           |
    |   +-------+-------+-------+-------+-------+-------+-------+-------+ 0x30      |
    |   |             ptr               |                                           |
    |   +-------+-------+-------+-------+                                           |
    |                                                                               |
    \--> variable length : (frgmt&0xff80) + (m_size-8) + 40                         |
                                                                                    |
        /---------------------------------------------------------------------------/ 
        |
        V                                                                                  
        +-------+-------+-------+-------+-------+-------+-------+-------+
        |         D/C                   | m_size        | flag  |  D/C  | ; m_szie -> (variable_length - 40)
        +-------+-------+-------+-------+-------+-------+-------+-------+
        |                                                               |
        |                               sender ip                       |
        |                                                               |
        +-------+-------+-------+-------+-------+-------+-------+-------+
        |                                                               |
        |                               dest ip                         |
        |                                                               |
  ---   +-------+-------+-------+-------+-------+-------+-------+-------+
   | 
   |   
 (frgmt&0xff80) 
   | 
   |    
   \--->[ MESSAGE ] 

따라서 아래와 같이 차례차례 패킷을 잘라서 보내면 %n filter를 우회할 수 있다. 
                           
[     header     ]     [     header     ]    [     header     ]           [     header     ]   
[     sender ip  ]     [     sender ip  ]    [     sender ip  ]           [     sender ip  ]   
[     sender ip  ]     [     sender ip  ]    [     sender ip  ]           [     sender ip  ]   
[     dest ip    ]     [     dest ip    ]    [     dest ip    ]           [     dest ip    ]   
[     dest ip    ]     [     dest ip    ]    [     dest ip    ]           [     dest ip    ]   
[                ]     [                ]    [                ]   ---->   [ last fragemnted]   
[                ]     [                ]    [                ]           [                ]   
...                    ...                   ...                          ...                  
[                ]     [                ]    [ 3rd fragmented ]           [ 3rd fragmented ]   
[                ]     [ 2nd fragmented ]    [ 2nd fragmented ]           [ 2nd fragmented ]   
[ 1st fragmented ]     [ 1st fragmented ]    [ 1st fragmented ]           [ 1st fragmented ]   

<exploit> 
format string 공격을 하기 위해 sprintf의 got를  
popen을 call 하기 직전의 주소로 덮어 쓴다. 
그러면 echo 명령어를 호출할 때, 해당 명령을 실행할 수 있게 된다. 

gdb$ x/2i snprintf
   0x8048c60 <snprintf@plt>:    jmp    DWORD PTR ds:0x804e09c

.text:0804AB8B                 mov     dword ptr [esp+4], offset modes ; "r"
.text:0804AB93                 mov     eax, [ebp+command]
.text:0804AB99                 mov     [esp], eax      ; command
.text:0804AB9C                 call    _popen

