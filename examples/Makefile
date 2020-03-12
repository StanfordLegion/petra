BIN := sqrt collatz

LDFLAGS += -lm

.SUFFIXES: # disable builtin rules (results in cyclic dependency on .py)

.PHONY: all
all: $(BIN)

.PHONY: run
run: all
	for bin in $(BIN); do ./$$bin; done

%.py.o: %.py
	python $<

%.c.o: %.c
	$(CC) $(CFLAGS) $^ -c -o $@

$(BIN): % : %.c.o %.py.o
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

.PHONY: clean
clean:
	rm -f $(BIN) *.o
