from pathlib import Path
from re import search
from ..fileselection import FileSelection

class NonEmptyStringValidator:
    @staticmethod
    def validate(*args):
        testlist = [x for x in args if x is None or len(x) == 0]
        return len(testlist) == 0

class PathEntryValidator:
    @staticmethod
    def validateall(strdir, strscan, strpoint):
        if not NonEmptyStringValidator.validate(strdir, strscan, strpoint):
            return False, [], "Text entries cannot be empty."

        dirpath = None
        if Path(strdir).exists() and len(strdir) > 0:
            dirpath = Path(strdir)
            filepaths = sorted(dirpath.glob("*.h5"))
            scanpaths = [x for x in filepaths if search(strscan, x.name) is not None]
            pointpaths = [y for y in scanpaths if search(strpoint, y.name) is not None]

            if len(pointpaths) == 0:
                return False, [], "No files found."
            else:
                sel = FileSelection(strdir, strscan, strpoint, pointpaths)
                return True, sel, "SUCCESS!"
        else:
            return False, [], "Invalid directory."

