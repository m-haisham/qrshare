use serde::Serialize;
use std::{collections::HashMap, fs, io, path::PathBuf};

#[derive(Debug, Serialize)]
pub struct SharedPathState {
    pub root: PathBuf,
    pub paths: HashMap<PathBuf, SharedPath>,
}

impl From<SharedPath> for SharedPathState {
    fn from(mut path: SharedPath) -> Self {
        let key = "~";

        let mut paths = HashMap::new();
        if let SharedType::Dir(dir) = &mut path.shared {
            // populate child paths into the cache
            if let Some(children) = &dir.children {
                for child in children {
                    let value =
                        SharedPath::with_parent(path.relative.clone(), child.clone()).unwrap();

                    paths.insert(value.key(), value);
                }
            }

            // the previous children are not normalized and can have
            // relative path such as "." and ".."
            // these woudnt map correctly in the cache
            dir.children = Some(
                paths
                    .iter()
                    .map(|(_, v)| PathBuf::from(v.shared.name()))
                    .collect(),
            );
        };

        // add home to cache
        paths.insert(PathBuf::from(""), path);

        Self {
            root: PathBuf::from(key),
            paths,
        }
    }
}

impl SharedPathState {
    pub fn visit(&mut self, path: &PathBuf) -> io::Result<()> {
        let result = {
            let path = match self.paths.get_mut(path) {
                Some(shared) => shared,
                None => return Ok(()),
            };

            if let SharedType::Dir(dir) = &mut path.shared {
                if let Some(_) = dir.children {
                    return Ok(());
                }

                let read_result = fs::read_dir(&dir.path)?;

                let mut children: Vec<PathBuf> = vec![];
                let mut subpaths = vec![];
                for entry in read_result {
                    let entry_path = entry?.path();

                    children.push(path.relative.join(entry_path.file_name().unwrap()));
                    subpaths.push(entry_path);
                }

                dir.children = Some(children);

                Some((path.relative.clone(), subpaths))
            } else {
                None
            }
        };

        // add new paths to cache
        if let Some((parent, subpaths)) = result {
            println!("Visit {:?}: {} children", parent, subpaths.len());
            for subpath in subpaths {
                let value = SharedPath::with_parent(parent.clone(), subpath)?;
                self.paths.insert(value.key(), value);
            }
        }

        Ok(())
    }
}

#[derive(Debug, Serialize)]
pub struct SharedPath {
    pub parent: Option<PathBuf>,
    pub shared: SharedType,
    pub relative: PathBuf,
}

impl SharedPath {
    pub fn root(paths: Vec<String>) -> io::Result<Self> {
        let children = paths.iter().map(|p| PathBuf::from(p)).collect();
        let shared = SharedType::Dir(SharedDir::with(PathBuf::from("~"), Some(children)));

        Ok(Self {
            parent: None,
            relative: PathBuf::from(""),
            shared,
        })
    }

    pub fn with_parent(parent: PathBuf, path: PathBuf) -> io::Result<Self> {
        let shared = SharedType::from(path)?;
        let relative = parent.join(shared.path().file_name().unwrap());

        Ok(Self {
            parent: Some(parent),
            shared,
            relative,
        })
    }
}

impl SharedPath {
    pub fn key(&self) -> PathBuf {
        self.relative.clone()
    }
}

#[derive(Debug, Serialize)]
#[serde(tag = "tag", content = "content")]
pub enum SharedType {
    File(SharedFile),
    Dir(SharedDir),
}

impl SharedType {
    pub fn from(path: PathBuf) -> io::Result<Self> {
        let buf = fs::canonicalize(path)?;
        let md = buf.metadata()?;

        let path = if md.is_dir() {
            Self::Dir(SharedDir::from(buf))
        } else {
            Self::File(SharedFile::from(buf))
        };

        Ok(path)
    }

    pub fn path(&self) -> &PathBuf {
        match self {
            SharedType::File(file) => &file.path,
            SharedType::Dir(dir) => &dir.path,
        }
    }

    pub fn name(&self) -> &String {
        match self {
            SharedType::File(file) => &file.name,
            SharedType::Dir(dir) => &dir.name,
        }
    }
}

#[derive(Debug, Serialize)]
pub struct SharedDir {
    pub name: String,
    pub path: PathBuf,
    pub children: Option<Vec<PathBuf>>,
}

impl SharedDir {
    fn with(path: PathBuf, children: Option<Vec<PathBuf>>) -> Self {
        let name = path.file_name().unwrap().to_string_lossy().to_string();

        Self {
            path,
            name,
            children,
        }
    }
}

impl From<PathBuf> for SharedDir {
    fn from(path: PathBuf) -> Self {
        let name = path.file_name().unwrap().to_string_lossy().to_string();

        Self {
            path,
            name,
            children: None,
        }
    }
}

#[derive(Debug, Serialize)]
pub struct SharedFile {
    pub name: String,
    pub path: PathBuf,
}

impl From<PathBuf> for SharedFile {
    fn from(path: PathBuf) -> Self {
        let name = path.file_name().unwrap().to_string_lossy().to_string();

        Self { path, name }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn new_shared_path_from() {
        let result = SharedType::from(PathBuf::from("."));

        println!("{:?}", result);
        assert_eq!(result.is_ok(), true);
    }
}
