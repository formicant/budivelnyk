from typing import Iterator

from .intermediate import Node, Loop, Add, Move, Output, Input


def generate_x86_64_intel(intermediate: list[Node]) -> Iterator[str]:
    yield from _generate_prologue()
    yield from _generate_body(intermediate)
    yield from _generate_epilogue()


def _generate_prologue() -> Iterator[str]:
    yield '.globl run'
    yield '.intel_syntax noprefix'
    yield '.type run, @function'
    yield ''
    yield 'run:'


def _generate_body(intermediate: list[Node], parent_label: str='') -> Iterator[str]:
    loop_id = 0
    for node in intermediate:
        match node:
            case Add(n):
                if n == 1:
                    yield '    inc   byte ptr [rdi]'
                elif n == -1:
                    yield '    dec   byte ptr [rdi]'
                elif n > 1:
                    yield f'    add   byte ptr [rdi], {n}'
                elif n < 1:
                    yield f'    sub   byte ptr [rdi], {-n}'
            
            case Move(n):
                if n == 1:
                    yield '    inc   rdi'
                elif n == -1:
                    yield '    dec   rdi'
                elif n > 1:
                    yield f'    add   rdi, {n}'
                elif n < 1:
                    yield f'    sub   rdi, {-n}'
            
            case Output(n):
                yield '    push  rdi'
                yield '    movzx rdi, byte ptr [rdi]'
                sequence = ['    call  putchar', '    mov   rdi, rax'] * n
                yield from sequence[:-1]
                yield '    pop   rdi'
            
            case Input(n):
                yield '    push  rdi'
                yield from ['    call  getchar'] * n
                yield '    pop   rdi'
                yield '    mov   byte ptr [rdi], al'
            
            case Loop(body):
                label = f'{parent_label}_{loop_id}'
                yield f'start{label}:'
                yield '    cmp   byte ptr [rdi], 0'
                yield f'    je    end{label}'
                yield from _generate_body(body, label)
                yield f'    jmp   start{label}'
                yield f'end{label}:'
                loop_id += 1


def _generate_epilogue() -> Iterator[str]:
    yield '    ret'
    yield ''
    yield '.section .note.GNU-stack, "", @progbits'
