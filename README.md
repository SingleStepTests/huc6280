# huc6280
Mesen-generated Huc6280 JSON single-step tests

Mesen *may* be the most accurate Huc6280 emulator currently. It passes timing tests other emulators don't. It needs more research, though, and these tests are only as good as Mesen.

These tests are not perfect. They treat RAM as a flat 2MB chunk, with no MMU other than the usual MPR translation.

Also, due to limitations in the test generator, currently only up to 500 RAM pairs and 500 cycles are supported. This is only an issue for block-move instructions.

The tests are distributed in a binary format, because it's easier for me to use them this way. However, I include a Python script to translate them to plain .json. If you'd like to use the binary format, follow what the Python transcoder program does to extract the data.

Here is an example test:

```json
{
  "name": "01 #0",
  "opcode": 1,
  "initial": {
    "A": 177,
    "X": 82,
    "Y": 20,
    "S": 118,
    "P": 79,
    "PC": 9336,
    "MPR": [ 235, 126, 85, 150, 189, 131, 92, 110 ],
    "RAM": [
      [ 1033336, 1 ],
      [ 1033337, 153 ],
      [ 1032427, 254 ],
      [ 1032428, 19 ],
      [ 1930238, 47 ]
    ]
  },
  "final": {
    "A": 191,
    "X": 82,
    "Y": 20,
    "S": 118,
    "P": 205,
    "PC": 9338,
    "MPR": [ 235, 126, 85, 150, 189, 131, 92, 110 ],
    "RAM": [
      [ 1033336, 1 ],
      [ 1033337, 153 ],
      [ 1032427, 254 ],
      [ 1032428, 19 ],
      [ 1930238, 47 ]
    ]
  },
  "num_cycles": 7,
  "cycles": [
    [ 1033336, 1, "r--" ],
    [ 1033337, 153, "r--" ],
    [ 2097151, 255, "r-d" ],
    [ 1032427, 254, "r--" ],
    [ 1032428, 19, "r--" ],
    [ 2097151, 255, "r-d" ],
    [ 1930238, 47, "r--" ]
  ]
}

```

### The top-level keys are "initial," "final," "opcode," "num_cycles," "cycles," and "name."

### name
A unique name for the test. Also used as the RNG seed for the test.

### opcode
The opcode being tested

### Initial and final are the same format.
They contain the initial and final state of all relevant registers in the CPU, as well as the state of various places in RAM.

A, X, Y, S, P, and PC should be self-explanatory, as should MPR.

Each 2-pair in the "RAM" section (example):
```json
[ 1033337, 153 ]
```
consists of an address and value.

### num_cycles
As noted above, only up to 500 cycles are stored. This verifies the total number of cycles for the instruction.

### cycles
A list of cycles, assuming that opcode fetch is the first cycle (many emulators use that as the last cycle of the previous instruction).

Example:
```json
[ 2097151, 255, "r-" ]
```

This is address pins, data pins, and r/w pins. A pin is 'on' if it is present in the list, and 'off' if it is -.

The read and write pins should be obvious.

## Disclaimers

* Again, these tests are made from Mesen, so are only as accurate as Mesen is.
* We're not even 100% sure about dummy reads and writes how they act...
* Currently only up to 500 RAM pairs and 500 cycles are supported
* So buyer beware!

I hope you find them useful!
