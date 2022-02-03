use serde::Serialize;
use std::{collections::HashMap, fs, io, path::PathBuf};

use crate::models::mimetype::MimeType;

#[derive(Debug, Serialize)]
pub struct SharedPathState {
    pub root: PathBuf,
    pub paths: HashMap<PathBuf, SharedPath>,
}

impl From<SharedPath> for SharedPathState {
    fn from(path: SharedPath) -> Self {
        let key = "~";

        let mut paths = HashMap::new();
        if let PathType::Dir(children) = &path.specific {
            // populate child paths into the cache
            if let Some(children) = &children {
                for child in children {
                    let value =
                        SharedPath::with_parent(PartialPath::from(&path), child.path.clone())
                            .unwrap();

                    paths.insert(value.key.clone(), value);
                }
            }
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
        let result: Option<(PartialPath, Vec<PathBuf>)> = {
            let shared = match self.paths.get_mut(path) {
                Some(shared) => shared,
                None => return Ok(()),
            };

            if let PathType::Dir(paths) = &mut shared.specific {
                if let Some(_) = &paths {
                    return Ok(());
                }

                let read_result = fs::read_dir(&shared.path)?;

                let mut children = vec![];
                let mut subpaths = vec![];
                for entry in read_result {
                    let entry_path = entry?.path();

                    children.push(PartialPath {
                        key: shared.key.join(entry_path.file_name().unwrap()),
                        path: entry_path.clone(),
                    });

                    subpaths.push(entry_path);
                }

                shared.specific = PathType::Dir(Some(children));

                Some((shared.into(), subpaths))
            } else {
                None
            }
        };

        // add new paths to cache
        if let Some((parent, subpaths)) = result {
            println!("Visit {:?}: {} children", parent, subpaths.len());
            for subpath in subpaths {
                let value = SharedPath::with_parent(parent.clone(), subpath)?;
                self.paths.insert(value.key.clone(), value);
            }
        }

        Ok(())
    }
}

#[derive(Debug, Serialize)]
pub struct SharedPath {
    pub parent: Option<PartialPath>,
    pub name: String,
    pub path: PathBuf,
    pub specific: PathType,
    pub key: PathBuf,
}

#[derive(Debug, Serialize)]
#[serde(tag = "tag", content = "content")]
pub enum PathType {
    File(FileData),
    Dir(Option<Vec<PartialPath>>),
}

#[derive(Debug, Serialize, Clone)]
pub struct PartialPath {
    pub key: PathBuf,
    pub path: PathBuf,
}

#[derive(Debug, Serialize)]
pub struct FileData {
    mime_type: MimeType,
}

impl From<&SharedPath> for PartialPath {
    fn from(path: &SharedPath) -> Self {
        Self {
            key: path.key.clone(),
            path: path.path.clone(),
        }
    }
}

impl From<&mut SharedPath> for PartialPath {
    fn from(path: &mut SharedPath) -> Self {
        Self {
            key: path.key.clone(),
            path: path.path.clone(),
        }
    }
}

impl SharedPath {
    pub fn root(paths: Vec<String>) -> io::Result<Self> {
        let children = Self::root_children(paths)?;

        Ok(Self {
            parent: None,
            name: String::from("~"),
            key: PathBuf::from(""),
            path: PathBuf::from("~"),
            specific: PathType::Dir(Some(children)),
        })
    }

    fn root_children(children: Vec<String>) -> io::Result<Vec<PartialPath>> {
        let mut child_paths = Vec::with_capacity(children.len());
        for child in children {
            let path = fs::canonicalize(child)?;
            let key = PathBuf::from(path.file_name().unwrap());

            child_paths.push(PartialPath { key, path });
        }

        Ok(child_paths)
    }

    pub fn with_parent(parent: PartialPath, path: PathBuf) -> io::Result<Self> {
        let path = fs::canonicalize(path)?;
        let name = path.file_name().unwrap().to_string_lossy().to_string();
        let key = parent.key.join(path.file_name().unwrap());

        let md = path.metadata()?;
        let specific = if md.is_dir() {
            PathType::Dir(None)
        } else {
            PathType::File(FileData {
                mime_type: MimeType::from(&path),
            })
        };

        Ok(Self {
            parent: Some(parent),
            name,
            path,
            key,
            specific,
        })
    }
}
