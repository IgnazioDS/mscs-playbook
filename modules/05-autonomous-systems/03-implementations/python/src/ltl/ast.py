"""LTL abstract syntax tree (AST) nodes and helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AP:
    name: str


@dataclass(frozen=True)
class Not:
    child: "Formula"


@dataclass(frozen=True)
class And:
    left: "Formula"
    right: "Formula"


@dataclass(frozen=True)
class Or:
    left: "Formula"
    right: "Formula"


@dataclass(frozen=True)
class Next:
    child: "Formula"


@dataclass(frozen=True)
class Globally:
    child: "Formula"


@dataclass(frozen=True)
class Eventually:
    child: "Formula"


@dataclass(frozen=True)
class Until:
    left: "Formula"
    right: "Formula"


Formula = AP | Not | And | Or | Next | Globally | Eventually | Until


def X(child: Formula) -> Next:
    return Next(child)


def G(child: Formula) -> Globally:
    return Globally(child)


def F(child: Formula) -> Eventually:
    return Eventually(child)


def U(left: Formula, right: Formula) -> Until:
    return Until(left, right)
