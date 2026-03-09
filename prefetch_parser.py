import os
import sys
import sqlite3
from datetime import datetime, timedelta
from decompress import DecompressWin


DB_NAME = "prefetch.db"

# чтение значения (4 байта)
def read_uint32(data, offset):
    return int.from_bytes(data[offset:offset+4], "little")

# чтение значения (8 байт)
def read_uint64(data, offset):
    return int.from_bytes(data[offset:offset+8], "little")

# чтение строки в utf-16
def read_string_utf16(data, offset, length):
    raw = data[offset:offset+length]
    return raw.decode("utf-16", errors="ignore").rstrip("\x00")

# преобразование временной метки 8 байт
def filetime_to_dt(filetime):

    if filetime == 0:
        return ""

    epoch = datetime(1601, 1, 1)
    seconds = filetime / 10000000
    dt = epoch + timedelta(seconds=seconds)

    return dt.strftime("%Y.%m.%d %H:%M:%S")

# создание бд
def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Data(
        Filename TEXT,
        process_EXE TEXT,
        file_size INTEGER,
        volume_serial INTEGER,
        volume_creation_time TEXT,
        run_count INTEGER,
        last_run_time TEXT,
        files TEXT,
        directories TEXT
    )
    """)

    conn.commit()
    return conn

# парсер
def parse_pf(data, Filename):

    version = read_uint32(data, 0)
    process_EXE = read_string_utf16(data, 16, 60)
    file_size = read_uint32(data, 12)
    run_count = read_uint32(data, 200)

    # достаем временные метки
    run_times = []
    run_time_offset = 128

    for i in range(8):

        ft = read_uint64(data, run_time_offset + i*8)
        dt = filetime_to_dt(ft)

        # только ненулевые метки времени
        if dt:
            run_times.append(dt)

    last_run_time = ", ".join(run_times)

    # Volume info offset
    volume_offset = read_uint32(data, 108)

    # числовое значение серийного номера тома в бинарном виде
    volume_serial_raw = read_uint32(data, volume_offset + 16)
    # преобразуем в hex
    volume_serial = f"{volume_serial_raw:X}"

    volume_creation = read_uint64(data, volume_offset + 8)

    volume_creation_time = filetime_to_dt(volume_creation)

    # File list
    filenames_offset = read_uint32(data, 100)
    filenames_size = read_uint32(data, 104)
    files_raw = data[filenames_offset:filenames_offset+filenames_size]

    # список файлов через 0х00 байт
    files = files_raw.decode("utf-16", errors="ignore").split("\x00")
    files = [f for f in files if f.strip()]
    files_str = "\n".join(files)

    # собираем уникальные папки
    directories = set()

    for f in files:
        directory = os.path.dirname(f)
        if directory:
            directories.add(directory)
    dirs_str = "\n".join(directories)

    return {
        "Filename": Filename,
        "process_EXE": process_EXE,
        "file_size": file_size,
        "volume_serial": volume_serial,
        "volume_creation_time": volume_creation_time,
        "run_count": run_count,
        "last_run_time": last_run_time,
        "files": files_str,
        "directories": dirs_str
    }

# записываем в бд
def save_to_db(conn, data):

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO Data VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        data["Filename"],
        data["process_EXE"],
        data["file_size"],
        data["volume_serial"],
        data["volume_creation_time"],
        data["run_count"],
        data["last_run_time"],
        data["files"],
        data["directories"]
    ))

    conn.commit()

# работа с /Prefetch
def process_directory(path):

    # находим и распаковываем файлы .pf
    decompressor = DecompressWin()
    conn = init_db()
    files = [f for f in os.listdir(path) if f.lower().endswith(".pf")]
    total = len(files)

    for i, file in enumerate(files, 1):
        full_path = os.path.join(path, file)
        print(f"[{i}/{total}] Processing {file}")

        data = decompressor.decompress(full_path)

        if data is None:
            print("Decompression failed")
            continue

        # парсим и сохраняем в бд
        parsed = parse_pf(data, file)
        save_to_db(conn, parsed)

    conn.close()
    print("\nProcessing completed. Check db file")

# проверка аргументов запуска
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python prefetch_parser.py <path_to_pf_folder>")
        sys.exit(1)

    directory = sys.argv[1]
    process_directory(directory)
