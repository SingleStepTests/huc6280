#!/usr/bin/python3
import os
import glob
import json
from struct import unpack_from
from typing import Dict, Any


def load_cycles(buf, ptr):
    cycles = []
    full_sz = 4
    num_cycles = unpack_from('I', buf, ptr)[0]
    ptr += 4
    rec_cycles = unpack_from('I', buf, ptr)[0]
    ptr += 4
    for i in range(0, rec_cycles):
        cdata = unpack_from('I', buf, ptr)[0]
        ptr += 4
        full_sz += 4
        # u32 o = c->RD | (c->WR << 1) | (c->Addr << 2) | (c->D << 24);
        rd = cdata & 1
        wr = (cdata >> 1) & 1
        dummy = (cdata >> 2) & 1
        addr = (cdata >> 3) & 0x1FFFFF
        data = (cdata >> 24) & 0xFF
        pstr = 'r' if rd else '-'
        pstr += 'w' if wr else '-'
        if dummy:
            pstr = '--'
        cycles.append([addr, data, pstr])

    return full_sz, cycles, num_cycles


def load_state(buf, ptr) -> (int, Any):
    full_sz = unpack_from('i', buf, ptr)[0]
    ptr += 4
    '''
        W32(st.num_RAM);
        for (u32 i = 0; i < st.num_RAM; i++) {
            struct RAM_pair *rp = &st.RAM_pairs[i];
            W16(rp->addr);
            W8(rp->val);
        }
        size_t len = ts.ptr - bufbegin;
        cW32(bufbegin, 0, (u32)len);
    
    '''
    state = {}
    values = unpack_from('B' * 5, buf, ptr)
    ptr += 5
    state['A'] = values[0]
    state['X'] = values[1]
    state['Y'] = values[2]
    state['S'] = values[3]
    state['P'] = values[4]
    state['PC'] = unpack_from('H', buf, ptr)[0]
    ptr += 2
    state['MPR'] = []
    for i in range(0, 8):
        state['MPR'].append(unpack_from('B', buf, ptr)[0])
        ptr += 1
    state['RAM'] = []
    num_ram = unpack_from('i', buf, ptr)[0]
    ptr += 4
    for i in range(0, num_ram):
        addr = unpack_from('I', buf, ptr)[0]
        ptr += 4
        val = unpack_from('B', buf, ptr)[0]
        ptr += 1
        state['RAM'].append((addr, val))
    return full_sz, state


def decode_test(buf, ptr) -> (int, Dict):
    full_sz = unpack_from('i', buf, ptr)[0]
    ptr += 4
    test = {}
    # 50 char name
    # 32-bit opcode
    # initial, final
    # num. cycles
    # cycle array
    nn = unpack_from('50s', buf, ptr)[0].decode()
    test['name'] = nn.strip()

    sz = 50
    ptr += sz
    opcode = unpack_from('I', buf, ptr)[0]
    test['opcode'] = opcode
    ptr += 4
    sz, test['initial'] = load_state(buf, ptr)
    ptr += sz
    sz, test['final'] = load_state(buf, ptr)
    ptr += sz
    sz, ns, num_cycles = load_cycles(buf, ptr)
    test['num_cycles'] = num_cycles
    test['cycles'] = ns
    ptr += sz

    #print(json.dumps(test, indent=2))

    return full_sz, test


def decode_file(infilename, outfilename):
    print('Decoding ' + infilename)
    with open(infilename, 'rb') as infile:
        content = infile.read()
    NUMTESTS = unpack_from('<I', content, 0)[0]
    ptr = 4
    tests = []
    for i in range(0, NUMTESTS):
        sz, test = decode_test(content, ptr)
        ptr += sz
        tests.append(test)
    if os.path.exists(outfilename):
        os.unlink(outfilename)
    with open(outfilename, 'w') as outfile:
        outfile.write(json.dumps(tests, indent=2))


def do_path(where):
    print("Doing path...", where)
    fs = glob.glob(where + '**.json.bin')
    for fname in fs:
        decode_file(fname, fname[:-4])


def main():
    do_path('v1/')


if __name__ == '__main__':
    main()
