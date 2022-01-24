use rocket::figment::value;
use serde::Serialize;
use std::{collections::HashMap, error::Error, fs, io, path::PathBuf, rc::Rc};

#[derive(Debug, Serialize)]
pub struct SharedPathState {
    pub root: String,
    pub paths: HashMap<String, SharedPath>,
}

impl From<SharedPath> for SharedPathState {
    fn from(path: SharedPath) -> Self {
        let key = "~";

        let mut paths = HashMap::new();
        if let SharedType::Dir(dir) = &path.shared {
            if let Some(children) = &dir.children {
                for child in children {
                    let value =
                        SharedPath::with_parent(path.relative.clone(), child.clone()).unwrap();

                    paths.insert(value.key(), value);
                }
            }
        };

        paths.insert(String::from(""), path);

        Self {
            root: String::from(key),
            paths,
        }
    }
}

impl SharedPathState {
    // pub fn visit(&mut self, path: &mut SharedPath) -> io::Result<()> {
    //     if let SharedType::Dir(dir) = &path.shared {
    //         let read_result = fs::read_dir(&path.shared.path())?;
    //         let mut children: Vec<String> = vec![];

    //         for entry in read_result {
    //             let entry_path = entry?.path();

    //             children.push(entry_path.file_name().unwrap().to_string_lossy().into());
    //             SharedPath::with_parent(path);
    //         }

    //         if let Some(children) = &dir.children {
    //             for child in children {
    //                 let value =
    //                     SharedPath::with_parent(path.relative.clone(), child.clone()).unwrap();

    //                 paths.insert(value.key(), value);
    //             }
    //         }
    //     };

    //     Ok(())
    // }
}

#[derive(Debug, Serialize)]
pub struct SharedPath {
    pub parent: Option<PathBuf>,
    pub shared: SharedType,
    pub relative: PathBuf,
}

impl SharedPath {
    pub fn root(paths: Vec<String>) -> Result<Self, Box<dyn Error>> {
        let children = paths.iter().cloned().collect();
        let shared = SharedType::Dir(SharedDir::with(PathBuf::from("~"), Some(children)));

        Ok(Self {
            parent: None,
            relative: PathBuf::from(""),
            shared,
        })
    }

    pub fn with_parent(parent: PathBuf, path: String) -> Result<Self, Box<dyn Error>> {
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
    pub fn key(&self) -> String {
        self.relative
            .clone()
            .into_os_string()
            .to_string_lossy()
            .into()
    }
}

#[derive(Debug, Serialize)]
#[serde(tag = "tag", content = "content")]
pub enum SharedType {
    File(SharedFile),
    Dir(SharedDir),
}

impl SharedType {
    pub fn from(path: String) -> Result<Self, Box<dyn Error>> {
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
}

#[derive(Debug, Serialize)]
pub struct SharedDir {
    pub path: PathBuf,
    pub children: Option<Vec<String>>,
}

impl SharedDir {
    fn with(path: PathBuf, children: Option<Vec<String>>) -> Self {
        Self { path, children }
    }
}

impl From<PathBuf> for SharedDir {
    fn from(path: PathBuf) -> Self {
        Self {
            path,
            children: None,
        }
    }
}

#[derive(Debug, Serialize)]
pub struct SharedFile {
    pub path: PathBuf,
}

impl From<PathBuf> for SharedFile {
    fn from(path: PathBuf) -> Self {
        Self { path }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn new_shared_path_from() {
        let result = SharedType::from(".".to_string());

        println!("{:?}", result);
        assert_eq!(result.is_ok(), true);
    }
}

// TEST

#[derive(Debug)]
struct Hold {
    pub current: String,
    pub items: HashMap<String, Item>,
}

#[derive(Debug)]
struct Item(Rc<i32>);

impl Hold {
    pub fn from(items: Vec<i32>) -> Self {
        let items: HashMap<String, Item> = items
            .into_iter()
            .map(|i| (i.to_string(), Item(Rc::new(i))))
            .collect();

        Hold {
            items,
            current: "0".to_string(),
        }
    }
}

#[cfg(test)]
mod temp_tests {
    use super::*;

    #[test]
    fn new_hold_from() {
        let result = Hold::from(vec![0, 1, 2, 3]);

        println!("{:?}", result);
    }
}
