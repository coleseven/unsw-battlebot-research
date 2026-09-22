"""Decode .replay files (local `unswbc run` output, or gzip'd server replays).

The format is a packed Cap'n Proto message; the schema below was read off
the official replay viewer. Usage:

    rp = load("data/replays/52968.replay")
    rp.map_text, rp.bot_a, rp.bot_b, rp.result
    for ev in rp.events: ...          # tuples, see EVENT_* below
"""

from __future__ import annotations

import gzip
import pathlib
import struct
from dataclasses import dataclass

DIRS = "NESW"
DEATH = "WSOHA"   # hit wall, self, other body, head-to-head, no valid action

# Event tuples (first field is the kind):
ROUND_START = 0        # (0, round)
TURN_START = 1         # (1, id)
PEARL_COUNTDOWN = 2    # (2, x, y, countdown)
TILE_CHANGE = 3        # (3, x, y, has_pearl)
DRAGON_ACTION = 4      # (4, id, action, points or None, exceeded, tle)
#                        action: ("move", "NNE") | ("split", n) | ("suicide",) | None
ENGINE_LOG = 5         # (5, id, text)
DRAGON_LOG = 6         # (6, id, text)
DRAGON_INDICATOR = 7   # (7, id, text)
DEBUG_DRAW = 8         # (8, id, shape, (x1, y1), (x2, y2), (r, g, b))
DRAGON_UPDATE = 9      # (9, id, facing, (hx, hy), (tx, ty))
DRAGON_SPLIT = 10      # (10, parent, child, team, child_facing, parent_body, child_body)
DRAGON_DEATH = 11      # (11, id, reason letter)
SONAR_PING = 12        # (12, sender, direction, value, origin, end, hit_id or None)


def unpack(data: bytes) -> bytes:
    out = bytearray()
    i, n = 0, len(data)
    while i < n:
        tag = data[i]
        i += 1
        if tag == 0:
            out += bytes(8 * (1 + data[i]))
            i += 1
            continue
        word = bytearray(8)
        for b in range(8):
            if tag & (1 << b):
                word[b] = data[i]
                i += 1
        out += word
        if tag == 0xFF:
            count = data[i]
            i += 1
            out += data[i:i + 8 * count]
            i += 8 * count
    return bytes(out)


class _Msg:
    def __init__(self, raw: bytes) -> None:
        count = struct.unpack_from("<I", raw, 0)[0] + 1
        sizes = struct.unpack_from(f"<{count}I", raw, 4)
        off = 4 + 4 * count
        off += (-off) % 8
        self.segs = []
        for s in sizes:
            self.segs.append(memoryview(raw)[off:off + 8 * s])
            off += 8 * s

    def word(self, seg: int, w: int) -> int:
        return struct.unpack_from("<Q", self.segs[seg], 8 * w)[0]

    def _follow(self, seg: int, w: int):
        """Resolve the pointer at (seg, w) through far pointers.
        Returns (seg, pointer word, target word index) or None if null."""
        p = self.word(seg, w)
        if p == 0:
            return None
        if p & 3 == 2:  # far pointer
            double = (p >> 2) & 1
            pad = (p >> 3) & 0x1FFFFFFF
            seg = p >> 32
            if not double:
                p = self.word(seg, pad)
                off = _signed30(p >> 2)
                return seg, p, pad + 1 + off
            land = self.word(seg, pad)
            tag = self.word(seg, pad + 1)
            return land >> 32, tag, (land >> 3) & 0x1FFFFFFF
        return seg, p, w + 1 + _signed30(p >> 2)

    def struct(self, seg: int, w: int):
        r = self._follow(seg, w)
        if r is None:
            return None
        seg, p, target = r
        return _Struct(self, seg, target, (p >> 32) & 0xFFFF, p >> 48)

    def list(self, seg: int, w: int):
        r = self._follow(seg, w)
        if r is None:
            return None
        seg, p, target = r
        esize = (p >> 32) & 7
        count = p >> 35
        return seg, target, esize, count


def _signed30(v: int) -> int:
    v &= 0x3FFFFFFF
    return v - (1 << 30) if v & (1 << 29) else v


