import tarfile
import io
import re

from datetime import datetime

class TarModeError(tarfile.TarError):
    """ Raised when given a name without a proper extension """

class Tar:
    _MODE_REGEX = '\.tar\.(gz|xz|bz2)$'

    def __init__(
        self,
        name: str,
        encoding: str = 'utf-8',
        compresslevel: int = 9,
    ):
        self._name = name
        self._mode = self._extract_mode(name)

        self._encoding = encoding
        self._compresslevel = compresslevel

    def _extract_mode(self, name: str) -> str:
        if mode_match := re.findall(self._MODE_REGEX, name):
            return f'x:{mode_match[0]}'

        raise TarModeError('File name does not contain a valid tar mode')

    def _create(self):
        return tarfile.open(name=self._name,
                            mode=self._mode,
                            compresslevel=self._compresslevel)

    def __enter__(self):
        self._tar = self._create()

        return self

    def __exit__(self, *args, **kwargs):
        self._tar.close()

    def _create_tar_info(self, name: str, size: int) -> tarfile.TarInfo:
        tar_info = tarfile.TarInfo(name)
        tar_info.size = size
        tar_info.mtime = datetime.now().timestamp()

        return tar_info

    def _create_data_io(self, data: bytes) -> io.BytesIO:
        return io.BytesIO(initial_bytes=data)

    def add_file(self, name: str, buf: str) -> None:
        enc_buf = buf.encode(self._encoding)

        info = self._create_tar_info(name, len(enc_buf))
        data_io = self._create_data_io(enc_buf) 

        self._tar.addfile(info, data_io)
