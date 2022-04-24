print_int:
    lw $a0, 0($fp)
    li $v0, 1
    syscall

print_char:
    lw $a0, 0($fp)
    li $v0, 11
    syscall

print_float:
    l.s $f12, 0($fp)
    li $v0, 2
    syscall

malloc:
    lw $a0, 0($fp)
    li $v0, 9
    syscall

    # Stack Pointer Change
    la $sp, 0($fp)
    lw $ra, -8($sp)
    lw $fp, -4($sp)
    jr $ra

read_int:
    li $v0, 5
    syscall

    #; Stack Pointer Change
    la $sp, 0($fp)
    lw $ra, -8($sp)
    lw $fp, -4($sp)
    jr $ra

read_float:
    li $v0, 6
    syscall  

    la $sp, 0($fp) 
    lw $ra, -8($sp)
    lw $fp, -4($sp)
    jr $ra         

read_char:
    li $v0, 12
    syscall   

    la $sp, 0($fp) 
    lw $ra, -8($sp)
    lw $fp, -4($sp)
    jr $ra         

read_string:
    la $a0, 0($fp)
    lw $a1, 4($fp)
    li $v0, 8     
    syscall       

    la $sp, 0($fp) 
    lw $ra, -8($sp)
    lw $fp, -4($sp)
    jr $ra         

# power:
#     li $v0, 1
#     li $t0, 0
#
# powLoop:
#     mul $v0, $v0, $a0
#     add $t0, $t0, 1
#     blt $t0, $a1, powLoop
