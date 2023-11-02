.text
ori, $v1, $a0, 0x3f09
label9:
lui, $v1, 0x96b
label1:
ori, $s5, $s3, 0xb3fc
add, $v0, $v1, $t4
jal, label0
label8:
ori $t0, $zero, 3968
lw, $t1, 216($t0)
jal, label0
ori $t0, $zero, 4184
lw, $t6, 0($t0)
beq, $a0, $v1, label1
ori, $s0, $s7, 0xcd1e
ori $t0, $zero, 4184
lw, $a0, 0($t0)
ori $t0, $zero, 13048
sw, $a2, -992($t0)
ori $t0, $zero, 10708
sw, $s4, 4196($t0)
ori, $a3, $t6, 0xf31b
add, $v0, $s3, $v0
lui, $s0, 0x55dd
label0:
sub, $s3, $t3, $s0
ori $t0, $zero, 4184
lw, $v1, 0($t0)
ori, $v0, $t0, 0xf89f
ori, $v1, $a2, 0x7e98
ori, $s0, $s3, 0x7faf
ori, $a3, $t7, 0xf4f3
lui, $t7, 0x2a69
ori, $a1, $a1, 0x4321
ori, $a0, $v1, 0xe358
ori, $v1, $s3, 0x5314
jal, label1
ori $t0, $zero, 6008
lw, $v1, 7060($t0)
lui, $t9, 0xfb28
lui, $v0, 0x4bb9
ori $t0, $zero, 880
lw, $s7, -100($t0)
sub, $a1, $a0, $v1
jal, label2
jal, label3
jal, label0
add, $t4, $a3, $v0
ori, $t8, $a0, 0xed12
ori $t0, $zero, 4184
sw, $s4, 0($t0)
ori, $v1, $t9, 0x5aa7
add, $t3, $s0, $v0
ori, $s6, $v1, 0xdaeb
beq, $a1, $t5, label1
add, $s1, $t1, $t9
ori, $t2, $s4, 0x83f8
ori $t0, $zero, 14904
sw, $v0, 0($t0)
ori, $s3, $v1, 0x118b
ori $t0, $zero, 12056
sw, $t1, 0($t0)
jal, label3
ori $t0, $zero, 464
sw, $t5, 1460($t0)
beq, $v1, $s4, label1
jal, label0
jal, label4
jal, label0
ori $t0, $zero, 3324
sw, $a0, 212($t0)
sub, $s6, $t4, $a2
ori, $a3, $s7, 0xc7e6
beq, $a3, $t8, label5
ori $t0, $zero, 2216
sw, $a0, 592($t0)
jal, label2
ori, $t3, $v1, 0x2417
ori, $s0, $v0, 0x13
add, $s1, $v1, $t5
ori $t0, $zero, 3536
lw, $v0, 0($t0)
ori $t0, $zero, 2620
sw, $s0, 12728($t0)
beq, $v0, $s0, label4
lui, $a0, 0x24b1
label4:
add, $v1, $v0, $a3
beq, $v0, $a2, label0
ori, $s3, $a3, 0xf937
label2:
label7:
beq, $a3, $s7, label6
ori, $s1, $s4, 0x860
beq, $s4, $t7, label0
label3:
sub, $t4, $s0, $v1
label6:
ori, $t7, $a2, 0xb8c1
ori $t0, $zero, 4184
lw, $s3, 0($t0)
ori, $s7, $a1, 0x1f7a
jal, label4
sub, $t8, $s7, $t2
sub, $s2, $a2, $t8
ori, $v0, $s1, 0xba5d
add, $s5, $t7, $t8
lui, $t9, 0xc1c5
jal, label2
add, $a3, $s4, $v1
lui, $v1, 0xac42
jal, label7
beq, $s0, $a0, label8
ori, $v0, $s1, 0x1eea
add, $a0, $a0, $s1
label5:
beq, $t0, $a3, label9
ori $t0, $zero, 11828
sw, $s6, -5168($t0)
sub, $a2, $t6, $a3
ori $t0, $zero, 2148
lw, $t6, 11184($t0)
ori, $s5, $a3, 0x5eaf
ori $t0, $zero, 1924
sw, $a2, 0($t0)
ori $t0, $zero, 14904
lw, $a3, 0($t0)
ori $t0, $zero, 11064
sw, $v1, -1044($t0)
beq, $a3, $t6, label3
ori, $s6, $v0, 0x2433
ori, $s1, $a0, 0x920b
ori $t0, $zero, 13472
lw, $s5, 1288($t0)
ori $t0, $zero, 780
sw, $a2, 0($t0)
ori $t0, $zero, 40
lw, $s5, 3780($t0)
