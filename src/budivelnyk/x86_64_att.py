from typing import Iterator

from .intermediate import Node, Loop, Add, Move, Output, Input


def generate_x86_64_att(intermediate: list[Node]) -> Iterator[str]:
    yield from _generate_prologue()
    yield from _generate_body(intermediate)
    yield from _generate_epilogue()


def _generate_prologue() -> Iterator[str]:
    yield '.globl run'
    yield '.type run, @function'
    yield ''
    yield 'run:'


def _generate_body(intermediate: list[Node], parent_label: str='') -> Iterator[str]:
    loop_id = 0
    for node in intermediate:
        match node:
            case Add(n):
                if n == 1:
                    yield '    incb   (%rdi)'
                elif n == -1:
                    yield '    decb   (%rdi)'
                elif n > 1:
                    yield f'    addb   ${n}, (%rdi)'
                elif n < 1:
                    yield f'    subb   ${-n}, (%rdi)'
            
            case Move(n):
                if n == 1:
                    yield '    incq   %rdi'
                elif n == -1:
                    yield '    decq   %rdi'
                elif n > 1:
                    yield f'    addq   ${n}, %rdi'
                elif n < 1:
                    yield f'    subq   ${-n}, %rdi'
            
            case Output(n):
                yield '    pushq  %rdi'
                yield '    movzbq (%rdi), %rdi'
                sequence = ['    call   putchar', '    mov    %rax, %rdi'] * n
                yield from sequence[:-1]
                yield '    popq   %rdi'
            
            case Input(n):
                yield '    pushq  %rdi'
                yield from ['    call   getchar'] * n
                yield '    popq   %rdi'
                yield '    movb   %al, (%rdi)'
            
            case Loop(body):
                label = f'{parent_label}_{loop_id}'
                yield f'start{label}:'
                yield '    cmpb   $0, (%rdi)'
                yield f'    je     end{label}'
                yield from _generate_body(body, label)
                yield f'    jmp    start{label}'
                yield f'end{label}:'
                loop_id += 1


def _generate_epilogue() -> Iterator[str]:
    yield '    ret'
    yield ''
    yield '.section .note.GNU-stack, "", @progbits'