class _Struct:
    __slots__ = ("m", "seg", "w", "dw", "pw")

    def __init__(self, m: _Msg, seg: int, w: int, dw: int, pw: int) -> None:
        self.m, self.seg, self.w, self.dw, self.pw = m, seg, w, dw, pw

    def _get(self, fmt: str, byte: int, size: int):
        if byte + size > 8 * self.dw:
            return 0
        return struct.unpack_from(fmt, self.m.segs[self.seg], 8 * self.w + byte)[0]

    def i32(self, b): return self._get("<i", b, 4)
    def u32(self, b): return self._get("<I", b, 4)
    def u16(self, b): return self._get("<H", b, 2)
    def u8(self, b): return self._get("<B", b, 1)
    def u64(self, b): return self._get("<Q", b, 8)

    def bit(self, n: int) -> bool:
        return bool(self.u8(n // 8) >> (n % 8) & 1)

    def ptr_index(self, i: int) -> int | None:
        return None if i >= self.pw else self.w + self.dw + i

    def struct(self, i: int):
        w = self.ptr_index(i)
        return None if w is None else self.m.struct(self.seg, w)

    def text(self, i: int) -> str:
        w = self.ptr_index(i)
        r = None if w is None else self.m.list(self.seg, w)
        if r is None:
            return ""
        seg, target, _, count = r
        return bytes(self.m.segs[seg][8 * target:8 * target + count - 1]).decode(errors="replace")

    def u16_list(self, i: int) -> list[int]:
        w = self.ptr_index(i)
        r = None if w is None else self.m.list(self.seg, w)
        if r is None:
            return []
        seg, target, _, count = r
        return list(struct.unpack_from(f"<{count}H", self.m.segs[seg], 8 * target))

    def struct_list(self, i: int) -> list["_Struct"]:
        w = self.ptr_index(i)
        r = None if w is None else self.m.list(self.seg, w)
        if r is None:
            return []
        seg, target, esize, count = r
        assert esize == 7, "expected a composite list"
        tag = self.m.word(seg, target)
        n = _signed30(tag >> 2)
        dw, pw = (tag >> 32) & 0xFFFF, tag >> 48
        step = dw + pw
        return [_Struct(self.m, seg, target + 1 + k * step, dw, pw) for k in range(n)]


def _pt(s: _Struct | None) -> tuple[int, int]:
    return (s.i32(0), s.i32(4)) if s is not None else (-1, -1)


def _event(e: _Struct):
    kind = e.u16(0)
    s = e.struct(0)
    if kind == ROUND_START:
        return (0, s.i32(0))
    if kind == TURN_START:
        return (1, s.i32(0))
    if kind == PEARL_COUNTDOWN:
        x, y = _pt(s.struct(0))
        return (2, x, y, s.i32(0))
    if kind == TILE_CHANGE:
        x, y = _pt(s.struct(0))
        return (3, x, y, s.bit(0))
    if kind == DRAGON_ACTION:
        a = s.struct(0)
        action = None
        if a is not None:
            which = a.u16(0)
            if which == 0:
                action = ("move", "".join(DIRS[d] for d in a.u16_list(0)))
            elif which == 1:
                action = ("split", a.i32(4))
            else:
                action = ("suicide",)
        ins = s.struct(1)
        points = ins.u64(0) if ins is not None else None
        exceeded = ins.bit(64) if ins is not None else False
        return (4, s.i32(0), action, points, exceeded, s.bit(32))
    if kind in (ENGINE_LOG, DRAGON_LOG, DRAGON_INDICATOR):
        return (kind, s.i32(0), s.text(0))
    if kind == DEBUG_DRAW:
        d = s.struct(0)
        return (8, s.i32(0), d.u16(0), _pt(d.struct(0)), _pt(d.struct(1)), (d.u8(2), d.u8(3), d.u8(4)))
    if kind == DRAGON_UPDATE:
        return (9, s.i32(0), DIRS[s.u16(4)], _pt(s.struct(0)), _pt(s.struct(1)))
    if kind == DRAGON_SPLIT:
        return (10, s.i32(0), s.i32(4), "AB"[s.u16(8)], DIRS[s.u16(10)],
                [_pt(p) for p in s.struct_list(0)], [_pt(p) for p in s.struct_list(1)])
    if kind == DRAGON_DEATH:
        return (11, s.i32(0), DEATH[s.u16(4)])
    if kind == SONAR_PING:
        hit = s.i32(12) if s.u16(6) == 1 else None
        return (12, s.i32(0), DIRS[s.u16(4)], s.u32(8), _pt(s.struct(0)), _pt(s.struct(1)), hit)
    raise ValueError(f"unknown event kind {kind}")


@dataclass
class Replay:
    format_version: int
    map_text: str
    bot_a: str
    bot_b: str
    events: list
    result: dict

    @property
    def map_name(self) -> str:
        for line in self.map_text.splitlines():
            if line.startswith("MAP_NAME"):
                return line.split(None, 1)[1].strip()
        return ""


def decode(blob: bytes) -> Replay:
    if blob[:2] == b"\x1f\x8b":
        blob = gzip.decompress(blob)
    m = _Msg(unpack(blob))
    root = m.struct(0, 0)
    res = root.struct(4)
    result = {}
    if res is not None:
        team = lambda t: None if t is None else {  # noqa: E731
            "dragons": t.i32(0), "longest": t.i32(4), "total": t.i32(8)}
        result = {
            "terminated": res.bit(0),
            "end_reason": ("eliminated", "round_limit")[res.u16(2)] if res.u16(2) < 2 else res.u16(2),
            "winner": "AB"[res.u16(6)] if res.u16(4) == 1 else None,
            "a": team(res.struct(0)),
            "b": team(res.struct(1)),
        }
    events = [_event(e) for e in root.struct_list(3)]
    return Replay(root.u32(0), root.text(0), root.text(1), root.text(2), events, result)


def load(path) -> Replay:
    return decode(pathlib.Path(path).read_bytes())
