use std::{path::PathBuf, str::FromStr};

use crate::utils::STATIC;
use rocket::{http::ContentType, response::status::NotFound};

#[get("/static/<path..>")]
pub fn static_file_server<'r>(path: PathBuf) -> Result<(ContentType, &'r [u8]), NotFound<String>> {
    let guess = mime_guess::from_path(&path);
    let mime = match guess.first() {
        Some(mime) => mime,
        None => mime_guess::mime::STAR_STAR,
    };

    let content_type = ContentType::from_str(mime.essence_str()).unwrap();
    let file = match STATIC.get_file(&path) {
        Some(file) => file,
        None => return Err(NotFound(String::from("File not found"))),
    };

    Ok((content_type, file.contents()))
}
