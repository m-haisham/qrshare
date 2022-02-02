use std::{
    ffi::OsStr,
    fs::File,
    io::{Cursor, Read, Write},
    path::{Path, PathBuf},
};

use walkdir::WalkDir;
use zip::{result::ZipResult, write::FileOptions, CompressionMethod, ZipWriter};

pub fn zip_dir(src: &PathBuf) -> ZipResult<Vec<u8>> {
    let cursor = Cursor::new(Vec::new());
    let mut zip = ZipWriter::new(cursor);
    let options = FileOptions::default()
        .compression_method(CompressionMethod::Deflated)
        .unix_permissions(0o755);

    let walkdir = WalkDir::new(src);
    let it = walkdir.into_iter().filter_map(|e| e.ok());
    let mut buffer = Vec::new();
    for entry in it {
        let path = entry.path();
        let name = path.strip_prefix(src).unwrap();

        if path.is_file() {
            zip.start_file(path_string(name), options)?;

            let mut file = File::open(path)?;
            file.read_to_end(&mut buffer)?;
            zip.write_all(&buffer)?;
            buffer.clear();
        } else {
            zip.add_directory(path_string(name), options)?;
        }
    }

    Ok(zip.finish()?.into_inner())
}

pub fn path_string(path: &Path) -> String {
    let mut it = path.iter();

    let mut segments = match it.next() {
        Some(value) if value == OsStr::new(&std::path::MAIN_SEPARATOR.to_string()) => Vec::new(),
        Some(value) => vec![value.to_string_lossy()],
        None => return String::new(),
    };

    segments.extend(it.map(|s| s.to_string_lossy()));
    segments.join("/")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_path_string() {
        let paths = vec![
            (Path::new("/path/to"), "path/to"),
            (Path::new("another/path/to"), "another/path/to"),
            (Path::new(""), ""),
        ];

        for (path, expected) in paths {
            assert_eq!(path_string(path), expected);
        }
    }
}
