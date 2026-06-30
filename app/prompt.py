"""Prompt assembly.

The first reference returned by the store is the creator's identity anchor — it
sets the voice. Remaining references are style examples.
"""
from typing import List

from .models import Creative


def build_prompt(brief: str, references: List[Creative]) -> str:
    if not references:
        return f"Write a creative for: {brief}"
    anchor = references[0]          # primary identity reference (store returns primary first)
    others = references[1:]
    voice = anchor.hook
    examples = " / ".join(r.caption for r in others) or "(none)"
    return (
        f"Voice & identity anchor: {voice}\n"
        f"Style examples: {examples}\n"
        f"Now write a fresh creative for: {brief}"
    )
