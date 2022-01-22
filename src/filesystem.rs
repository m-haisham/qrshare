use serde::Serialize;
use std::{error::Error, fs};

#[derive(Debug, Serialize)]
pub struct SharedPath {
    pub parent: Option<Box<SharedPath>>,
    pub shared: SharedType,
}

impl SharedPath {
    pub fn from(paths: Vec<String>) -> Result<Self, Box<dyn Error>> {
        let mut children = Vec::with_capacity(paths.len());
        for path in paths.iter() {
            children.push(SharedType::from(path.clone())?);
        }

        let shared = SharedType::Dir(SharedDir::with(String::from("~"), Some(children)));

        Ok(Self {
            parent: None,
            shared,
        })
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
        let md = fs::metadata(&path)?;

        let path = if md.is_dir() {
            Self::Dir(SharedDir::from(path))
        } else {
            Self::File(SharedFile::from(path))
        };

        Ok(path)
    }
}

#[derive(Debug, Serialize)]
pub struct SharedDir {
    pub path: String,
    pub children: Option<Vec<SharedType>>,
}

impl SharedDir {
    fn with(path: String, children: Option<Vec<SharedType>>) -> Self {
        Self { path, children }
    }
}

impl From<String> for SharedDir {
    fn from(path: String) -> Self {
        Self {
            path,
            children: None,
        }
    }
}

#[derive(Debug, Serialize)]
pub struct SharedFile {
    pub path: String,
}

impl From<String> for SharedFile {
    fn from(path: String) -> Self {
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
