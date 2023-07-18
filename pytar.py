import tarfile
import io

from datetime import datetime

class Tar:
    def __init__(
        self,
        name: str,
        mode: str = 'x:gz',
        encoding: str = 'utf-8',
        compresslevel: int = 9,
    ):
        self._name = name
        self._mode = mode
        self._encoding = encoding
        self._compresslevel = compresslevel

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
