override CFLAGS := -m32 -Wall -fno-stack-protector $(CFLAGS)
override LDFLAGS := -m32 -fno-stack-protector 
PRG = ropeman
OBJS = checkASLR.o display.o ropeman.o scoreboard.o


all: $(PRG)

$(PRG): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^

clean:
	$(RM) -f $(PRG) $(OBJS)

.PHONY: all clean
