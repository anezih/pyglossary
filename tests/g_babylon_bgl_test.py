import sys
from os.path import dirname, abspath, join
import unittest
import hashlib

rootDir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, rootDir)

from tests.glossary_test import TestGlossaryBase
from pyglossary.glossary import Glossary


class TestGlossaryStarDict(TestGlossaryBase):
	def __init__(self, *args, **kwargs):
		TestGlossaryBase.__init__(self, *args, **kwargs)

		self.dataFileCRC32.update({
			"Flavours_of_Malaysia.bgl": "46ef154b",
			"Flavours_of_Malaysia.txt_res/icon1.ico": "76a3b4c3",
			"Currency_In_Each_Country.bgl": "309f1b3f",
			"Solar_Physics_Glossary.bgl": "cc8f5ca1",
			"Farsi_Aviation_Dictionary.bgl": "efa7bee4",
		})

	def convert_bgl_txt(
		self,
		fname,
		sha1sum=None,
		md5sum=None,
		resFiles=None,
		**convertArgs
	):
		inputFilename = self.downloadFile(f"{fname}.bgl")
		outputFname = f"{fname}-2.txt"
		outputFilename = self.newTempFilePath(outputFname)

		if resFiles is None:
			resFiles = {}
		resFilesPath = {
			resName: self.newTempFilePath(join(f"{outputFname}_res", resName))
			for resName in resFiles
		}

		glos = self.glos = Glossary()
		res = glos.convert(
			inputFilename=inputFilename,
			outputFilename=outputFilename,
			**convertArgs
		)
		self.assertEqual(outputFilename, res)

		if sha1sum:
			with open(outputFilename, mode="rb") as _file:
				actualSha1 = hashlib.sha1(_file.read()).hexdigest()
			self.assertEqual(actualSha1, sha1sum)

		if md5sum:
			with open(outputFilename, mode="rb") as _file:
				actualMd5 = hashlib.md5(_file.read()).hexdigest()
			self.assertEqual(actualMd5, md5sum)

		for resName in resFiles:
			resPathActual = resFilesPath[resName]
			resPathExpected = self.downloadFile(f"{fname}.txt_res/{resName}")
			self.compareBinaryFiles(resPathActual, resPathExpected)

	def test_convert_bgl_txt_1(self):
		self.convert_bgl_txt(
			"Flavours_of_Malaysia",
			sha1sum="2b1fae135df2aaaeac23fb1dde497a4b6a22fd95",
			resFiles=["icon1.ico"],
		)

	def test_convert_bgl_txt_2(self):
		self.convert_bgl_txt(
			"Currency_In_Each_Country",
			sha1sum="731147c72092d813dfe1ab35d420477478832443",
		)

	def test_convert_bgl_txt_3(self):
		self.convert_bgl_txt(
			"Solar_Physics_Glossary",
			sha1sum="f30b392c748c4c5bfa52bf7f9945c574617ff74a",
		)

	def test_convert_bgl_txt_4(self):
		self.convert_bgl_txt(
			"Farsi_Aviation_Dictionary",
			sha1sum="b5741bf7ca4306f76ba414fe8efb637c59999d2b",
		)


if __name__ == "__main__":
	unittest.main()