use std::path::PathBuf;

use rocket::response::status::BadRequest;

use crate::{
    guard::{auth::Auth, RelativePath},
    utils::zip_dir,
};

#[derive(Responder)]
#[response(content_type = "application/zip")]
pub struct Archive(Vec<u8>);

#[get("/archive/<path..>")]
pub fn archive_dir(path: RelativePath, _auth: Auth) -> Result<Archive, BadRequest<String>> {
    let path = PathBuf::from(path);

    if path.is_file() {
        return Err(BadRequest(Some("Path is not a directory".to_string())));
    }

    let bytes = match zip_dir(&path) {
        Ok(b) => b,
        Err(err) => return Err(BadRequest(Some(err.to_string()))),
    };

    Ok(Archive(bytes))
}
