use include_dir::{include_dir, Dir};

pub static STATIC: Dir = include_dir!("$CARGO_MANIFEST_DIR/static");
pub static TEMPLATES: Dir = include_dir!("$CARGO_MANIFEST_DIR/templates");
