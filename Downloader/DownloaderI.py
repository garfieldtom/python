#-*- coding:utf-8 -*-

from urllib.request import *
from threading import *
import time
import os

PIECE_SIZE = 1024
class Block:
    def __init__(self, fileInfo, startPiece, endPiece, last = False, lastSize = None):
        self.fileInfo = fileInfo
        self.startPiece = startPiece
        self.endPiece = endPiece
        self.last = last
        self.lastSize = lastSize
        # [startPos, endPos]闭区间
        self.startPos = PIECE_SIZE * startPiece
        if not self.last:
            self.endPos = PIECE_SIZE * endPiece - 1
        else:
            self.endPos = PIECE_SIZE * endPiece - (PIECE_SIZE - lastSize) - 1
        print("range:(%d-%d)"%(self.startPos, self.endPos))


    def getNext(self):
        s = -1
        e = self.endPiece
        #print(self.fileInfo.pieceMap[self.startPiece:self.endPiece])
        for i in range(self.startPiece, self.endPiece):
            if s == -1 and self.fileInfo.pieceMap[i] == ord('0'):
                s = i
            if s >= 0 and self.fileInfo.pieceMap[i] == ord('1'):
                e = i
                break
        print("getNext.raw(", s, e, ")")
        if s >= 0 and e > s:
            start = PIECE_SIZE * s
            end = PIECE_SIZE * e
            if end > self.endPos:
                end = self.endPos
            self.pos = start
            print("getNext.result(%d, %d)"%(start, end))
            return (start, end)
        else:
            return None


    def write(self, data):
        self.fileInfo.write(self.pos, data)
        with self.fileInfo.lock:
            s = self.pos
            self.pos += len(data)
            e = self.pos
            if self.last and self.pos >= self.endPos:
                self.fileInfo.pieceMap[self.endPiece - 1] = ord('1')
                #print("set(%d)"%(self.endPiece - 1))
            sp = s // PIECE_SIZE
            ep = e // PIECE_SIZE
            for i in range(sp, ep):
                self.fileInfo.pieceMap[i] = ord('1')
                #print("set(%d)"%i)
            #self.fileInfo.saveInfo()


class FileInfo:
    def __init__(self, fileName, fileSize, numBlocks = 4):
        self.fileName = fileName
        self.fileSize = fileSize
        self.numBlocks = numBlocks
        try:
            self.file = open(self.downname(), "rb+")
        except:
            self.file = open(self.downname(), "wb")
        self.file.truncate(fileSize)
        self.lock = Lock()


        d, v = divmod(fileSize, PIECE_SIZE)
        if v:
            d += 1
        self.numPieces = d
        self.piecePad = 0
        self.pieceCount = d // 8
        if d % 8:
            self.pieceCount + 1
            self.piecePad = 8 - d % 8
        self.pieceMap = bytearray(b"0"*d + b"1" * self.piecePad)
        self.lastPieceSize = v
        pb = self.numPieces // self.numBlocks
        r = []
        for i in range(self.numBlocks):
            r.append(i * pb)
        r.append(self.numPieces)
        self.range = r
        self.blocks = []
        for i in range(self.numBlocks):
            self.blocks.append(Block(self, self.range[i], self.range[i + 1], i == self.numBlocks - 1, self.lastPieceSize))
        print("fileName:%s, size:%d, blocks:%d, pieces:%d, last:%d, range:%s"%(self.fileName, self.fileSize, self.numBlocks, self.numPieces, self.lastPieceSize, self.range))
        self.load()


    def write(self, pos, data):
        with self.lock:
            #print("file.pos = ", self.file.tell())
            #print("write(%d, %d)"%(pos, len(data)))
            self.file.seek(pos)
            self.file.write(data)
    def downname(self):
        return self.fileName + ".down"
    def infoname(self):
        return self.fileName + "info.txt"
    def saveInfo(self):
        with open(self.infoname(), "wb") as inf:
            inf.write(self.bits2hex(self.pieceMap))
    def load(self):
        if os.path.exists(self.infoname()):
            print("****************info.size:", os.path.getsize(self.infoname()), "pieces:", len(self.pieceMap))
        if os.path.exists(self.downname()) and os.path.exists(self.infoname()) and os.path.getsize(self.downname()) == self.fileSize:
            data = open(self.infoname(), "rb").read()
            data = self.hex2bits(data)
            self.pieceMap = bytearray(data)
            print("load:", self.pieceMap)
    def close(self):
        self.file.close()
        os.rename(self.downname(), self.fileName)
        os.remove(self.infoname())
    def bits2hex(self, bits):
        #print("bits:", bits)
        v = int(bits, 2)
        return bytes(hex(v)[2:], "ascii")


    def hex2bits(self, bs):
        #print("hex2bits(", bs, ")")
        v = int(bs, 16)
        return bytes(bin(v)[2:], "ascii")


class DownTask(Thread):
    def __init__(self, url, block):
        self.url = url
        self.block = block
        self.stopIt = False
        super().__init__()


    def run(self):
        print("Task(%s).run(%d, %d) begin"%(self.name, self.block.startPiece, self.block.endPiece))
        while not self.stopIt:
            rg = self.block.getNext()
            print("range:", rg)
            if rg:
                len = rg[1] - rg[0] + 1
                r = Request(url = self.url)
                r.add_header("Range", "bytes=%d-%d"%(rg[0], rg[1]))
                print(r.header_items())
                con = urlopen(r)
                print(con.info().as_string())
                while 1:
                    data = con.read(133)
                    if data:
                        self.block.write(data)
                    else:
                        break
            else:
                break
        print("Task(%s).run(%d, %d) end"%(self.name, self.block.startPiece, self.block.endPiece))
    def stop(self):
        self.stopIt = True


class Downloader:
    def __init__(self, url, numThread = 4, filename = None):
        self.url = url
        self.numThread = numThread
        self.filename = filename if filename else os.path.split(url)[1]


    def start(self):
        con = urlopen(self.url)
        print(con.info().as_string())
        supp = con.headers.get("Accept-Ranges")
        if supp:
            if supp.lower() == "none":
                supp = False
        length = int(con.headers.get("Content-length", "0"))
        cd = con.headers.get("Content-Disposition")
        self._fileName = None
        if cd:
            cd = cd.lower()
            if "filename=" in cd:
                self._filename = cd.split("filename=")[1]


        if supp:
            con.close()
            self.tasks = []
            self.fileInfo = FileInfo(self.filename, length, self.numThread)
            for b in self.fileInfo.blocks:
                self.tasks.append(DownTask(self.url, b))
            for t in self.tasks:
                t.start()
            while any(map(lambda t:t.isAlive(), self.tasks)):
                time.sleep(0.5)
                print(self.fileInfo.bits2hex(self.fileInfo.pieceMap))
                self.fileInfo.saveInfo()
            self.fileInfo.close()
        else:
            while 1:
                f = open(self.fileName, "wb")
                data = con.read(133)
                if data:
                    f.write(data)
                else:
                    break
            f.close()
            con.close()
                

d = Downloader("http://www.python.org/ftp/python/3.2.1/python-3.2.1.msi", 6)
d.start()