use std::path::PathBuf;

use rocket::{
    http::uri::{fmt::Path, Segments},
    request::FromSegments,
};

pub struct RelativePath(PathBuf);

#[derive(Debug)]
pub struct BadStart<'a>(&'a str);

impl<'r> FromSegments<'r> for RelativePath {
    type Error = BadStart<'r>;

    fn from_segments(segments: Segments<'r, Path>) -> Result<Self, Self::Error> {
        let mut path = PathBuf::new();
        for segment in segments {
            if segment.starts_with("..") {
                return Err(BadStart(segment));
            }

            path.push(segment);
        }

        Ok(RelativePath::from(path))
    }
}

impl From<PathBuf> for RelativePath {
    fn from(path: PathBuf) -> Self {
        RelativePath(path)
    }
}

impl From<RelativePath> for PathBuf {
    fn from(path: RelativePath) -> Self {
        path.0
    }
}
