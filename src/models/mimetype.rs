use std::path::PathBuf;

use mime_guess::Mime;
use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct MimeType {
    pub main: String,
    pub sub: String,
}

impl From<Mime> for MimeType {
    fn from(mime: Mime) -> Self {
        Self {
            main: mime.type_().to_string(),
            sub: mime.subtype().to_string(),
        }
    }
}

impl From<&PathBuf> for MimeType {
    fn from(path: &PathBuf) -> Self {
        mime_guess::from_path(path)
            .first_or(mime_guess::mime::STAR_STAR)
            .into()
    }
}
